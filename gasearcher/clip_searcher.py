import clip
import numpy as np
import torch
from numba import jit

from var import device, model, clip_data


@jit(nopython=True)
def cosine_distance(h1, h2):
    return 1 - np.dot(h1, h2)


@jit(nopython=True)
def get_data_from_clip_text_search(query):
    text = clip.tokenize(query).to(device)
    with torch.no_grad():
        text_features = np.transpose(model.encode_text(text))
        text_features /= np.linalg.norm(text_features)

    scores = np.zeros(len(clip_data))
    for i in range(len(clip_data)):
        scores[i] = cosine_distance(clip_data[i], text_features)

    return np.argsort(scores)


@jit(nopython=True)
def get_data_from_clip_image_search(image_query):
    image_query_index = int((image_query[-9:])[:5]) - 1
    image_query = np.transpose(clip_data[image_query_index])

    scores = np.zeros(len(clip_data))
    for i in range(len(clip_data)):
        scores[i] = cosine_distance(clip_data[i], image_query)

    return np.argsort(scores)
