import os
from gasearcher.settings import STATICFILES_DIRS

# configuration
SEA_DATABASE = True
COMBINATION = True  # if result should be combined with previous result
PATH_DATA = os.path.join(STATICFILES_DIRS[0], "data/")  # get path to data
SUR = 7  # surrounding of image in context
SHOWING = 60  # number of shown image in result