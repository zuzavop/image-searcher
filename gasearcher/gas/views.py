import secrets
from collections import Counter

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from gas.models import device, model, clip_data, path_log, finding, class_data, classes, last_search, same_video, \
    showing, class_pr, combination, first_show


def get_data_from_clip_text_search(query, session, found, activity):
    # get normalize features of text query
    with torch.no_grad():
        text_features = model.encode_text(clip.tokenize([query]).to(device))
    text_features /= np.linalg.norm(text_features)

    # get distance of vectors
    scores = (np.concatenate([1 - (torch.cat(clip_data) @ text_features.T)], axis=None))

    new_scores = list(np.argsort((scores + last_search[session]) if combination else scores))
    # save score for next search
    if combination:
        last_search[session] = scores

    # if searching image is present in context (surrounding of image) of any image in shown result same is equal 1
    same = 1 if len(list(set(new_scores[:showing]) & set(same_video[finding[found]]))) > 0 else 0
    # write down log
    with open(path_log, "a") as log:
        log.write(query + ';' + str(finding[found]) + ';' + session + ';' + str(
            new_scores.index(finding[found]) + 1) + ';' + str(same) + ';"' + activity[:-1] + '"' + '\n')

    return new_scores[:showing]


def get_data_from_clip_image_search(image_query):
    # get features of image query
    image_query_index = int(image_query)
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(np.concatenate([1 - (torch.cat(clip_data) @ image_query)], axis=None)))

    return scores[:showing]


def search(request):
    if not request.session.get('session_id'):
        return render(request, 'index.html')

    template = loader.get_template('index.html')

    # load index of currently searching image from cookies
    found = int(request.COOKIES.get('index')) if request.COOKIES.get('index') is not None else 0
    if found >= len(finding):  # control of end
        return redirect('/end')
    data = first_show

    if request.GET.get('query'):
        data = get_data_from_clip_text_search(request.GET['query'], request.session['session_id'], found,
                                              request.COOKIES.get('activity'))
    else:
        # reset save search if user use any other method than text search
        last_search[request.session['session_id']] = np.zeros(len(clip_data))
        if request.GET.get('id'):
            data = get_data_from_clip_image_search(request.GET['id'])

    # get classes of current shown result
    data_to_display = {str(i): ([] if i not in class_data else class_data[i]) for i in data}
    # get top classes contains in result
    top_classes = [word for word, word_count in
                   Counter(np.concatenate([a for a in data_to_display.values()], axis=None)).most_common(5) if
                   word_count > 5]

    send_data = {
        'list_photo': data_to_display,
        'percent': class_pr,
        'classes': ','.join(classes),
        'top_classes': top_classes[::-1],
        'find_id': finding[found]
    }

    return HttpResponse(template.render(send_data, request))


def index(request):
    # "login" - setting session id
    request.session['session_id'] = secrets.token_urlsafe(6)
    last_search[request.session['session_id']] = np.zeros(len(clip_data))
    return render(request, 'start.html')


def end(request):
    return render(request, 'end.html')
