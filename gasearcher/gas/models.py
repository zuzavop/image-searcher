import os
import random
from ast import literal_eval

import clip
import numpy as np
import pandas as pd
import torch as torch

from gasearcher.settings import STATICFILES_DIRS

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

clip_data = []
class_data = {}
classes = []
path_data = os.path.join(STATICFILES_DIRS[0], "data/")
path_log = path_data + "message.csv"
path_clip = path_data + "sea_clip"
path_nounlist = path_data + "sea_nounlist.txt"
path_classes = path_data + "sea_result.csv"

last_search = {}  # vectors of last text search
same_video = {}  # indexes of images in same video (high probability of same looking photos)
class_pr = {}
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result

finding = []
for _ in range(80):
    new_int = random.randint(1, 20000)
    if new_int not in finding:
        finding.append(new_int)
random.shuffle(finding)


def get_data(is_sea_database):
    global clip_data, class_data, classes, same_video
    print('loading data...')
    for fn in sorted(os.listdir(path_clip)):
        clip_data.append(torch.load(path_clip + f"/{fn}"))

    class_data = pd.read_csv(path_classes, sep=';').set_index('id')
    class_data = class_data.to_dict()['top']
    class_data = {int(key) - 1: literal_eval(value) for key, value in class_data.items()}

    with open(path_nounlist, 'r') as f:
        for line in f:
            split = line.split(":")
            classes.append(split[0][:-1])
            class_pr[len(classes) - 1] = float(split[1][:-1])

    if is_sea_database:
        bottom = 0
        with open(path_data + 'sea_videos.txt', 'r') as f:
            for line in f:
                top = int(line[:-1]) - 1
                same_video.update({i: np.arange(max(bottom, i - sur), min(top, i + sur)) for i in range(bottom, top)})
                bottom = top
    else:
        for i in range(len(clip_data)):
            same_video[i] = [i]


get_data(True)
