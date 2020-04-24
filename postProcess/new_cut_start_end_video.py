from postProcess.cut_video_function import *
import copy


def pick_predict_frame_sections(prediction_structure_list, frame_list, normal_frame_gap_threshold, short_frame_gap_threshold, im_width, im_height, blackBorder=False):

    frame_gap = 0
    last_frame = 0  
    start_frame_list = []
    end_frame_list = []
    frame_gap_list = []
    location_ratio_flag = True

    for i, frame_info_dict in enumerate(prediction_structure_list):
        """
        frame_info_dict: 
        ex. {58: {'scores': [0.30838698], 'boxes': [[0.90856266, 0.32726675, 1.0, 0.47203618]]}}
            {58: [{'scores': [0.30838698]}, {'boxes': [[0.90856266, 0.32726675, 1.0, 0.47203618]]}]}
        ex. {168: {'scores': [0.6841056, 0.6657858], 'boxes': [[0.3419823, 0.47440776, 0.502142, 0.55743474], [0.48269054, 0.65848, 0.64012533, 0.72797984]]}}
            {168: [{'scores': [0.6841056, 0.6657858]}, {'boxes': [[0.3419823, 0.47440776, 0.502142, 0.55743474], [0.48269054, 0.65848, 0.64012533, 0.72797984]]}]}
 
        frame_list:
        [58, 59, 64, 65, 66, 69, 70, 72, ..., 1789, 1791, 1792, 1793]
        """
        print("----- {} -----".format(i))
        for (frame_value, frame_info_value_dict) in frame_info_dict.items():
            
            # scores_list = frame_info_value_dict['scores']
            boxes_lists = frame_info_value_dict['boxes']
            # print("frame_value: ", frame_value)
            # print("score_list: ", scores_list)
            # print("boxes_lists: ", boxes_lists)

            current_frame = frame_value
            # print("current_frame: ", current_frame)
            frame_gap = float(current_frame) - float(last_frame)
            print("current_frame -- frame_gap: {} -- {}".format(current_frame, frame_gap))

            bbox_y = im_height  

            for boxes_list in boxes_lists:
                # ex. [[0.12900555, 0.7695243, 0.24960786, 0.85627383], [0.34959477, 0.7613315, 0.46716428, 0.8410577]]
                (left, right, top, bottom) = (boxes_list[1] * im_width, boxes_list[3] * im_width,
                                          boxes_list[0] * im_height, boxes_list[2] * im_height)
            
                box_center = ((left+right)/2, (top+bottom)/2)
                # print("(left, right, top, bottom): ", (left, right, top, bottom))
                # print("box_center: ", box_center)

                bbox_y = min(box_center[1], float(bbox_y))  # 取位置高的"hand"
            # print("high bbox_y: ", bbox_y)

            location_ratio = float(bbox_y)/float(im_height) 
            # pdb.set_trace()

        if not blackBorder:
            endpoint_ratio_threshold = 0.85
        else:
            endpoint_ratio_threshold = 0.65  # To be determined

        if location_ratio <= endpoint_ratio_threshold:
            if frame_gap > short_frame_gap_threshold and i != len(prediction_structure_list) -1:
                next_frame = frame_list[i+1]
                next_frame_gap = float(next_frame) - float(current_frame)
                if next_frame_gap > short_frame_gap_threshold:
                    # 某一帧 与其相邻两帧间隔皆大于0.5s，且位于帧图像上部，该帧视作”误判“帧
                    # print(current_frame, next_frame, next_frame_gap)
                    print('---', '误判')
                    continue
            print("The upper part frame.")
            location_ratio_flag = False  # 帧图像 顶部

        last_frame = current_frame

        if location_ratio > endpoint_ratio_threshold:
            if location_ratio_flag and frame_gap > short_frame_gap_threshold:
                # 此帧与上一帧 皆为”起手式“/”落手式“ ，且间隔0.5s以上 可判定为间隔 
                # 解决动作间隔短的问题
                # 缺点：造成 a - a (start-end)
                # pdb.set_trace()
                if start_frame_list == []:
                    start_frame_list.append(frame_list[i])
                    continue
                if i == 0:
                    continue
                end_frame_list.append(frame_list[i-1])
                start_frame_list.append(frame_list[i])
                frame_gap_list.append(frame_gap)
                print('---', '细间断')
                # pdb.set_trace()
                continue
            print("The bottom part frame.")
            location_ratio_flag = True  # 帧图像 底部

        if i == 0:  
            start_frame_list.append(current_frame)
            print("{} as start frame.".format(current_frame))
            continue
            
        if i == len(prediction_structure_list) -1 :
            end_frame_list.append(current_frame)
            print('>'*5)
            print("{} as end frame.".format(current_frame))
            continue

        if frame_gap > normal_frame_gap_threshold:
            end_frame_list.append(frame_list[i-1])
            start_frame_list.append(frame_list[i])
            frame_gap_list.append(frame_gap)
            pass
        
        print('-'*10)

    duration_list = []
    for i in range(len(start_frame_list)):
        print("({}) {} {} {}".format(i+1, start_frame_list[i], end_frame_list[i], float(end_frame_list[i]) - float(start_frame_list[i])))
        if float(end_frame_list[i]) - float(start_frame_list[i]) == 0:
            print('-'*10, '0')
        duration_list.append(float(end_frame_list[i]) - float(start_frame_list[i]))

    # print("len(start_frame_list):", len(start_frame_list))  # 20 
    # print("len(end_frame_list):", len(end_frame_list))  # 20 
    # print("len(frame_gap_list):", len(frame_gap_list)) # 19
    # print("len(duration_list):", len(duration_list))  # 20

    return start_frame_list, end_frame_list, frame_gap_list, duration_list


