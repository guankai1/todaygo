import configparser


class ConfigparserHandler(object):

    def __init__(self, file):
        self.file = file
        self.config = configparser.ConfigParser()
        self.config.read(file, encoding='utf-8')

    def get_data(self, key, name):
        return self.config.get(key, name)

    def set_data(self, key, name, value):
        self.config.set(key, name, value)
        with open(self.file, 'w') as f:
            self.config.write(f)
