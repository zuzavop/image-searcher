import os
import random
from ast import literal_eval

import numpy as np
import pandas as pd
import torch as torch
from sklearn_som.som import SOM


def get_clip_data(path_clip):
    print('loading data...')
    clip_data = []

    # preprocessed data from clip
    for fn in sorted(os.listdir(path_clip)):
        clip_data.append(torch.load(path_clip + f"/{fn}"))
    return clip_data


def get_photos_classes(path_classes):
    class_data = pd.read_csv(path_classes, sep=';').set_index('id').to_dict()['top']
    return {int(key) - 1: literal_eval(value) for key, value in class_data.items()}


def get_classes(path_nounlist):
    classes = []
    class_pr = {}
    with open(path_nounlist, 'r') as f:
        for line in f:
            split = line.split(":")
            classes.append(split[0][:-1])
            class_pr[len(classes) - 1] = float(split[1][:-1])
    return classes, class_pr


def get_context(is_sea_database, path_data, clip_data, sur):
    same_video = {}
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

    return same_video


def load_first_screen(class_data, size_dataset):
    # get first window - SOM of labels
    first_show = [0 for _ in range(12 * 5)]
    input_data = np.array(list(class_data.values()))
    som = SOM(m=5, n=12, dim=len(input_data[0]))

    prediction = som.fit_predict(input_data)

    for i in range(len(first_show)):
        if i in prediction:
            first_show[i] = np.random.choice(np.where(prediction == i)[0])
        else:
            first_show[i] = random.randint(1, size_dataset)

    return first_show


def set_finding(sea_database, size_dataset, path_selection):
    # images that should be found
    if sea_database:
        with open(path_selection, 'r') as file:
            sea_finding = [int(num) for num in file.readline().split(',')]
        random.shuffle(sea_finding)

    finding = sea_finding[:20] if sea_database else []
    for i in range(80):
        new_int = random.randint(1, size_dataset)
        if new_int not in finding:
            finding.append(new_int)

    return finding
