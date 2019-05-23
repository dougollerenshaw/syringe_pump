import socket
import subprocess

configuration_values = {
    'servername':'stepper.server',
    'syringe':'3ml',
    'mode':'rpi'
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
        ip = subprocess.check_output(['hostname', '-I'])
        return ip.decode("utf-8").split()[0]

if __name__ == '__main__':
    config = Config()
    print(config.servername)
    print(config.ip)