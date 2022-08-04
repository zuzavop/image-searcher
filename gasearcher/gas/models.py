from django.db import models

import os

import clip
import torch as torch
from PIL import ImageTk

from gasearcher.settings import STATICFILES_DIRS


class Image(models.Model):
    index = models.IntegerField(default=0)
    classes = models.TextField()

    def __str__(self):
        return self.index


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

clip_data = []
filenames = []
path_data = os.path.join(STATICFILES_DIRS[0], "data/")


def get_image_class(index):
    return Image.objects.get(index=index)


def get_image(index):
    return ImageTk.PhotoImage(Image.open(filenames[index]))


def get_data():
    global clip_data, filenames
    print("loading data...")
    for fn in sorted(os.listdir(path_data + "clip")):
        clip_data.append(torch.load(path_data + f"clip/{fn}"))

    for fn in sorted(os.listdir(path_data + "photos")):
        filenames.append(fn)


get_data()
