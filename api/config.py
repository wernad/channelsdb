import configparser

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
if not config.read('config.ini'):
    raise IOError('Cannot read config.ini')
