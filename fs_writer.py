import definitions
import config


class FSWriter:
    def __init__(self, year):
        self.name = year + '.txt'
        self.f = open(definitions.ROOT_DIR + config.directory + '/' + self.name.replace('/', ''), 'r+')

    def write(self, stream):
        self.f.write(stream.encode('utf-8'))

    def read_all(self):
        return self.f.readlines()

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
