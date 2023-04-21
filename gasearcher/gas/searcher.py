import clip
import numpy as np
import torch


class Searcher:
    """

    Attributes:
        clip_data (list):
        combination (bool):
        logger (Logger):
        showing (int):
        last_search (dict):
        device:
        model:
    """

    def __init__(self, clip_data, combination, logger, showing):
        """
        Args:
            clip_data (list):
            combination (bool):
            logger (Logger):
            showing (int):
        """
        self.clip_data = clip_data
        self.combination = combination
        self.last_search = {}  # vectors of last text search
        self.logger = logger
        self.showing = showing
        # clip
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, preprocess = clip.load("ViT-B/32", device=self.device)

    def result_score(self, features):
        """
        Calculate the similarity distance of the query feature vector to the CLIP data (normalize feature vectors of images).

        Args:
            features (numpy.ndarray): A 2D array representing the normalize feature vector of the query.

        Returns:
            numpy.ndarray: A 1D array representing the similarity distance (from 0 to 2) of each image to the query.
        """
        return np.concatenate([1 - (torch.cat(self.clip_data) @ features)], axis=None)

    def text_search(self, query, session, found, activity):
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
            text_features = self.model.encode_text(clip.tokenize([query]).to(self.device))
        text_features /= np.linalg.norm(text_features)

        # get distance of vectors
        scores = self.result_score(text_features.T)

        new_scores = list(np.argsort((scores + self.last_search[session]) if self.combination else scores))
        # save score for next search
        if self.combination:
            self.last_search[session] = scores

        self.logger.log_text_query(query, new_scores, found, session, activity)

        return new_scores[:self.showing]

    def image_search(self, image_query, found, session):
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
        image_query = np.transpose(self.clip_data[image_query_index])

        scores = list(np.argsort(self.result_score(image_query)))

        self.logger.log_image_query(image_query, scores, found, session)

        return scores[:self.showing]

    def reset_last(self, session):
        """
        Reset scores of last search for user of given session.

        Args:
            session (str): The session.
        """
        self.last_search[session] = np.zeros(len(self.clip_data))
