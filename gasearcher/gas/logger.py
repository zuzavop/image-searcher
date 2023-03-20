class Logger:
    """
    Log text and image queries.

    Attributes:
        path_log_search (str): The path of the log file for text queries.
        path_log (str): The path of the log file for image queries.
        showing (int): The number of images to show in the query result.
        finding (dict): A dictionary containing the indexes of all images.
        same_video (dict): A dictionary containing the indexes of images in the same video.
    """
    def __init__(self, path_data, showing, finding, same_video):
        """
        Args:
            path_data (str): The path to data.
            showing (int): The number of images to show in the query result.
            finding (dict): A dictionary containing the indexes of all images.
            same_video (dict): A dictionary containing the indexes of images in the same video.
        """
        self.path_log_search = path_data + "sea_log.csv"
        self.path_log = path_data + "v3c_log.csv"
        self.showing = showing
        self.finding = finding
        self.same_video = same_video  # indexes of images in same video (high probability of same looking photos)

    def log_text_query(self, query, new_scores, found, session, activity):
        """
        Logs a text query.

        Args:
            query (str): The query text.
            new_scores (list): A list of scores for the searched images.
            found (int): The index of the currently searching image.
            session (str): The unique session ID of the user.
            activity (str): The activity from the user.
        """
        same = self.is_in_same_video(new_scores[:self.showing], found)
        # write down log
        with open(self.path_log_search, "a") as log:
            log.write(query + ';' + str(self.finding[found]) + ';' + session + ';' + str(
                new_scores.index(self.finding[found]) + 1) + ';' + str(same) + ';"' + activity + '"' + '\n')

    def log_image_query(self, query_id, new_scores, found, session):
        """
        Logs an image query.

        Args:
            query_id (int): The query image ID.
            new_scores (list): A list of scores for the searched images.
            found (int): The index of the currently searching image.
            session (str): The unique session ID of the user.
        """
        same = self.is_in_same_video(new_scores[:self.showing], found)
        # write down log
        with open(self.path_log, "a") as log:
            log.write(str(query_id) + ';' + str(self.finding[found]) + ';' + session + ';' + str(
                new_scores.index(self.finding[found]) + 1) + ';' + str(same) + '"' + '\n')

    def is_in_same_video(self, new_showing, found):
        """
        Determines if the searched image is present in the context of any image in the shown result.

        Args:
            new_showing (list): A list of indexes of images to be shown in the query result.
            found (int): The index of the currently searching image.

        Returns:
            int: If the searched image is present in the context of any image in the shown result, returns 1. Otherwise, returns 0.
        """
        # if searching image is present in context (surrounding of image) of any image in shown result same is equal 1
        return 1 if len(list(set(new_showing) & set(self.same_video[self.finding[found]]))) > 0 else 0
