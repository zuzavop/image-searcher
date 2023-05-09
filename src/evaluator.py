import csv
import os

import clip
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
from matplotlib import ticker


class Evaluator:
    """
    A class for evaluating models and visualizing results.

    Attributes:
        device (str): The device on which the model is loaded.
        model: The loaded model.
        preprocess: The preprocessing function of the loaded model.
        clip_data (list): A list of data extracted from images.
        same_video (dict): A dictionary mapping video names to their surrounding.
        last_search (dict): A dictionary mapping sessions to their last searched query.
        multi_search (dict): A dictionary mapping sessions to their last searched queries for multi model.
        min_search (dict): A dictionary mapping sessions to their last search query for min model.
    """

    def __init__(self, result_path, clip_path, showing=60, has_sur=True, surrounding=7,
                 sur_path="videos_end.txt"):
        """
        Initializes the Evaluator object.

        Args:
            result_path (str): Path to the directory where the results will be stored.
            clip_path (str): Path to the directory where the clip data will be loaded from.
            showing (int): The number of images to be shown in the result.
            has_sur (bool): Whether to use surrounding of images.
            surrounding (int): How much surrounding images to use.
            sur_path (str): Path to the file which define ends of each video.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.result_path = result_path
        self.showing = showing
        self.sur = surrounding

        self.clip_data = []
        self.same_video = {}
        self.last_search = {}
        self.multi_search = {}
        self.min_search = {}

        for fn in sorted(os.listdir(clip_path)):
            self.clip_data.append(torch.load(clip_path + f"/{fn}"))

        if has_sur:
            bottom = 0
            with open(sur_path, 'r') as f:
                for line in f:
                    top = int(line[:-1]) - 1
                    self.same_video.update(
                        {i: np.arange(max(bottom, i - self.sur), min(top, i + self.sur)) for i in range(bottom, top)})
                    bottom = top
        else:
            for i in range(len(self.clip_data)):
                self.same_video[i] = [i]

        self.logger = Logger(showing, self.same_video, self.result_path)

    def evaluate_data(self, log_path, reform_count=2, with_som=False, is_sea=False):
        """
        Evaluates the data from given log for each model define in project.

        Args:
            log_path (str): Path to the log file.
            reform_count (int): How many times the text query can be reformulated.
            with_som (bool): Whether the Self-Organizing Map is used for generating first screen.
            is_sea (bool): Whether the sea dataset is used.
        """
        query_count = 0

        with open(log_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line = 0
            prev_id = -1
            prev_session = ""
            count_same = 0

            for row in csv_reader:
                if line > 0:
                    ids = int(row[1])
                    session = row[2]
                    if prev_id != ids or prev_session != session:
                        query_count += 1
                        count_same = 1
                        self.last_search[session] = np.zeros(len(self.clip_data))
                        self.min_search[session] = np.full(len(self.clip_data), 2)
                        self.multi_search[session] = np.ones(len(self.clip_data))
                    else:
                        count_same += 1

                    if count_same <= reform_count:
                        self.get_data_from_text_search(row[0], session, ids, prev_id == ids, with_som, is_sea)

                    prev_id = ids
                    prev_session = session
                line += 1

        print("Total search: ", query_count)

    def get_data_from_text_search(self, query, session, found, is_second, with_som, is_sea):
        """
        Gets data for a current text search and log search for all models.

        Args:
            query (str): The text query used for search.
            session (str): The id of current session.
            found (int): The id of the image that was currently looking for.
            is_second (bool): Whether this is the second text query.
            with_som (bool): Whether the Self-Organizing Map is used for generating first screen.
            is_sea (bool): Whether the sea dataset is used.
        """
        # get features of text query
        with torch.no_grad():
            text_features = self.model.encode_text(clip.tokenize([query]).to(self.device))
        text_features /= np.linalg.norm(text_features)

        # get distance of vectors
        scores = (np.concatenate([1 - (torch.cat(self.clip_data) @ text_features.T)], axis=None))

        self.log_text_search_for_all_models(scores, query, session, found, is_second, with_som, is_sea)
        self.log_text_search_for_all_models(scores, query, session, found, is_second, with_som, is_sea, 0.25)
        self.log_text_search_for_all_models(scores, query, session, found, is_second, with_som, is_sea, 0.5)
        self.log_text_search_for_all_models(scores, query, session, found, is_second, with_som, is_sea, 0.75)

        self.last_search[session] = scores
        self.multi_search[session] = scores
        self.min_search[session] = scores

    def log_text_search_for_all_models(self, scores, query, session, found, is_second, with_som, is_sea, limit=1.0):
        """
        Logs the text search for all models.

        Args:
            scores (numpy.ndarray): The scores of the text search.
            query (str): The text query used for search.
            session (str): The id of current session.
            found (int): The id of the image that was currently looking for.
            is_second (bool): Whether this is the second text query.
            with_som (bool): Whether the Self-Organizing Map is used for generating first screen.
            is_sea (bool): Whether the sea dataset is used.
            limit (float): The percentage limit for dataset after first query.
        """
        indexes = np.arange(len(self.clip_data))

        if is_second:
            indexes = np.argsort(self.last_search[session])[:int(len(self.clip_data) * limit)]
            scores = scores[indexes]

        self.logger.log_down(self.get_log_name("basic", with_som, is_sea, limit), list(np.argsort(scores)), indexes,
                             query, session, found)
        self.logger.log_down(self.get_log_name("min", with_som, is_sea, limit),
                             list(np.argsort(np.min(np.array([scores, self.min_search[session]]), axis=0))), indexes,
                             query, session, found)
        self.logger.log_down(self.get_log_name("max", with_som, is_sea, limit),
                             list(np.argsort(np.max(np.array([scores, self.last_search[session]]), axis=0))), indexes,
                             query, session, found)
        self.logger.log_down(self.get_log_name("sum", with_som, is_sea, limit),
                             list(np.argsort(scores + self.last_search[session])), indexes, query, session, found)
        self.logger.log_down(self.get_log_name("multi", with_som, is_sea, limit),
                             list(np.argsort(scores * self.multi_search[session])), indexes, query, session, found)
        self.logger.log_down(self.get_log_name("avg", with_som, is_sea, limit),
                             list(np.argsort((2 * scores) + self.last_search[session])), indexes, query, session, found)

    @staticmethod
    def get_log_name(name, is_som, is_sea, limit=1.0):
        """
        Gets the name for the log.

        Args:
            name (str): The name of the model.
            is_som (bool): Whether the Self-Organizing Map is used for generating first screen.
            limit (float): The percentage limit for dataset after first query.
            is_sea (bool): Whether the sea dataset is used.

        Returns:
            str: The name for the log.
        """
        if is_sea:
            name = "sea_" + name
        if is_som:
            name += "_som"
        if limit < 1.0:
            name += "_limit_" + str(25 if limit == 0.25 else (50 if limit == 0.5 else 75))
        return name + ".csv"

    @staticmethod
    def get_data_from_log(log_path):
        """
        Method to extract data from a log file.

        Args:
            log_path (str): Path to the log file.

        Returns:
            A list containing the ranks for second query, ranks for first query, and difference values
            extracted from the log file.
        """
        ranks1 = []
        ranks2 = []
        with open(log_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line = 0

            previous_row = {}

            for row in csv_reader:
                if line > 0 and row[1] == previous_row[1] and row[2] == previous_row[2]:
                    ranks1.append(int(previous_row[3]))
                    ranks2.append(int(row[3]) if int(row[3]) > 0 else 22036)

                previous_row = row
                line += 1

        return [ranks2, ranks1]

    def get_data_for_graph(self, input_path, first_col_name):
        """
        Extracts data from multiple log files to be used for generating a plot.

        Args:
            input_path (str): Path to the directory containing the log files.
            first_col_name (str): Name of the first column in the generated plot.

        Returns:
            A tuple containing the data and column names to be used in generating the plot.
        """
        data = []
        columns = [first_col_name]

        x = 0
        for fn in sorted(os.listdir(input_path)):
            if x == 0:
                data = [self.get_data_from_log(fn)[1]]
            data = np.append(data, [self.get_data_from_log(fn)[0]], axis=0)
            columns.append(fn[:-4])
            x += 1

        return zip(data, columns)

    def get_violin_plot(self, input_path, output_file, first_col_name='1_not_found', use_log_scale=True):
        """
        Generates a violin plot of the data extracted from the log files.

        Args:
            input_path (str): Path to the directory containing the log files.
            output_file (str): Path to the output file to save the plot.
            first_col_name (str): Name of the first column in the generated plot.
            use_log_scale (bool): If plot has log scale.
        """
        data, columns_name = self.get_data_for_graph(input_path, first_col_name)

        if use_log_scale:
            data = [[np.log10(d) for d in row] for row in data]
        data = pd.DataFrame(np.array(data).T, columns=columns_name)

        fig, ax = plt.subplots(figsize=(16, 5))
        sns.set()
        sns.violinplot(data=data, bw=.02, ax=ax)

        if use_log_scale:
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
            ymin, ymax = ax.get_ylim()
            tick_range = np.arange(np.floor(ymin), ymax)
            ax.yaxis.set_ticks(tick_range)
            ax.yaxis.set_ticks([np.log10(x) for p in tick_range for x in np.linspace(10 ** p, 10 ** (p + 1), 10)],
                               minor=True)
            plt.tight_layout()

        plt.savefig(output_file)

    def get_points_plot(self, input_path, output_file, first_col_name='1_not_found', use_log_scale=True):
        """
        Generates a points plot of the data extracted from the log files.

        Args:
            input_path (str): Path to the directory containing the log files.
            output_file (str): Path to the output file to save the plot.
            first_col_name (str): Name of the first column in the generated plot.
            use_log_scale (bool): If plot has log scale.
        """
        data, columns_name = self.get_data_for_graph(input_path, first_col_name)
        data = pd.DataFrame(np.array(data).T, columns=columns_name)

        sns.set()
        sns.stripplot(data=data)
        if use_log_scale:
            plt.yscale('log')
        plt.savefig(output_file)

    def get_boxen_plot(self, input_path, output_file, first_col_name='1_not_found', use_log_scale=True):
        """
        Generates a boxen plot of the data extracted from the log files.

        Args:
            input_path (str): Path to the directory containing the log files.
            output_file (str): Path to the output file to save the plot.
            first_col_name (str): Name of the first column in the generated plot.
            use_log_scale (bool): If plot has log scale.
        """
        data, columns_name = self.get_data_for_graph(input_path, first_col_name)
        data = pd.DataFrame(np.array(data).T, columns=columns_name)

        sns.set()
        sns.boxenplot(data=data)
        if use_log_scale:
            plt.yscale('log')
        plt.savefig(output_file)

    def get_combine_plot(self, input_path, output_file, first_col_name='1_not_found', use_log_scale=True):
        """
        Generates a combine plot (violin plot combine with swarm plot) of the data extracted from the log files.

        Args:
            input_path (str): Path to the directory containing the log files.
            output_file (str): Path to the output file to save the plot.
            first_col_name (str): Name of the first column in the generated plot.
            use_log_scale (bool): If plot has log scale.
        """
        data, columns_name = self.get_data_for_graph(input_path, first_col_name)
        data = pd.DataFrame(np.array(data).T, columns=columns_name)

        sns.set()
        sns.catplot(data=data, kind="violin", color=".9", inner=None, cut=0, bw=.02)
        sns.swarmplot(data=data, size=1.5)
        if use_log_scale:
            plt.yscale('log')
        plt.savefig(output_file)


class Logger:
    def __init__(self, showing, same_video, result_path):
        """
        Initializes a Logger object.

        Args:
            showing (int): The number of images to be shown in the result.
            same_video (dict): A dictionary containing the indices surrounding image (surrounding in same video).
            result_path (str): The directory path where the log files will be saved.
        """
        self.showing = showing
        self.same_video = same_video
        self.result_path = result_path + "\\model_results\\"
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

    def log_down(self, log_filename, new_scores, indexes, query, session, found):
        """
        Writes the result of a query to a log file.

        Args:
            log_filename (str): The name of the log file.
            new_scores (list): A list of indices of images sorted by similarity to the current query.
            indexes (list): A list of indices of all images in the dataset that are currently used.
            query (str): The text of the query.
            session (str): The id of the user session.
            found (int): The index of the image that was currently looking for.
        """
        with open(self.result_path + log_filename, "a") as log:
            # if searching image is present in context (surrounding of image) of any image in shown result same is equal 1
            same = self.is_in_same_video(indexes[new_scores[:self.showing]], found)
            first = self.get_rank(new_scores, np.where(indexes == found)[0][0])
            for i in list(set(indexes).intersection(set(self.same_video[found]))):
                first = min(first, self.get_rank(new_scores, np.where(indexes == i)[0][0]))

            log.write(f'"{query}";{found};{session};' + str(self.get_rank(new_scores, np.where(indexes == found)[0][
                0]) if found in indexes else -1) + ';{same};{first}')

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
        # if searching image is present in context (surrounding of image) of any image in shown result same is equal 1
        return 1 if len(list(set(new_showing) & set(self.same_video[target]))) > 0 else 0

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


evaluator = Evaluator(".//", "..//gasearcher//static//data//clip", 60, True, 2,
                      "..//gasearcher//static//data//videos_end.txt")
evaluator.evaluate_data("..//gasearcher//static//data//log.csv")