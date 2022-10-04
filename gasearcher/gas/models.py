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

sea_finding = [91, 97, 105, 193, 317, 362, 426, 590, 646, 772, 791, 811, 844, 1087, 1337, 1419, 1623, 1851, 1999, 2129,
               2261, 2235, 2295, 2486, 549, 2479, 2580, 2685, 3006, 4646, 4719, 5541, 5599, 8931, 9828, 10759, 11666,
               13521, 14198, 14761, 16545, 17862, 18806, 19929, 2549, 2585, 2658, 2682, 2742, 2785, 2809, 2819, 2951,
               3053, 3415, 3604, 3951, 4022, 4314, 4481, 4983, 4999, 5025, 5104, 5282, 5358, 5413, 5432, 5945, 6030,
               6070, 6114, 6134, 6231, 6257, 6295, 7346, 8740, 8812, 8912, 9104, 9233, 9368, 9487, 9600, 9656, 9772,
               10123, 10739, 11566, 11643, 12525, 12785, 12829, 12906, 13252, 13333, 13947, 14096, 14346, 14417, 15450,
               16062, 16142, 16394, 16631, 16673, 18547, 18677, 19807, 20426, 20912, 21412, 21617, 21876]

print(len(sea_finding))

finding = [3604, 4719, 17862, 4022, 2549, 3006, 2129, 2819, 2261, 549, 10759, 11666, 2742, 2951, 2235, 9828, 2295, 4314, 4646, 3053, 2486, 3951, 5541, 2809, 4481, 13521, 3415]
# for i in range(120):
#     new_int = random.randint(1, 22036)
#     if new_int not in finding:
#         finding.append(new_int)
# random.shuffle(finding)

last_search = {}  # vectors of last text search
same_video = {}  # indexes of images in same video (high probability of same looking photos)
class_pr = {}
sur = 5  # surrounding of image in context
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
