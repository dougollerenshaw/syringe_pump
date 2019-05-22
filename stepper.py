# from pyfirmata import Arduino, util
from gpiozero import DigitalOutputDevice
import time


class Stepper(object):
    def __init__(self, port='/dev/ttyACM0', syringe='5ml', mode='rpi', disable_when_inactive=True):
        self.mode = mode
        if self.mode == 'arduino':
            self.arduino = Arduino(port)
            self.disable_pin = 2
            self.dir_pin = 4
            self.step_pin = 3
            self.mc1 = 5
            self.mc2 = 6
            self.mc3 = 7
        elif self.mode == 'rpi':
            self.disable_pin = DigitalOutputDevice(2)
            self.dir_pin = DigitalOutputDevice(4)
            self.step_pin = DigitalOutputDevice(3)
            self.mc1 = DigitalOutputDevice(5)
            self.mc2 = DigitalOutputDevice(6)
            self.mc3 = DigitalOutputDevice(7)
            self.pin8 = DigitalOutputDevice(8)

        # should we turn off the motor between commands?
        self.disable_when_inactive = disable_when_inactive

        # the following are specific to a NEMA17 stepper with a T8 leadscrew
        self.steps_per_rotation = 200
        self.mm_per_rotation = 8

        self.step_count = 0
        # set as maximum step number to keep from pulling plunger from syringe
        self.max_limit = None
        self.min_limit = None  # set as minimum step number to avoid bottoming out
        self._direction_multiplier = 0

        self.set_mm_per_ml(syringe, calibrate_steps=False)

        self._pin13 = 0

        self.stepsize = "sixteenth"
        self.set_stepsize(self.stepsize)

        self.direction = "cw"
        self.set_direction(self.direction)

        if self.disable_when_inactive:
            self.set_pin(self.disable_pin, 1)
        else:
            self.set_pin(self.disable_pin, 0)

    def calibrate(self, syringe):
        self.set_mm_per_ml(syringe, calibrate_steps=True)

    def set_mm_per_ml(self, syringe, calibrate_steps=True):
        mm_per_ml = {
            '5ml': 44./5,
            '3ml': 51.7/3,
            '1ml': 57.
        }

        self.mm_per_ml = mm_per_ml[syringe.lower()]
        print('configuring for a {} syringe with {} mm of travel per mL'.format(
            syringe, self.mm_per_ml))
        if calibrate_steps:
            self.set_steps_per_ul()

    def set_steps_per_ul(self):
        self.ul_per_step = 1000 / \
            (self.mm_per_ml/self.mm_per_rotation *
             self.steps_per_rotation/self._step_deci)

    def set_stepsize(self, stepsize):
        step_def = {
            'full': [0, 0, 0],
            'half': [1, 0, 0],
            'quarter': [1, 0, 1],
            'eighth': [1, 1, 0],
            'sixteenth': [1, 1, 1]
        }
        step_deci = {
            'full': 1.,
            'half': 1./2,
            'quarter': 1./4,
            'eighth': 1./8,
            'sixteenth': 1./16
        }
        for i, pin in enumerate([self.mc1, self.mc2, self.mc3]):
            self.set_pin(pin, step_def[stepsize][i])
        self._stepsize = stepsize
        self._step_deci = step_deci[stepsize]
        self.set_steps_per_ul()

    def toggle_builtin_led(self):
        print('current state is {}, setting to {}'.format(
            self._pin13, abs(self._pin13 - 1)))
        self.set_pin(13, abs(self._pin13 - 1))
        self._pin13 = abs(self._pin13 - 1)

    def set_pin(self, pin_to_set, state):
        if self.mode == 'arduino':
            self.arduino.digital[pin_to_set].write(state)
        elif self.mode == 'rpi':
            pin_to_set.value = state

    def set_direction(self, direction):

        if direction.lower() == 'cw' or direction.lower() == 'retract':
            self.set_pin(self.dir_pin, 0)
            self._direction_multiplier = -1
        elif direction.lower() == 'ccw' or direction.lower() == 'dispense':
            self.set_pin(self.dir_pin, 1)
            self._direction_multiplier = 1
        self._direction = direction
        return direction

    def dispense(self, volume):
        steps = round(volume/self.ul_per_step)
        print('delivering {} ul in {} steps'.format(volume, steps))
        self.rotate(steps, direction='dispense')

    def retract(self, volume=1000):
        steps = round(volume/self.ul_per_step)
        print('retracting {} ul in {} steps'.format(volume, steps))
        self.rotate(steps, direction='retract')

    def rotate(self, steps, direction=None, delay=0.000):
        # make sure direction and stepsize are set
        if direction is not None:
            self.direction = self.set_direction(direction)
        if self.stepsize != self._stepsize:
            self.set_stepsize(self.stepsize)
        if self.direction != self._direction:
            self.set_direction(self.direction)

        # cast steps as int
        steps = int(steps)

        # enable stepper
        if self.disable_when_inactive:
            self.set_pin(self.disable_pin, 0)

        # toggle step pin in loop
        for i in range(steps):
            self.step_count += self._direction_multiplier
            self.set_pin(self.step_pin, 0)
            self.set_pin(self.step_pin, 1)
            time.sleep(delay)

        # disable stepper (otherwise it makes a high pitch whine while it waits)
        if self.disable_when_inactive:
            self.set_pin(self.disable_pin, 1)
        print('done stepping, current step count = {}'.format(self.step_count))
        time.sleep(delay)
