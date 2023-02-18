import os
import random
from ast import literal_eval

import clip
import numpy as np
import pandas as pd
import torch as torch
from sklearn_som.som import SOM

from gasearcher.settings import STATICFILES_DIRS

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

sea_database = True
combination = True

path_data = os.path.join(STATICFILES_DIRS[0], "data/")
path_log = path_data + "message.csv"
path_clip = path_data + ("sea_clip" if sea_database else "clip")
path_nounlist = path_data + ("sea_nounlist.txt" if sea_database else "new_nounlist.txt")
path_classes = path_data + ("sea_result.csv" if sea_database else "v3c_result.txt")
size_dataset = 22036 if sea_database else 20000

clip_data = []
class_data = {}
classes = []
last_search = {}  # vectors of last text search
same_video = {}  # indexes of images in same video (high probability of same looking photos)
class_pr = {}
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result

sea_finding = [91, 97, 105, 193, 317, 362, 426, 646, 791, 811, 1337, 1419, 1623, 1851, 2235, 2486, 2580, 2685, 4646,
               5541, 5599, 8931, 9828, 10759, 14198, 16545, 17862, 2549, 2585, 2658, 2742, 2785, 2809, 2951, 3053, 3415,
               3951, 4022, 4481, 4999, 5025, 5104, 5282, 5358, 5413, 5432, 6114, 6231, 6257, 6295, 7346, 8740, 8912,
               9368, 9487, 9600, 9772, 10739, 11643, 12525, 12785, 12829, 12906, 13252, 13333, 13947, 14346, 14417,
               15450, 16062, 16631, 16673, 19807, 21412]
random.shuffle(sea_finding)
finding = sea_finding[:20] if sea_database else []
for i in range(80):
    new_int = random.randint(1, size_dataset)
    if new_int not in finding:
        finding.append(new_int)


def get_data(is_sea_database):
    global clip_data, class_data, classes, same_video
    print('loading data...')

    for fn in sorted(os.listdir(path_clip)):
        clip_data.append(torch.load(path_clip + f"/{fn}"))

    class_data = pd.read_csv(path_classes, sep=';').set_index('id').to_dict()['top']
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


get_data(sea_database)

# get first window - SOM
input_data = np.array(torch.cat(clip_data))
data_som = SOM(m=5, n=12, dim=len(clip_data[0][0]))
X = data_som.fit_predict(input_data)

first_show = [21535 for _ in range(12 * 5)]
for i in range(len(first_show)):
    if i in X:
        first_show[i] = np.random.choice(np.where(X == i)[0])
