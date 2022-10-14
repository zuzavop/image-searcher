import os
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

finding = [7847, 4008, 16946, 9028, 1155, 17746, 783, 8446, 14537, 14630, 6379, 15575, 8965, 12693, 8941, 12742, 1664,
           2523, 19890, 2944, 15936, 3019, 11904, 5241, 12801, 9381, 11061, 13399, 5067, 3035, 10524, 17273, 12112,
           16355, 5570, 2253, 12736, 8797, 18719, 14587, 2546, 11901, 13744, 4729, 8056, 13772, 7419, 5950, 16813, 1006,
           898, 6670, 19946, 2075, 11450, 9074, 4436, 3068, 6546, 9408, 3809, 8354, 17558, 4056, 3387, 12863, 14202,
           543, 1985, 7782, 10924, 15085, 11022, 3682, 8541, 2134, 11577, 4094, 16476, 10432, 17507, 6744, 705]
# for i in range(80):
#     new_int = random.randint(1, 20000)
#     if new_int not in finding:
#         finding.append(new_int)
# random.shuffle(finding)

last_search = {}  # vectors of last text search
same_video = {}  # indexes of images in same video (high probability of same looking photos)
class_pr = {}
sur = 7  # surrounding of image in context
showing = 60  # number of shown image in result


def get_data():
    global clip_data, class_data, classes
    print('loading data...')
    for fn in sorted(os.listdir(path_data + "clip")):
        clip_data.append(torch.load(path_data + f"clip/{fn}"))

    class_data = pd.read_csv(path_data + "new_result.csv", sep=';').set_index('id')
    class_data = class_data.to_dict()['top']
    class_data = {int(key) - 1: literal_eval(value) for key, value in class_data.items()}

    with open(path_data + 'new_nounlist.txt', 'r') as f:
        for line in f:
            classes.append(line.split(":")[0][:-1].replace("'", '"'))
            class_pr[len(classes) - 1] = float(line.split(":")[1][:-1])

    # bottom = 0
    # with open(path_data + 'sea_videos.txt', 'r') as f:
    #     for line in f:
    #         top = int(line[:-1]) - 1
    #         for i in range(bottom, top):
    #             same = [_ for _ in range(bottom if bottom >= i - sur else i - sur,
    #                                      top if top <= i + sur else i + sur)]
    #             same_video[i] = same
    #         bottom = top
    for i in range(20000):
        same_video[i] = [i]


get_data()
