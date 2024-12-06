import logging
from logging import Formatter
from rich.progress import track
from rich.console import Console
from rich.logging import RichHandler
import time

from logging.handlers import  RotatingFileHandler
LOGFORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGFORMAT_RICH = '%(message)s'

error_console = Console(stderr=True)

rh = RichHandler(console=error_console)

rh.setFormatter(Formatter(LOGFORMAT_RICH))

logging.basicConfig(
    level=logging.INFO,
    # format=LOGFORMAT,python
    format=LOGFORMAT,
    handlers=[
        rh,
        # logging.StreamHandler(sys.stderr),
        RotatingFileHandler('xxx.log',
                            maxBytes=1024 * 1024 * 10,  # 10Mb
                            backupCount=10)
    ]
    )
log = logging.getLogger('somefancyname')
for n in range(5)   :
    log.info(f"logging .. {n}")
    time.sleep(0.2)