def adaptive_frame_sections(start_frame_list, end_frame_list, frame_gap_list, duration_list, normal_frame_gap_threshold, total_frames, fps):

    adaptive_start_frame_list = []
    adaptive_end_frame_list = []

    global_start_frame = start_frame_list[0]
    adaptive_global_start_frame = float(global_start_frame) - normal_frame_gap_threshold
    # print(adaptive_global_start_frame)
    adaptive_global_start_frame = max(adaptive_global_start_frame, 0)
    adaptive_start_frame_list.append(adaptive_global_start_frame)

    for i, section_start_frame in enumerate(start_frame_list[1:]):
        adaptive_section_start_frame = float(section_start_frame) - frame_gap_list[i]/3
        adaptive_start_frame_list.append(adaptive_section_start_frame)
        # print(i, section_start_frame, frame_gap_list[i]/3, adaptive_section_start_frame) 

    for i, section_end_frame in enumerate(end_frame_list[:-1]):
        adaptive_section_end_frame = float(section_end_frame) + frame_gap_list[i]/3
        adaptive_end_frame_list.append(adaptive_section_end_frame)
        # print(i, section_end_frame, frame_gap_list[i]/3, adaptive_section_end_frame) 

    # pdb.set_trace()
    global_end_frame = end_frame_list[-1]
    adaptive_global_end_frame = float(global_end_frame) + normal_frame_gap_threshold
    # print(adaptive_global_end_frame)
    adaptive_global_end_frame = min(adaptive_global_end_frame, total_frames)
    adaptive_end_frame_list.append(adaptive_global_end_frame)
    
    # print("adaptive_start_frame_list:", adaptive_start_frame_list)
    print("len(adaptive_start_frame_list): ", len(adaptive_start_frame_list))
    # print("adaptive_end_frame_list:", adaptive_end_frame_list)
    print("len(adaptive_end_frame_list): ", len(adaptive_end_frame_list))

    adaptive_duration_list = []
    for i in range(len(adaptive_start_frame_list)):
        adaptive_duration_list.append(float(adaptive_end_frame_list[i]) - float(adaptive_start_frame_list[i]))
        print("({}) {} {} {} {}".format(i+1, adaptive_start_frame_list[i], adaptive_end_frame_list[i], adaptive_end_frame_list[i]-adaptive_start_frame_list[i], adaptive_duration_list[i]))
        if float(adaptive_end_frame_list[i]) - float(adaptive_start_frame_list[i]) < (1 * fps):
            print('-'*20, '1')
        if float(adaptive_end_frame_list[i]) - float(adaptive_start_frame_list[i]) > (5 * fps):
            print('-'*20, '5')

    return adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list


