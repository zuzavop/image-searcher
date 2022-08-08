import secrets
import sys

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

import gas
from gas.models import device, model, clip_data, path_data, finding, finded, class_data, classes


def cosine_distance(h1, h2):
    return 1 - np.dot(h1, h2)


def get_data_from_clip_text_search(query, session):
    text = clip.tokenize(query).to(device)
    with torch.no_grad():
        text_features = np.transpose(model.encode_text(text))
        text_features /= np.linalg.norm(text_features)

    scores = list(np.argsort(
        np.concatenate([cosine_distance(clip_data[i], text_features) for i in range(len(clip_data))], axis=None)))

    old_stdout = sys.stdout
    log_file = open(path_data + "message.csv", "a")
    sys.stdout = log_file
    print(query + ';' + str(finding[finded]) + ';' + session + ';' + str(scores.index(finding[finded])))
    sys.stdout = old_stdout
    log_file.close()

    return scores


def get_data_from_clip_image_search(image_query):
    image_query_index = int(image_query)
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(
        np.concatenate([cosine_distance(clip_data[i], image_query) for i in range(len(clip_data))], axis=None)))

    return scores


def search(request):
    template = loader.get_template('index.html')
    dat = [i for i in range(2, 62)]
    if request.GET.get('query'):
        dat = get_data_from_clip_text_search(request.GET['query'], request.session['session_id'])[:60]
    elif request.GET.get('id'):
        dat = get_data_from_clip_image_search(request.GET['id'])[:60]
    elif request.GET.get('answer'):
        if int(request.GET['answer']) == finding[gas.models.finded]:
            gas.models.finded += 1
    data_to_display = {i: ([] if i not in class_data else [a for a in class_data[i]]) for i in dat}
    data = {
        'list_photo': data_to_display,
        'classes': ','.join(classes),
        'find_id': finding[gas.models.finded]
    }
    return HttpResponse(template.render(data, request))


def index(request):
    # "login" - setting session id
    request.session['session_id'] = secrets.token_urlsafe(6)
    return redirect('/search')  # redirect to search
