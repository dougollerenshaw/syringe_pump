import Pyro4

stepper_server = Pyro4.Proxy("PYRONAME:stepper.server")    # use name server object lookup uri shortcut