from modules.libraries import *

# Create a config parser
config = configparser.ConfigParser()

# Read the config file
config.read('config.properties')

# Get paths from the config file

class Props:

    DOWNLOAD_PATH = config.get('Downloads', 'downloads.path')
    LOGS_PATH = config.get('LOGS', 'logs.path')

