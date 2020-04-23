import cv2
import glob
import os
import pdb 
 
def get_video_info(video_path):

    videoCapture = cv2.VideoCapture()
    videoCapture.open(video_path)
    # 帧率
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    # 尺寸 (分辨率)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # (width, height)
    # 总帧数
    total_frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    # 时长
    rate = videoCapture.get(5)
    total_duration = total_frames/rate
    print("fps=", int(fps), "size=", size, "total_frames=", int(total_frames), "rate=", rate, "total_duration=", total_duration)
    
    return fps, size, total_frames, rate, total_duration


def frames_to_video(frames_path, fps, size, start_index, end_index, save_path):  
    """
    [start_index, end_index]
    """
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')  #  'xxx.avi'
    videoWriter = cv2.VideoWriter(save_path, fourcc, fps, size)  # size 不匹配，将导致生成的文件损坏（无法打开）
    for i in range(start_index, end_index+1):
        if os.path.isfile("%s/%d.jpg"%(frames_path, i)):
            frame = cv2.imread("%s/%d.jpg"%(frames_path, i))
            # print("%s/%d.jpg"%(frames_path, i))
            # print(frame.shape)
            videoWriter.write(frame)
    videoWriter.release()
    return
 

if __name__ == '__main__':

    video_file = "00004_result_part.mp4"
    result_file = video_file.split('.')[0] + '_cut.mp4'
    frames_dir = 'frames'

    fps, size, total_frames, rate, total_duration = get_video_info(video_file)
    # frames → video
    frames_to_video(frames_path=frames_dir, fps=fps, size=size, start_index=415, end_index=482, save_path=result_file)
    print("frames → video SUCCEED !!!")