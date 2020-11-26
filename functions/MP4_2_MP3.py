import os
import glob
from pydub import AudioSegment
import pydub

video_dir = 'C:/Users/ED/Desktop/新建文件夹/'  # 你保存有视频的文件夹路径
extension_list = ('*.mp4', '*.flv')

os.chdir(video_dir)
for file_dir_generate in os.walk("./", topdown=True):
    for video_name in file_dir_generate[2]:
        file_dict={
            "video_dir": file_dir_generate[0] +"/"+video_name,
            "export_dir":file_dir_generate[0] +"/"+video_name.replace(".mp4",".mp3"),
        }
        AudioSegment.from_file(file_dict["video_dir"]).export(file_dict["export_dir"], format='mp3')