def post_adapt(prediction_structure_list, adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list, post_frame_gap_threshold, post_action_frame_threshold, fps):
    """
    adaptive_frame_sections() 的结果中：
    
    1. 时长小于1s的片段与相邻短片段合并，
    2. 时长大于5s的片段 二次拆分, 部分为正常长片段
    """

    post_adapt_start_frame_list = copy.deepcopy(adaptive_start_frame_list)
    post_adapt_end_frame_list = copy.deepcopy(adaptive_end_frame_list)
    post_adapt_duration_frame_list = copy.deepcopy(adaptive_duration_list)

    merge_count = 0 
    split_count = 0   
    for i, adaptive_duration_frame in enumerate(adaptive_duration_list):

        print('----- {} -----'.format(i))
        print('----- {} -----'.format(adaptive_duration_frame))
        
        if adaptive_duration_frame < 1 * fps and i != len(adaptive_duration_list)-1:
            print("adaptive_duration_frame < 1: ", adaptive_duration_frame < 1)
            # pdb.set_trace()

            bias = split_count - merge_count
            # 1. 时长小于1s的片段与相邻短片段合并，
            # 找到相邻短片段
            if adaptive_duration_list[i-1] < adaptive_duration_list[i+1]:
                print("当前片段i与片段i-1合并")
                # 当前片段i与片段i-1合并
                # 1. 剔除当前片段信息(adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list)
                # 2. 修改 片段i-1 的 endframe、frame_gap, section_duration
                new_end_frame = adaptive_end_frame_list[i]
                post_adapt_end_frame_list[i-1+bias] = new_end_frame
                post_adapt_duration_frame_list[i-1+bias] = new_end_frame - post_adapt_start_frame_list[i-1+bias]  # ...

                # print(post_adapt_start_frame_list[i+bias])
                # print(post_adapt_end_frame_list[i+bias])
                # print(post_adapt_duration_frame_list[i+bias])

                del post_adapt_start_frame_list[i+bias] 
                del post_adapt_end_frame_list[i+bias] 
                del post_adapt_duration_frame_list[i+bias]
                # print(post_adapt_start_frame_list[i+bias])
                # print(post_adapt_end_frame_list[i+bias])
                # print(post_adapt_duration_frame_list[i+bias])
                # pdb.set_trace()
            else:
                print("当前片段i与片段i+1合并")
                # 当前片段i与片段i+1合并
                # 1. 剔除当前片段信息(adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list)
                # 2. 修改 片段i-1 的 endframe、frame_gap, section_duration
                new_start_frame = adaptive_start_frame_list[i] 
                post_adapt_start_frame_list[i+1+bias] = new_start_frame
                post_adapt_duration_frame_list[i+1+bias] = post_adapt_end_frame_list[i+1+bias] - new_start_frame
                
                # print(post_adapt_start_frame_list[i+bias])
                # print(post_adapt_end_frame_list[i+bias])
                # print(post_adapt_duration_frame_list[i+bias])
                
                del post_adapt_start_frame_list[i+bias] 
                del post_adapt_end_frame_list[i+bias] 
                del post_adapt_duration_frame_list[i+bias]
                
                # print(post_adapt_start_frame_list[i+bias])
                # print(post_adapt_end_frame_list[i+bias])
                # print(post_adapt_duration_frame_list[i+bias])
                # pdb.set_trace()

            merge_count += 1
        
        if adaptive_duration_frame > 5 * fps:

            adaptive_start_frame = float(adaptive_start_frame_list[i])
            adaptive_end_frame = float(adaptive_end_frame_list[i])

            # 获取该片段 start - end currentframe (prediction_frame)
            for frame_info_dict in prediction_structure_list:
                for (frame_value, _) in frame_info_dict.items():
                    if float(frame_value) >= adaptive_start_frame:
                        start_currentframe = float(frame_value)
                        break

            for i, frame_info_dict in enumerate(prediction_structure_list):
                for (frame_value, _) in frame_info_dict.items():
                    if float(frame_value) >= adaptive_end_frame:
                        end_currentframe = last_frame
                        break
                    last_frame = float(frame_value) 
                
                if i == len(prediction_structure_list)-1:
                    end_currentframe = frame_value
            
            
            # print("start_currentframe: ", start_currentframe)
            # print("end_currentframe: ", end_currentframe)
            # print("adaptive_duration_frame: ", adaptive_duration_frame)
            # print('i:', i)
            # pdb.set_trace()

            last_frame = adaptive_start_frame
            for frame_info_dict in prediction_structure_list:
                for (prediction_frame, _) in frame_info_dict.items():

                    if float(prediction_frame) >= start_currentframe:

                        bias = split_count - merge_count
                        
                        current_frame = float(prediction_frame)
                        # print("current_frame: ", current_frame)
                        frame_gap = float(current_frame) - float(last_frame)
                        # print("frame_gap: ", frame_gap)

                        if frame_gap >= post_frame_gap_threshold:
                            # pdb.set_trace()

                            # 超过0.5 就判定为间隔
                            if last_frame == adaptive_start_frame:
                                # 片段头部”空白“（无意义停顿）不处理
                                # print("last_frame == adaptive_start_frame")
                                continue
                            # 新增 adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list 条目
                            # 默认后增
                            update_adaptive_end_frame = last_frame + frame_gap//2
                            update_adaptive_duration_frame = update_adaptive_end_frame - post_adapt_start_frame_list[i+bias]
                            
                            new_adaptive_start_frame = current_frame - frame_gap//2
                            new_adaptive_end_frame = adaptive_end_frame
                            new_adaptive_duration_frame = new_adaptive_end_frame - new_adaptive_start_frame

                            if update_adaptive_duration_frame < 1 or new_adaptive_duration_frame < 1:
                                continue

                            post_adapt_end_frame_list[i+bias] = update_adaptive_end_frame
                            post_adapt_duration_frame_list[i+bias] = update_adaptive_duration_frame

                            post_adapt_start_frame_list.insert(i+1+bias, new_adaptive_start_frame)
                            post_adapt_end_frame_list.insert(i+1+bias, new_adaptive_end_frame)
                            post_adapt_duration_frame_list.insert(i+1+bias, new_adaptive_duration_frame)
                            split_count += 1
                            
                            if new_adaptive_duration_frame < post_action_frame_threshold:
                                break

                            # pdb.set_trace()
                        
                        last_frame = current_frame
                    
                    if float(prediction_frame) > end_currentframe:
                        break
                
            # print()

    for i in range(len(post_adapt_start_frame_list)):
        print("({}) {} {} {}".format(i+1, post_adapt_start_frame_list[i], post_adapt_end_frame_list[i], post_adapt_end_frame_list[i]-post_adapt_start_frame_list[i]), post_adapt_duration_frame_list[i])
        if float(post_adapt_end_frame_list[i]) - float(post_adapt_start_frame_list[i]) < (1 * fps):
            print('-'*30, '1')
        if float(post_adapt_end_frame_list[i]) - float(post_adapt_start_frame_list[i]) > (5 * fps):
            print('-'*30, '5')

    return post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list


