import secrets
import sys
from collections import Counter

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from gas.models import device, model, clip_data, path_data, finding, class_data, classes, last_search


def get_data_from_clip_text_search(query, session, found):
    text = clip.tokenize(query).to(device)
    with torch.no_grad():
        text_features = np.transpose(model.encode_text(text))
        text_features /= np.linalg.norm(text_features)

    scores = list(np.argsort(np.concatenate([1 - (torch.cat(clip_data) @ text_features)], axis=None)))

    old_stdout = sys.stdout
    log_file = open(path_data + "message.csv", "a")
    sys.stdout = log_file
    print(query + ';' + str(finding[found]) + ';' + session + ';' + str(scores.index(finding[found]) + 1))
    sys.stdout = old_stdout
    log_file.close()

    return scores


def get_data_from_clip_image_search(image_query):
    image_query_index = int(image_query)
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(np.concatenate([1 - (torch.cat(clip_data) @ image_query)], axis=None)))

    return scores


def search(request):
    template = loader.get_template('index.html')
    found = int(request.COOKIES.get('index')) if request.COOKIES.get('index') is not None else 0
    data = [i for i in range(1, 61)]

    if request.GET.get('query'):
        data = get_data_from_clip_text_search(request.GET['query'], request.session['session_id'], found)[:60]
        last_search[request.session['session_id']] = data
    elif request.GET.get('id'):
        data = get_data_from_clip_image_search(request.GET['id'])[:60]
    elif request.GET.get('answer'):
        if int(request.GET['answer']) == finding[found] and found >= len(finding):
            return redirect('/end')

    data_to_display = {str(i): ([] if i not in class_data else [a for a in class_data[i]]) for i in data}
    top_classes = [word for word, word_count in
                   Counter(np.concatenate([a for a in data_to_display.values()], axis=None)).most_common(5) if
                   word_count > 5]
    send_data = {
        'list_photo': data_to_display,
        'classes': ','.join(classes),
        'top_classes': top_classes[::-1],
        'find_id': finding[found]
    }
    return HttpResponse(template.render(send_data, request))


def index(request):
    # "login" - setting session id
    request.session['session_id'] = secrets.token_urlsafe(6)
    return redirect('/search')  # redirect to search


def end(request):
    return render(request, 'end.html')
