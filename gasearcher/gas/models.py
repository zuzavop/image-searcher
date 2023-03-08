import os

import clip
import torch as torch

from gasearcher.gas.data import get_clip_data, get_context, get_classes, load_first_screen, get_photos_classes, \
    set_finding
from gasearcher.gasearcher.settings import STATICFILES_DIRS

# clip
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# configuration
sea_database = True
combination = True

path_data = os.path.join(STATICFILES_DIRS[0], "data/")
path_log = path_data + "message.csv"
path_clip = path_data + ("sea_clip" if sea_database else "clip")
path_nounlist = path_data + ("sea_nounlist.txt" if sea_database else "new_nounlist.txt")
path_classes = path_data + ("sea_result.csv" if sea_database else "v3c_result.txt")
size_dataset = 22036 if sea_database else 20000
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result

clip_data = get_clip_data(path_clip)
class_data = get_photos_classes(path_classes)
classes, class_pr = get_classes(path_nounlist)
last_search = {}  # vectors of last text search
same_video = get_context(sea_database, path_data, clip_data,
                         sur)  # indexes of images in same video (high probability of same looking photos)
finding = set_finding(sea_database, size_dataset)
first_show = load_first_screen(class_data, size_dataset)


