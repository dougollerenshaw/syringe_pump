import Pyro4

# use name server object lookup uri shortcut
stepper_server = Pyro4.Proxy("PYRONAME:stepper.server")
