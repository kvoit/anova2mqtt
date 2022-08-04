import configparser
import os

from anova import AnovaCooker

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.anova2mqtt/config.ini'))

cooker = AnovaCooker(config['cooker']['deviceid'])
cooker.authenticate(config['cooker']['email'], config['cooker']['password'])

cooker.cook = True
cooker.save()