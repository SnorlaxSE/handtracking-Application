from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
import qdarkstyle
import sys
import time
 
from utils import detector_utils as detector_utils
import tensorflow as tf
import datetime
import argparse
import numpy as np
import cv2
import os
import pdb 

from postProcess.new_cut_start_end_video import *


 
detection_graph, sess = detector_utils.load_inference_graph()

class VideoBox(QWidget):
    
    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    def __init__(self, video_url="", cutVideoDir="", crop=False, fps=25):

        super(VideoBox, self).__init__()
        # self.frame = []  # 存图片
        self.playCaptureState = False
        self.video_url = video_url
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause
        self.crop=crop  # 如果视频中放下的手仍出现在视野中，crop=True
        self.fps = fps
        self.playCapture = cv2.VideoCapture()

        self.scores_list = []
        self.scoresList = []  # save scores_list like Container, prevent from PlayReset() 重置 scores_list
        self.num_frames = 0
        self.srcVideo = ""
        self.cutVideoDir = cutVideoDir

        self.start_time = datetime.datetime.now()

        # self.fps, size, total_frames, rate, total_duration = get_video_info(self.video_url)
        # self.im_width, self.im_height = size[0], size[1]

        # max number of hands we want to detect/track
        self.num_hands_detect = 2

        # 窗口框
        self.resize(1080, 650)
        self.setFixedSize(1080, 650)
        self.setWindowTitle("Hand Detection")

        # 帧label
        self.frameLabel = QLabel(self)
        self.frameLabel.setFixedSize(720, 540)  # width height
        # self.frameLabel.move(10, 10)
        self.init_image = QPixmap("src/cat.jpeg").scaled(self.frameLabel.width(), self.frameLabel.height())
        self.frameLabel.setPixmap(self.init_image)

        # 状态label
        self.stateTextEdit = QTextEdit(self)
        self.stateTextEdit.setText("Waiting for detectiong...")
        self.stateTextEdit.setAlignment(Qt.AlignLeft)
        self.stateTextEdit.setFixedSize(300, 600)  # width height
        # self.stateTextEdit.move(50, 500)
        self.stateTextEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stateTextEdit.moveCursor(QTextCursor.End)

        # 开启视频按键
        self.playButton = QPushButton(self)
        self.playButton.setText("Open")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.playButton.move(100, 570)
        self.playButton.clicked.connect(self.slotStart)

        # 暂停视频按钮
        self.pauseButton = QPushButton(self)
        self.pauseButton.setText("Pause")
        self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        # self.pauseButton.move(300, 570)
        self.pauseButton.setEnabled(False)
        self.pauseButton.clicked.connect(self.slotPause)
 
        # 停止视频按钮
        self.stopButton = QPushButton(self)
        self.stopButton.setText("Stop")
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        # self.stopButton.move(500, 570)
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.slotStop)

        # 裁剪按钮
        self.cutButton = QPushButton(self)
        self.cutButton.setText("Cut")
        self.cutButton.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        # self.cutButton.move(700, 570)
        self.cutButton.setEnabled(False)
        self.cutButton.clicked.connect(self.slotCut)

        frameBox = QVBoxLayout()
        frameBox.addStretch()
        frameBox.addWidget(self.frameLabel)
        frameBox.addStretch()

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.pauseButton)
        controlBox.addWidget(self.stopButton)
        controlBox.addWidget(self.cutButton)

        ViewBox = QVBoxLayout()
        ViewBox.addLayout(frameBox)
        ViewBox.addLayout(controlBox)

        layout = QHBoxLayout()
        layout.addLayout(ViewBox)
        layout.addWidget(self.stateTextEdit)

        self.setLayout(layout)

        # timer 设置
        self.timer = QTimer()     #定义定时器


    def slotStart(self):
        """ 
        Slot function to start the progamme
        """
        if self.video_url == "":
            info = QMessageBox.information(self,'information', 'Choose a video to show.', QMessageBox.Yes | QMessageBox.Yes)
            self.video_url, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.MTS;;*.mp4;;*.avi;;All Files(*)")

        if self.video_url != "" and os.path.isfile(self.video_url):  # “”为用户取消

            # reset something
            self.stateTextEdit.setText("Waiting for detectiong...")
            self.status = VideoBox.STATUS_INIT

            self.playCapture.open(self.video_url)
            self.timer.start(1000/self.fps)  # 单位是毫秒，这点要注意,相当于时间每过xxx ms，timer的timeout()就会被触发一次
            self.timer.timeout.connect(self.showFrame)
            self.playCaptureState = True
            self.pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)

            # reset something   （预防 pause 后 click 'open'）
            if self.scores_list != []:
                self.scoresList = self.scores_list
            self.scores_list = []  
            self.num_frames = 0
            self.start_time = datetime.datetime.now()
            self.cutButton.setEnabled(False)

 
    def slotPause(self):
        
        if self.status is VideoBox.STATUS_PAUSE or self.status is VideoBox.STATUS_INIT:
            # want to pause
            self.timer.stop()
        elif self.status is VideoBox.STATUS_PLAYING:
            # want to play
            self.timer.start(1000/self.fps)
        
        if not self.video_url == '':  # 避免多次无效click 'open', 将self.video_url重置
            self.srcVideo = self.video_url  # 避免self.video_url重置后，无法 cut

        self.video_url = ""  # make sure 暂停状态 click 'open' 无异常

        self.status = (VideoBox.STATUS_PLAYING,
                       VideoBox.STATUS_PAUSE,
                       VideoBox.STATUS_PLAYING)[self.status]

    def slotStop(self):
        """ 
        Slot function to stop the programme
        """
        if self.playCaptureState:
            self.stateTextEdit.append("This video detection has been stopped.")
            self.playReset()
            QMessageBox.information(self,'information',"This video detection has been stopped.", QMessageBox.Yes |  QMessageBox.Yes)
            
        else:
            self.stateTextEdit.append("Please choose a video to show.")
            Warming = QMessageBox.warning(self, "Warming", "Please choose a video to show.",QMessageBox.Yes)


    def playReset(self):

        """
        仅 click 'stop' 、 play complete 调用
        """
        
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoBox.STATUS_INIT
        
        if self.video_url != '':  # 避免多次无效click 'open', 将self.video_url重置
            self.srcVideo = self.video_url  # 避免self.video_url重置后，无法 cut

        self.video_url = ""  #  make sure 暂停状态 click 'open' 无异常

        if self.scores_list != []:
            self.scoresList = self.scores_list

        self.scores_list = []
        self.playCaptureState = False
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.cutButton.setEnabled(True)
        self.cutVideoDir = ""


    def slotCut(self):
        """ 
        Slot function to cut the programme

        only call when click 'stop' or play complete 
        """

        if self.scoresList == []:
            QMessageBox.information(self,'information',"Detection Uncompleted.", QMessageBox.Yes | QMessageBox.Yes)
            return

        if self.cutVideoDir == '':
            info = QMessageBox.information(self,'information',"Choose Output Folder.", QMessageBox.Yes | QMessageBox.Yes)
            self.cutVideoDir = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./") 
            if self.cutVideoDir == '':
                print("self.cutVideoDir == '': ", self.cutVideoDir == '')
                return

        print("self.cutVideoDir: ", self.cutVideoDir)

        if not os.path.exists(self.cutVideoDir):
            os.makedirs(self.cutVideoDir)

        video_name = self.srcVideo.split('/')[-1]
        outputDir = self.cutVideoDir.split('/')[-1]
        
        self.frameLabel.setPixmap(self.init_image)
        self.playButton.setText("Wait")
        self.playButton.setEnabled(False)
        self.pauseButton.setText("for")
        self.pauseButton.setEnabled(False)
        self.stopButton.setText("cutting")
        self.stopButton.setEnabled(False)
        self.cutButton.setText("...")
        self.cutButton.setEnabled(False)

        self.stateTextEdit.append("Now start to cut the video \n'{}'".format(video_name)) 
        QMessageBox.information(self, "information", "Now start to cut the video  {}. And the Outputs would save at '{}' Folder.".format(video_name, outputDir), QMessageBox.Yes)


        prediction_structure_list = []
        for frame_info_dict in self.scoresList:
            for (frame_value, frame_info_value_dict) in frame_info_dict.items():
                if frame_info_value_dict['scores'] != []:
                    prediction_structure_list.append(frame_info_dict)
                    continue

        frame_list = []
        for frame_info_dict in prediction_structure_list:
            for (frame_value, _) in frame_info_dict.items():
                frame_list.append(frame_value)
        print("len(prediction_structure_list): ", len(prediction_structure_list))
        print("len(frame_list): ", len(frame_list))

        fps, size, total_frames, rate, total_duration = get_video_info(self.srcVideo)  # size: (width, height)

        normal_frame_gap_threshold = 1 * fps  # 正常动作间隔
        short_frame_gap_threshold = 0.5 * fps  # 较短动作间隔
        post_frame_gap_threshold = 0.6 * fps
        post_action_frame_threshold = 3.5 * fps
            
        start_frame_list, end_frame_list, frame_gap_list, duration_list = pick_predict_frame_sections(prediction_structure_list, frame_list, normal_frame_gap_threshold, short_frame_gap_threshold, self.im_width, self.im_height, blackBorder=False)
        print('*'*10)
        adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list = adaptive_frame_sections(start_frame_list, end_frame_list, frame_gap_list, duration_list, normal_frame_gap_threshold, total_frames, fps)
        print('**'*10)
        post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list = post_adapt(prediction_structure_list, adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list, post_frame_gap_threshold, post_action_frame_threshold, fps)
        print('***'*10)
        cut_video(self.srcVideo, self.cutVideoDir, post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list, fps, self.stateTextEdit)

        self.playButton.setText("Open")
        self.playButton.setEnabled(True)
        self.pauseButton.setText("Pause")
        self.pauseButton.setEnabled(False)
        self.stopButton.setText("Stop")
        self.stopButton.setEnabled(False)
        self.cutButton.setText("Cut")
        self.cutButton.setEnabled(False)

        self.stateTextEdit.append("Completed.") 
        QMessageBox.information(self, "information", "Completed.", QMessageBox.Yes)
        self.cutButton.setEnabled(False)

        pass

    def showFrame(self):
        """ 
        Slot function to capture frame and process it
        """

        if self.playCapture.isOpened():
            ret, frame = self.playCapture.read()
            if ret:

                # crop frame
                print("frame: ", frame.shape)
                if self.crop:
                    frame = frame[:int(frame.shape[0]*0.88),:,:] # (height, width, bytesPerComponent)
                    print("frame: ", frame.shape, type(frame))

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                boxes, scores = detector_utils.detect_objects(frame, detection_graph, sess)

                # Calculate Frames per second (FPS)
                self.num_frames += 1
                elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
                # fps = self.num_frames / elapsed_time

                score_index = np.where(scores>=args.score_thresh)
                self.scores_list.append({self.num_frames:{'scores':list(scores[scores>=args.score_thresh]), 'boxes':list(boxes[score_index]) } })

                height, width, bytesPerComponent = frame.shape
                self.im_height, self.im_width = height, width   # update crop size 
                bytesPerLine = bytesPerComponent * width

                # print(frame.data,  width, height, bytesPerLine, QImage.Format_RGB888)
                q_image = QImage(frame.data,  width, height, bytesPerLine,
                                QImage.Format_RGB888).scaled(self.frameLabel.width(), self.frameLabel.height())

                # q_image = QImage(frame.data,  width, height, bytesPerLine, QImage.Format_RGB888)
                self.frameLabel.setPixmap(QPixmap.fromImage(q_image))
                
                print("frames processed: ", self.num_frames, "elapsed time: ", elapsed_time, " scores: ", scores[score_index])  # (100,)
                score =  str(scores[score_index][:2])[1:-1]
                if score == '':
                    score = "0"
                self.stateTextEdit.append("frame: {}  scores: {}".format( self.num_frames, score))  # (100,)
                self.stateTextEdit.moveCursor(QTextCursor.End)
                # pdb.set_trace()

            else:
                # 判断本地文件播放完毕
                self.stateTextEdit.append("Completed.")
                QMessageBox.information(self,'information',"Completed.", QMessageBox.Yes | QMessageBox.Yes)
                self.playReset()

                return 

        else:
            self.stateTextEdit.append("open file or capturing device error, try again.")
            # Warming = QMessageBox.warning(self, "Warming", "open file or capturing device error, try again.", QMessageBox.Yes)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-sth',
        '--scorethreshold',
        dest='score_thresh',
        type=float,
        default=0.2,
        help='Score threshold for displaying bounding boxes')
    parser.add_argument(
        '-fps',
        '--fps',
        dest='fps',
        type=int,
        default=1,
        help='Show FPS on detection/display visualization')
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        default="",
        help='Device index of the camera.')
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=720,
        help='Width of the frames in the video stream.')
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=540,
        help='Height of the frames in the video stream.')
    parser.add_argument(
        '-ds',
        '--display',
        dest='display',
        type=int,
        default=1,
        help='Display the detected images using OpenCV. This reduces FPS')
    parser.add_argument(
        '-num-w',
        '--num-workers',
        dest='num_workers',
        type=int,
        default=4,
        help='Number of workers.')
    parser.add_argument(
        '-q-size',
        '--queue-size',
        dest='queue_size',
        type=int,
        default=5,
        help='Size of the queue.')
    args = parser.parse_args()


    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # my = VideoBox(video_url="/Users/snorlaxse/Documents/Github/handtracking/src/00005_h264_cut_32.mp4", cutVideoDir="VideoOutputs")
    my = VideoBox(video_url="", cutVideoDir="")
    my.show()
    sys.exit(app.exec_())