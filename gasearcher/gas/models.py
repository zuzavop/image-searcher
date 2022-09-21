import os
import random
from ast import literal_eval

import clip
import pandas as pd
import torch as torch
from django.db import models

from gasearcher.settings import STATICFILES_DIRS


class Image(models.Model):
    index = models.IntegerField(default=0)
    classes = models.TextField()

    def __str__(self):
        return self.index


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

clip_data = []
class_data = {}
classes = []
path_data = os.path.join(STATICFILES_DIRS[0], "data/")
finding = [144, 198, 214, 300, 838, 870, 900, 1031, 1181, 1215, 1840, 2315, 2416, 3558, 3658, 3977, 4477, 4952,
           6735, 7051, 7479, 7531, 7541, 7581, 7682, 7977, 8108, 8378, 8486, 8527, 8598, 8637, 8687, 8956, 9138, 9180,
           9287, 9404, 9818, 9883, 10151, 11850]
# finding = []
for i in range(40):
    new_int = random.randint(1, 11870)
    if new_int not in finding:
        finding.append(new_int)
random.shuffle(finding)
last_search = {}


def get_data():
    global clip_data, class_data, classes
    print('loading data...')
    for fn in sorted(os.listdir(path_data + "old_clip")):
        clip_data.append(torch.load(path_data + f"old_clip/{fn}"))

    class_data = pd.read_csv(path_data + "result.csv", sep=';').set_index('id')
    class_data = class_data.to_dict()['top']
    class_data = {int(key) - 1: literal_eval(value) for key, value in class_data.items()}

    with open(path_data + 'nounlist.txt', 'r') as f:
        for line in f:
            classes.append(line[:-1].replace("'", '"'))


get_data()
