import configparser
import os
import signal
import sys

import daemon
import lockfile

from anova2mqtt.anova2mqtt import main, shutdown

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.anova2mqtt/config.ini'))

# with daemon.DaemonContext(
#         stdout=sys.stdout,
#         stderr=sys.stderr,
#         signal_map={
#             signal.SIGTERM: shutdown,
#             signal.SIGTSTP: shutdown
#         },
#         pidfile=lockfile.FileLock(os.path.expanduser('~/.anova2mqtt/anova2mqtt.pid')),
# ):
main(config)
