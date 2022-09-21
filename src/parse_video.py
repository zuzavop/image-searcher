import os
import glob
import sys


def latest_index():
    list_of_files = glob.glob('F://sea_photos//*')
    if list_of_files == []:
        return 1
    latest_file = max(list_of_files, key=os.path.getctime).split('\\')[-1]
    latest_index = int(latest_file[:-4]) + 1
    old_stdout = sys.stdout
    log_file = open("F://videos.txt", "a")
    sys.stdout = log_file
    print(latest_index)
    sys.stdout = old_stdout
    log_file.close()
    return latest_index


def get_comm():
    index = latest_index()
    comm = 'ffmpeg -i {0} -vf "fps=0.5,scale=-1:224" -start_number {1} F://sea_photos//%9d.jpg'.format(path + "//" + folder,index) ##.format(folder_path + "//" + filename, index)
    print(comm)
    return comm


paths = "F://sea_dataset"

for folder in os.listdir(path):
    folder_path = path + "//" + folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".MP4"):
            os.system(get_comm())
