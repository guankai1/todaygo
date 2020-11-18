import logging
import logging.config
from os import path


class LogHandler(object):

    def __init__(self):
        log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
        print("log_fiel_path: "+str(log_file_path))
        logging.config.fileConfig(log_file_path)
        print("fileconfig")
        print(logging.config.fileConfig(log_file_path))
        self.logging = logging.getLogger()
        print("self.logging: "+str(self.logging))

    def log(self):
        return self.logging
if  __name__ == '__main__':
    loghand = LogHandler()
    loghand.log()
    loghand.__init__()
