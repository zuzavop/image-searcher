import glob
import os


def get_latest_index(output_path):
    list_of_files = glob.glob(output_path + "//*")
    if not list_of_files:
        return 1
    latest_file = max(list_of_files, key=os.path.getctime).split('\\')[-1]
    return int(latest_file[:-4]) + 1


def get_comm(video_path, output_path, start_index):
    comm = 'ffmpeg -i {0} -vf "fps=0.5,scale=-1:224" -start_number {1} {2}'.format(video_path, start_index, output_path + "//%9d.jpg")
    print(video_path)
    return comm


def parse_video(video_path, output_path, logging_enable, log_path=""):
    if video_path.endswith(".mp4") or video_path.endswith(".MP4"):
        start_index = get_latest_index(output_path)
        if logging_enable:
            with open(log_path, "a") as log:
                log.write(str(start_index))
        os.system(get_comm(video_path, output_path, start_index))
