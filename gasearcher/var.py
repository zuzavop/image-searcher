import os
import clip
import numpy as np
import torch as torch

from gas.models import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

clip_data = []


def get_image_class(index):
    return Image.objects.get(index=index)


def get_clip_data():
    global clip_data
    for fn in sorted(os.listdir("../../data/clip")):
        clip_data.append(torch.load(f"../../data/clip/{fn}"))
        clip_data[-1] = clip_data[-1]/np.linalg.norm(clip_data[-1])


get_clip_data()