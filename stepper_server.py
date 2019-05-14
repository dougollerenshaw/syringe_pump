from pyfirmata import Arduino, util
import Pyro4

Pyro4.config.REQUIRE_EXPOSE = False

from stepper import Stepper

# NOTE: must have nameserver running on same device
# for example: `python -m Pyro4.naming -n 192.168.0.46 -p 1234`

@Pyro4.expose
class StepperServer(Stepper):
    def __init__(self,port='/dev/ttyACM0',syringe='5ml'):
        Stepper.__init__(self, port=port, syringe=syringe)
        # self.arduino = Arduino(port)
        print('running stepper server')
        print('usb port = {}'.format(port))
        print('syringe = {}'.format(syringe))

    @Pyro4.oneway
    def deliver_reward(self,volume):
        '''
        a one-way (non-blocking) method for delivering a reward
        '''
        self.dispense(volume)


    @Pyro4.expose
    def get_step_count(self):
        return self.step_count

daemon = Pyro4.Daemon("10.128.50.194")                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
print("nameserver = {}".format(ns))
uri = daemon.register(StepperServer)   # register the stepper server as a Pyro object
ns.register("stepper.server", uri)   # register the object with a name in the name server

# print("The daemon runs on port: {}".format(daemon.port))
print("The object's uri is: {}".format(uri))

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
