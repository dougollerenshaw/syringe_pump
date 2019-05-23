import socket

configuration_values = {
    'servername':'stepper.server',
}

class Config(object):
    def __init__(self):
        self.hostname = self.get_hostname()
        self.ip = self.get_ip()
        for key in configuration_values:
            setattr(self, key, configuration_values[key])

    def get_hostname(self):
        return socket.gethostname()

    def get_ip(self):
        hostname = self.get_hostname()
        return socket.gethostbyname(hostname)

if __name__ == '__main__':
    config = Config()
    print(config.servername)
    print(config.ip)