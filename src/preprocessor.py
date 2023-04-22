import os

from images_to_clip import get_vector_from_photo
from parse_video import parse_video
from top_classes import classify_images


class Preprocessor:
    def __init__(self, videos_path, result_path):
        """
        Initializes a Preprocessor.

        Args:
            videos_path (str): The path to the directory containing the videos to be parsed.
            result_path (str): The path to the directory where the results will be saved.
        """
        self.videos_path = videos_path
        self.result_path = result_path
        self.photos_path = result_path + "\\photos\\"
        self.vectors_path = result_path + "\\clip\\"

    def parse_videos(self, input_path, enable_logging, log_path="videos.txt"):
        """
        Recursively parses a directory of videos and extracts frames from them.

        Args:
            input_path (str): The path to the directory containing the videos to be parsed.
            enable_logging (bool): A flag indicating whether logging is enabled or not.
            log_path (str): The path to the log file where information about end of each video will be written.
        """
        for filename in os.listdir(input_path):
            if os.path.isdir(filename):
                self.parse_videos(input_path + "\\" + filename, enable_logging, log_path)
            else:
                parse_video(input_path + "\\" + filename, self.photos_path, enable_logging, log_path)

    def images_to_vectors(self):
        """
        Converts images to vectors using CLIP.
        """
        for photo in os.listdir(self.photos_path):
            get_vector_from_photo(self.photos_path + photo, photo[:-4], self.vectors_path)

    def classify_images(self, nounlist_path, result_file):
        """
        Classifies images using a CLIP model and saves the results to a file.

        Args:
            nounlist_path (str): The path to the noun list file used for classification.
            result_file (str): The path to the file where the classification results will be saved.
        """
        classify_images(self.vectors_path, nounlist_path, result_file)
        self.get_class_pr(result_file)

    def get_class_pr(self, result_path):
        print(self.result_path)

    @staticmethod
    def rename_images(images_path, name_format='{:05d}'):
        """
        Renames images in a directory to a specified format.

        Args:
            images_path (str): The path to the directory containing the images to be renamed.
            name_format (str): The format string to use for the new image names. Default is '{:05d}'.
        """
        i = 1
        for file in os.listdir(images_path):
            os.rename(images_path + "//" + file, images_path + "//" + name_format.format(i) + ".jpg")
            i += 1

    def preprocess_dataset(self, videos_path, nounlist_path):
        """
        Preprocesses a dataset by parsing the videos, extracting frames, converting them to vectors,
        classifying the vectors, and saving the results to a file.

        Args:
            videos_path (str): The path to the directory containing the videos to be parsed.
            nounlist_path (str): The path to the noun list file used for classification.
        """
        self.parse_videos(videos_path, True, self.result_path + "videos.txt")
        self.rename_images(self.result_path)
        self.images_to_vectors()
        self.classify_images(nounlist_path, self.result_path + "result.csv")
