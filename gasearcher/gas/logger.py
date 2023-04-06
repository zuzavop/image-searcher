import numpy as np
class Logger:
    """
    Log text and image queries.

    Attributes:
        path_log_search (str): The path of the log file for text queries.
        path_log (str): The path of the log file for image queries.
        showing (int): The number of images to show in the query result.
        same_video (dict): A dictionary containing the limit indices bounding images context (surrounding in same video).
    """
    def __init__(self, path_data, showing, same_video):
        """
        Args:
            path_data (str): The path to data.
            showing (int): The number of images to show in the query result.
            same_video (dict): A dictionary containing the limit indices bounding images context (surrounding in same video).
        """
        self.path_log_search = path_data + "sea_log.csv"
        self.path_log = path_data + "v3c_log.csv"
        self.showing = showing
        self.same_video = same_video  # indexes of images in same video (high probability of same looking photos)

    def log_text_query(self, query, new_scores, target, session, activity):
        """
        Logs a text query.

        Args:
            query (str): The query text.
            new_scores (list): A list of indices of images sorted by similarity to the current text query.
            target (int): The index of the currently searching image.
            session (str): The unique session ID of the user.
            activity (str): The activity from the user.
        """
        same = self.is_in_same_video(new_scores[:self.showing], target)
        # write down log
        with open(self.path_log_search, "a") as log:
            log.write(query + ';' + str(target) + ';' + session + ';' + str(self.get_rank(new_scores, target))
                      + ';' + str(same) + ';"' + activity + '"' + '\n')

    def log_image_query(self, query_id, new_scores, target, session):
        """
        Logs an image query.

        Args:
            query_id (int): The query image ID.
            new_scores (list): A list of indices of images sorted by similarity to the current image query.
            target (int): The index of the currently searching image.
            session (str): The unique session ID of the user.
        """
        same = self.is_in_same_video(new_scores[:self.showing], target)
        # write down log
        with open(self.path_log, "a") as log:
            log.write(str(query_id) + ';' + str(target) + ';' + session + ';' + str(self.get_rank(new_scores, target))
                      + ';' + str(same) + '"' + '\n')

    def is_in_same_video(self, new_showing, target):
        """
        Determines if the searched image and its surrounding is present in the shown result.

        Args:
            new_showing (list): A list of indices of images to be shown in the query result.
            target (int): The index of the currently searching image.

        Returns:
            int: If the searched image is present in the context of any image in the shown result, returns 1.
            Otherwise, returns 0.
        """
        surrounding = np.arange(self.same_video[target][0], self.same_video[target][1] + 1)
        # if searching image is present in context (surrounding of image) of any image in shown result same is equal 1
        return 1 if len(list(set(new_showing) & set(surrounding))) > 0 else 0

    @staticmethod
    def get_rank(scores, index):
        """
        Get rank (from 1) of image.

        Args:
            scores (list): A list of indices of images sorted by similarity to the current query
            index (int): The index of the image

        Returns:
            int: The rank of given image
        """
        return scores.index(index) + 1
