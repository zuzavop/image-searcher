import os
from ast import literal_eval

import clip
import pandas as pd
import torch as torch
from django.db import models
import numpy as np

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
finding = [4156, 7522, 9373, 3877, 1821, 912, 11850, 3977, 2416, 101]
finded = 0


def get_data():
    global clip_data, class_data, classes
    print('loading data...')
    for fn in sorted(os.listdir(path_data + "clip")):
        clip_data.append(torch.load(path_data + f"clip/{fn}"))

    class_data = pd.read_csv(path_data + "result.csv", sep=';').set_index('id')
    class_data = class_data.to_dict()['top']
    class_data = {int(key): literal_eval(value) for key, value in class_data.items()}

    with open(path_data + 'nounlist.txt', 'r') as f:
        for line in f:
            classes.append(line[:-1].replace("'", '"'))


get_data()
