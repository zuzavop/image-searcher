import os
import clip
import numpy as np
import torch as torch
from torchvision.models.resnet import resnet50

path = ""

shown = 96

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

model_resnet = resnet50(pretrained=True)
model_resnet = model_resnet.eval()

clip_data = []
resnet_data = []


def get_clip_data():
    global clip_data
    for fn in sorted(os.listdir("clip")):
        clip_data.append(torch.load(f"clip/{fn}"))
        clip_data[-1] = clip_data[-1]/np.linalg.norm(clip_data[-1])


get_clip_data()
