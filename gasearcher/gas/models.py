import os

import clip
import torch as torch

from gas.data import LoaderDatabase, load_first_screen
from gas.logger import Logger
from gasearcher.settings import STATICFILES_DIRS


# clip
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# configuration
sea_database = True
combination = True # if result should be combined with previous result

path_data = os.path.join(STATICFILES_DIRS[0], "data/") # get path to data
loader = LoaderDatabase(path_data, sea_database)
size_dataset = 22036 if sea_database else 20000
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result

clip_data = loader.get_clip_data()
class_data = loader.get_photos_classes()
classes, class_pr = loader.get_classes()
last_search = {}  # vectors of last text search
finding = loader.set_finding(size_dataset)

# the initial set of images indexes to be shown in the search result
first_show = load_first_screen(class_data, size_dataset)

# logger that logs the search activities
logger = Logger(path_data, showing, finding, loader.get_context(size_dataset, sur))



