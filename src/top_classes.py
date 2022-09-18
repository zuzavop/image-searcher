import os
import clip
import torch
import json
from PIL import Image
from collections import Counter

# load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)

path = "../clip"

for fn in os.listdir(path):
    filename = path + "/" + fn
    # load image features get from clip
    image_features = torch.load(filename)

    # load nounlist (text dataset) features
    text_features = torch.load('result.pt')

    # get top 10 classes for image
    similarity = (100.0 * image_features @ text_features.T)
    values, indices = similarity[0].topk(10)

    # save classes to file
    if not os.path.exists('result/' + fn[:-3] + '.txt'):
        os.mknod('result/' + fn[:-3] + '.txt')

    with open('result/' + fn[:-3] + '.txt', 'a') as f:
        for value, index in zip(values, indices):
            f.write(f"{index}: {100 * value.item():.2f},\n")

# get classes of images to one csv file
path = 'result/'
for fn in os.listdir(path):
    data = {}
    with open(path + fn) as f:
        for line in f:
            (k,v) = line.split(':')
            data[int(k)] = float(v[1:-2])

    new_data = dict(Counter(data).most_common(10))
    data = list(new_data.keys())

    with open('result.csv', 'a') as f:
        f.write(fn[:-4] + ';' + str(data) + '\n')