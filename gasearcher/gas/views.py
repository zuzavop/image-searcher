import secrets
from collections import Counter

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from gas.models import device, model, clip_data, path_log_search, finding, class_data, classes, last_search, \
    showing, class_pr, combination, first_show, is_in_same_video, path_log


def log_text_query(query, new_scores, found, session, activity):
    same = is_in_same_video(new_scores[:showing], found)
    # write down log
    with open(path_log_search, "a") as log:
        log.write(query + ';' + str(finding[found]) + ';' + session + ';' + str(
            new_scores.index(finding[found]) + 1) + ';' + str(same) + ';"' + activity + '"' + '\n')


def log_image_query(query_id, new_scores, found, session):
    same = is_in_same_video(new_scores[:showing], found)
    # write down log
    with open(path_log, "a") as log:
        log.write(str(query_id) + ';' + str(finding[found]) + ';' + session + ';' + str(
            new_scores.index(finding[found]) + 1) + ';' + str(same) + '"' + '\n')


def result_score(features):
    return np.concatenate([1 - (torch.cat(clip_data) @ features)], axis=None)


def text_search(query, session, found, activity):
    # get normalize features of text query
    with torch.no_grad():
        text_features = model.encode_text(clip.tokenize([query]).to(device))
    text_features /= np.linalg.norm(text_features)

    # get distance of vectors
    scores = result_score(text_features.T)

    new_scores = list(np.argsort((scores + last_search[session]) if combination else scores))
    # save score for next search
    if combination:
        last_search[session] = scores

    log_text_query(query, new_scores, found, session, activity)

    return new_scores[:showing]


def image_search(image_query, found, session):
    # get features of image query
    image_query_index = int(image_query)
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(result_score(image_query)))

    log_image_query(image_query, scores, found, session)

    return scores[:showing]


def send_data(request, data, find):
    template = loader.get_template('index.html')

    # get classes of current shown result
    data_to_display = {str(i): ([] if i not in class_data else class_data[i]) for i in data}
    # get top classes contains in result
    top_classes = [word for word, word_count in
                   Counter(np.concatenate([a for a in data_to_display.values()], axis=None)).most_common(5) if
                   word_count > 5]

    sending_data = {
        'list_photo': data_to_display,
        'percent': class_pr,
        'classes': ','.join(classes),
        'top_classes': top_classes[::-1],
        'find_id': find
    }

    return HttpResponse(template.render(sending_data, request))


def search(request):
    if not request.session.get('session_id'):
        return render(request, 'index.html')

    # load index of currently searching image from cookies
    found = int(request.COOKIES.get('index')) if request.COOKIES.get('index') is not None else 0
    if found >= len(finding):  # control of end
        return redirect('/end')
    data = first_show

    if request.GET.get('query'):
        data = text_search(request.GET['query'], request.session['session_id'], found,
                                              request.COOKIES.get('activity')[:-1])
    else:
        # reset save search if user use any other method than text search
        last_search[request.session['session_id']] = np.zeros(len(clip_data))
        if request.GET.get('id'):
            data = image_search(request.GET['id'], found, request.session['session_id'])

    send_data(request, data, finding[found])

def start(request):
    # "login" - setting session id
    request.session['session_id'] = secrets.token_urlsafe(6)
    last_search[request.session['session_id']] = np.zeros(len(clip_data))
    return render(request, 'start.html')


def end(request):
    return render(request, 'end.html')