def cut_video(video_file, cut_video_dir, post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list, fps, stateTextEdit):

    for i in range(len(post_adapt_duration_frame_list)):
        start_ss = float(post_adapt_start_frame_list[i])/fps
        duration = float(post_adapt_end_frame_list[i])/fps - start_ss
        result_filename = video_file.split('/')[-1].split('.')[0] + '_cut_{}.mp4'.format(i)
        result_file = os.path.join(cut_video_dir, result_filename)

        if os.path.isfile(result_file):
            os.remove(result_file)

        # frames → video
        os.system('ffmpeg -ss {} -i {} -t {} -c:v libx264 -c:a aac -strict experimental -b:a 96k {}'.format(start_ss, video_file, duration, result_file))
        print("start_ss: ", start_ss, "duration: ", duration, " SUCCEED !!!")
        stateTextEdit.append("{}  SUCCEED !!! ".format(result_filename))
        pass


if __name__ == "__main__":
    
    import global_config
    video_file = global_config.video_file
    scores_txt = global_config.scores_txt
    cut_video_dir = global_config.cut_video_dir
    
    if not os.path.exists(cut_video_dir):
        os.makedirs(cut_video_dir)

    prediction_structure_list, frame_list = txt2structure(scores_txt)
    print("len(prediction_structure_list): ", len(prediction_structure_list))
    print("len(frame_list): ", len(frame_list))

    fps, size, total_frames, rate, total_duration = get_video_info(video_file)  # size: (width, height)
    im_width, im_height = size[0], size[1]
     
    normal_frame_gap_threshold = 1 * fps  # 正常动作间隔
    short_frame_gap_threshold = 0.5 * fps  # 较短动作间隔
    post_frame_gap_threshold = 0.6 * fps
    post_action_frame_threshold = 3.5 * fps
    
    start_frame_list, end_frame_list, frame_gap_list, duration_list = pick_predict_frame_sections(prediction_structure_list, frame_list, normal_frame_gap_threshold, short_frame_gap_threshold, im_width, im_height, blackBorder=False)
    print('*'*10)
    adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list = adaptive_frame_sections(start_frame_list, end_frame_list, frame_gap_list, duration_list, normal_frame_gap_threshold, total_frames, fps)
    # pdb.set_trace()
    print('**'*10)
    post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list = post_adapt(prediction_structure_list, adaptive_start_frame_list, adaptive_end_frame_list, adaptive_duration_list, post_frame_gap_threshold, post_action_frame_threshold, fps)
    # pdb.set_trace()
    
    print('***'*10)
    # cut_video(video_file, cut_video_dir, post_adapt_start_frame_list, post_adapt_end_frame_list, post_adapt_duration_frame_list, fps)
    # pass
