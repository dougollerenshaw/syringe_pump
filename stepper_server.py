from stepper import Stepper
from config import Config
from pyfirmata import Arduino, util
from gpiozero import DigitalOutputDevice
import Pyro4

Pyro4.config.REQUIRE_EXPOSE = False


# NOTE: must have nameserver running on same device
# for example: `python -m Pyro4.naming -n 192.168.0.46 -p 1234`


@Pyro4.expose
class StepperServer(Stepper):
    def __init__(self, port='/dev/ttyACM0', syringe='5ml', mode='rpi'):
        Stepper.__init__(self, port=port, syringe=syringe)
        # self.arduino = Arduino(port)
        print('running stepper server')
        print('usb port = {}'.format(port))
        print('syringe = {}'.format(syringe))

    @Pyro4.oneway
    def deliver_reward(self, volume):
        '''
        a one-way (non-blocking) method for delivering a reward
        '''
        self.dispense(volume)

    @Pyro4.expose
    def get_step_count(self):
        return self.step_count

    @Pyro4.expose
    def get_max_limit(self):
        return self.max_limit

    @Pyro4.expose
    def get_min_limit(self):
        return self.min_limit

if __name__ == '__main__':

    config = Config()
    server = StepperServer()

    daemon = Pyro4.Daemon(config.ip)                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    print("nameserver = {}".format(ns))
    # register the stepper server as a Pyro object
    uri = daemon.register(server)
    # register the object with a name in the name server
    ns.register("stepper.server", uri)

    # print("The daemon runs on port: {}".format(daemon.port))
    print("The object's uri is: {}".format(uri))

    print("Ready.")
    # start the event loop of the server to wait for calls
    daemon.requestLoop()
