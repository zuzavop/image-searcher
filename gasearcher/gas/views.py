import secrets
from collections import Counter

import clip
import numpy as np
import torch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from gas.models import device, model, clip_data, targets, class_data, classes, last_search, showing, class_pr, \
    combination, first_show, logger


def result_score(features):
    """
    Calculate the similarity score of the query feature vector with the CLIP data.

    Args:
        features (numpy.ndarray): A 2D array representing the feature vector of the query.

    Returns:
        numpy.ndarray: A 1D array representing the similarity scores of the query.
    """
    return np.concatenate([1 - (torch.cat(clip_data) @ features)], axis=None)


def text_search(query, session, found, activity):
    """
    Text search using CLIP data.

    Args:
        query (str): The text query.
        session (str): The unique session ID of the user. (used for logging)
        found (int): The index of the currently searching image. (used for logging)
        activity (str): The activity from the user. (used for logging)

    Returns:
        list: A list of indices representing the top search results.
    """
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

    logger.log_text_query(query, new_scores, targets[found], session, activity)

    return new_scores[:showing]


def image_search(image_query, found, session):
    """
    Image search using CLIP data.

    Args:
        image_query (int): The index of the image query.
        found (int): The index of the currently searching image. (used for logging)
        session (str): The unique session ID of the user. (used for logging)

    Returns:
        list: A list of indices representing the top search results.
    """
    # get features of image query
    image_query_index = int(image_query)
    image_query = np.transpose(clip_data[image_query_index])

    scores = list(np.argsort(result_score(image_query)))

    logger.log_image_query(image_query, scores, targets[found], session)

    return scores[:showing]


def prepare_data(request, data, find):
    """
    Generate data used in template (results of search) and send the data to the index.html template.

    Args:
        request (HttpRequest): The HTTP request.
        data (list): The list of search results.
        find (int): The index of currently searching image.

    Returns:
        HttpResponse: The HTTP response.
    """
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
        'find_id': str(find)
    }

    return HttpResponse(template.render(sending_data, request))


def search(request):
    """
    Performs a search query and send the result to the template.

    Args:
        request (HttpRequest): The HTTP request containing information about the current request.

    Returns:
        Union[HttpResponse, HttpResponseRedirect]: The HTTP response.
    """
    if not request.session.get('session_id'):
        return render(request, 'index.html')

    # load index of currently searching image from cookies
    found = int(request.COOKIES.get('index')) if request.COOKIES.get('index') is not None else 0
    if found >= len(targets):  # control of end
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

    return prepare_data(request, data, targets[found])


def start(request):
    """
    Sets the session id and renders the start.html template (welcome page).

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response containing the data to be displayed in the template.
    """
    # "login" - setting session id
    request.session['session_id'] = secrets.token_urlsafe(6)
    last_search[request.session['session_id']] = np.zeros(len(clip_data))
    return render(request, 'start.html')


def end(request):
    """
    Renders the end.html template (final page).

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response containing the data to be displayed in the template.
    """
    return render(request, 'end.html')
