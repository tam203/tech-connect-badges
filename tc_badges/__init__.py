import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'lib')))

import logging
logger = logging.getLogger(__name__.split('.')[0])
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)
