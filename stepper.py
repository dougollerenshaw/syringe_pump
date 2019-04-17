from pyfirmata import Arduino, util
import time

class Stepper(object):
    def __init__(self,port='/dev/ttyACM0'):
        self.arduino = Arduino(port)
        self.disable_pin = 2
        self.dir_pin = 4
        self.step_pin = 3
        self.mc1 = 5
        self.mc2 = 6
        self.mc3 = 7
        self.steps_per_rotation = 200
        self.stepsize="sixteenth"
        self.set_stepsize(self.stepsize)
        self.direction="cw"
        self.set_direction(self.direction)

        self.mm_per_rotation = 8
        self.mm_per_ml = 44./5

        self.arduino.digital[self.disable_pin].write(0)

    def set_steps_per_ul(self):
        self.ul_per_step = 1000/(self.mm_per_ml/self.mm_per_rotation*self.steps_per_rotation/self._step_deci)

    def set_stepsize(self,stepsize):
        step_def = {
            'full':[0,0,0],
            'half':[1,0,0],
            'quarter':[1,0,1],
            'eighth':[1,1,0],
            'sixteenth':[1,1,1]
        }
        step_deci = {
            'full':1.,
            'half':1./2,
            'quarter':1./4,
            'eighth':1./8,
            'sixteenth':1./16
        }
        for i,pin in enumerate([self.mc1,self.mc2,self.mc3]):
            self.arduino.digital[pin].write(step_def[stepsize][i])
        self._stepsize=stepsize
        self._step_deci = step_deci[stepsize]
        self.set_steps_per_ul()

     def set_direction(self,direction):
        if direction.lower() == 'cw' or direction.lower() == 'retract':
            self.arduino.digital[self.dir_pin].write(0)
        elif direction.lower() == 'ccw' or direction.lower() == 'dispense':
            self.arduino.digital[self.dir_pin].write(1)
        self._direction = direction
        return direction

    def dispense(self,volume):
        steps = round(volume/self.ul_per_step)
        print('delivering {} ul in {} steps'.format(volume,steps))
        self.rotate(steps,direction='dispense')

    def retract(self,volume=1000):
        previous_stepsize = self.stepsize
        self.stepsize = 'half'
        self.set_stepsize(self.stepsize)
        steps = round(volume/self.ul_per_step)
        print('retracting {} ul in {} steps'.format(volume,steps))
        self.rotate(steps,direction='retract')
        self.stepsize = previous_stepsize
        self.set_stepsize(self.stepsize)

    def rotate(self,steps,direction=None,delay=0.000):
        if direction is not None:
            self.direction = self.set_direction(direction)
        if self.stepsize != self._stepsize:
            self.set_stepsize(self.stepsize)
        if self.direction != self._direction:
            self.set_direction(self.direction)
        steps = int(steps)
        self.arduino.digital[self.disable_pin].write(0)

        for i in range(steps):
            self.arduino.digital[self.step_pin].write(0)
            time.sleep(delay)
            self.arduino.digital[self.step_pin].write(1)
            time.sleep(delay)
        self.arduino.digital[self.disable_pin].write(1)
        time.sleep(delay)