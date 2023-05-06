import os
from gasearcher.settings import STATICFILES_DIRS

# configuration
SEA_DATABASE = False
COMBINATION = False  # if result should be combined with previous result
PATH_DATA = os.path.join(STATICFILES_DIRS[0], "data/")  # get path to data
SUR = 5  # surrounding of image in context
SHOWING = 60  # number of shown image in result