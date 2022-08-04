import sys

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.template import loader

from gas.models import device, model, clip_data, path_data


def cosine_distance(h1, h2):
    return 1 - np.dot(h1, h2)


def get_data_from_clip_text_search(query):
    old_stdout = sys.stdout
    log_file = open(path_data + "message.log", "w")
    sys.stdout = log_file
    text = clip.tokenize(query).to(device)
    with torch.no_grad():
        text_features = np.transpose(model.encode_text(text))
        text_features /= np.linalg.norm(text_features)

    scores = list(np.argsort(
        np.concatenate([cosine_distance(clip_data[i], text_features) for i in range(len(clip_data))], axis=None)))

    print(query + ';' + str(scores[0]))
    sys.stdout = old_stdout
    log_file.close()

    return scores


def get_data_from_clip_image_search(image_query):
    image_query_index = int((image_query[-9:])[:5]) - 1
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(
        np.concatenate([cosine_distance(clip_data[i], image_query) for i in range(len(clip_data))])))

    return scores


def index(request):
    template = loader.get_template('index.html')
    if request.GET.get('query'):
        data_to_display = get_data_from_clip_text_search(request.GET['query'])[:64]
    elif request.GET.get('id'):
        data_to_display = get_data_from_clip_image_search(request.GET['id'])[:64]
    else:
        data_to_display = [i for i in range(2, 66)]
    data = {
        'list_photo': data_to_display
    }
    return HttpResponse(template.render(data, request))
