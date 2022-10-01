import os
import random
from ast import literal_eval

import clip
import pandas as pd
import torch as torch

from gasearcher.settings import STATICFILES_DIRS

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

clip_data = []
class_data = {}
classes = []
path_data = os.path.join(STATICFILES_DIRS[0], "data/")

finding = []
for i in range(80):
    new_int = random.randint(1, 20000)
    if new_int not in finding:
        finding.append(new_int)
random.shuffle(finding)

last_search = {}  # vectors of last text search
same_video = {}  # indexes of images in same video (high probability of same looking photos)
class_pr = {}
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result


def get_data():
    global clip_data, class_data, classes
    print('loading data...')
    for fn in sorted(os.listdir(path_data + "sea_clip")):
        clip_data.append(torch.load(path_data + f"sea_clip/{fn}"))

    class_data = pd.read_csv(path_data + "sea_result.csv", sep=';').set_index('id')
    class_data = class_data.to_dict()['top']
    class_data = {int(key) - 1: literal_eval(value) for key, value in class_data.items()}

    with open(path_data + 'sea_nounlist.txt', 'r') as f:
        for line in f:
            classes.append(line.split(":")[0][:-1].replace("'", '"'))
            class_pr[len(classes) - 1] = float(line.split(":")[1][:-1])

    bottom = 0
    with open(path_data + 'sea_videos.txt', 'r') as f:
        for line in f:
            top = int(line[:-1]) - 1
            for i in range(bottom, top):
                same = [_ for _ in range(bottom if bottom >= i - sur else i - sur,
                                         top if top <= i + sur else i + sur)]
                same_video[i] = same
            bottom = top
    # for i in range(20000):
    #     same_video[i] = [i]


get_data()
