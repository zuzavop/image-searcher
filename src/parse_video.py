import os
import glob
import sys

output_path = "F://sea_photos"
logging_enable = True
log_path = "F://videos.txt"
photo_path = "F://sea_dataset"


def latest_index():
    list_of_files = glob.glob(output_path + "//*")
    if list_of_files == []:
        return 1
    latest_file = max(list_of_files, key=os.path.getctime).split('\\')[-1]
    latest_index = int(latest_file[:-4]) + 1
    if logging_enable:
        with open(log_path, "a") as log:
            log.write(latest_index)
    return latest_index


def get_comm(folder_path):
    index = latest_index()
    comm = 'ffmpeg -i {0} -vf "fps=0.5,scale=-1:224" -start_number {1} {2}'.format(folder_path, index, output_path + "//%9d.jpg")
    print(folder_path)
    return comm


for folder in os.listdir(photo_path):
    folder_path = photo_path + "//" + folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".MP4"):
            os.system(get_comm(folder_path))
