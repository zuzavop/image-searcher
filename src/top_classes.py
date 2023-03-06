import os
import clip
import torch
import json
from PIL import Image
from collections import Counter

# load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)

path_clip = "../clip"
path_nounlist = 'result.pt'
path_result = 'result/'
result_file = 'result.csv'
top_k = 10
top_labels = 10

for fn in os.listdir(path_clip):
    filename = path_clip + "/" + fn
    # load image features get from clip
    image_features = torch.load(filename)

    # load nounlist (text dataset) features
    text_features = torch.load(path_nounlist)

    # get top 10 classes for image
    similarity = (100.0 * image_features @ text_features.T)
    values, indices = similarity[0].topk(top_k)

    # save classes to file
    if not os.path.exists(path_result + fn[:-3] + '.txt'):
        os.mknod(path_result + fn[:-3] + '.txt')

    with open(path_result + fn[:-3] + '.txt', 'a') as f:
        for value, index in zip(values, indices):
            f.write(f"{index}: {100 * value.item():.2f},\n")

# get classes of images to one csv file
for fn in os.listdir(path_result):
    data = {}
    with open(path + fn) as f:
        for line in f:
            (k,v) = line.split(':')
            data[int(k)] = float(v[1:-2])

    new_data = dict(Counter(data).most_common(top_labels))
    data = list(new_data.keys())

    with open(result_file, 'a') as f:
        f.write(fn[:-4] + ';' + str(data) + '\n')
