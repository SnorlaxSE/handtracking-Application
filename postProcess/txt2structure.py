import collections
import os
import pdb


def txt2structure(txt_file):
    """
    仅记录被检测出的帧信息

    """

    prediction_structure_list = []
    frame_list = []
    frame_info_value_dict = {}
    with open(txt_file, "r") as f:
        for line in f.readlines():
            # ex. {58: {'scores': [0.30838698], 'boxes': [array([0.90856266, 0.32726675, 1.        , 0.47203618], dtype=float32)]}}

            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            line = line[1:-1]  # rm '{' and '}'


            frame_info = ':'.join(line.split(':')[1:]).strip()[1:-1]
            
            # extract scores info 
            scores_info = frame_info.split("'boxes'")[0].replace(' ', '')
            scores_str_list = scores_info[scores_info.index("[")+1: scores_info.index("]")].split(',')
            if scores_str_list == ['']:
                # 忽略 score 为空的帧信息
                continue

            frame_value = int(line.split(':')[0])
            frame_list.append(frame_value)

            scores_list = []
            for scores_str in scores_str_list:
                scores_list.append(float(scores_str))

            frame_info_value_dict['scores'] = scores_list

            # extract boxes info 
            boxes_info = ("'boxes'" + frame_info.split("'boxes'")[1]).replace(' ', '')
            boxes_tmp_list = boxes_info[boxes_info.index(":")+1:-1].split(",dtype=float32)")
            
            boxes_str_lists = []
            for boxes_tmp in boxes_tmp_list:
                if boxes_tmp != '':
                    boxes_str_lists.append(boxes_tmp[8:-1].split(','))
            
            boxes_lists = []
            for boxes_str_list in boxes_str_lists:
                boxes_list = []
                for boxes_str in boxes_str_list:
                    try:
                        boxes_list.append(float(boxes_str))
                    except:
                        pdb.set_trace()
                boxes_lists.append(boxes_list)
            frame_info_value_dict['boxes'] = boxes_lists

            # print("frame_value: ", frame_value)
            # print("frame_info: ", frame_info)
            # print("scores_info: ", scores_info)
            # print("scores_list: ", scores_list)
            # print("score_dict: ", score_dict)
            # print("boxes_info: ", boxes_info)
            # print("boxes_lists: ", boxes_lists)
            # print("boxes_dict: ", boxes_dict)
            # print({frame_value:[score_dict, boxes_dict]})
            prediction_structure_list.append({frame_value:frame_info_value_dict})
            frame_info_value_dict = {}

            # pdb.set_trace()

            """
            prediction_structure_list[0]
            {58: {'scores': [0.30838698], 'boxes': [[0.90856266, 0.32726675, 1.0, 0.47203618]]}}
            {168: {'scores': [0.6841056, 0.6657858], 'boxes': [[0.3419823, 0.47440776, 0.502142, 0.55743474], [0.48269054, 0.65848, 0.64012533, 0.72797984]]}}

            source:
            {58: {'scores': [0.30838698], 'boxes': [array([0.90856266, 0.32726675, 1.        , 0.47203618], dtype=float32)]}}
            {168: {'scores': [0.6841056, 0.6657858], 'boxes': [array([0.3419823 , 0.47440776, 0.502142  , 0.55743474], dtype=float32), array([0.48269054, 0.65848   , 0.64012533, 0.72797984], dtype=float32)]}}

            prediction_structure_list[0][168]['boxes'][0]
            [0.3419823, 0.47440776, 0.502142, 0.55743474]
            """
    return prediction_structure_list, frame_list

if __name__ == "__main__":
    
    import global_config
    scores_txt = global_config.scores_txt
    
    prediction_structure_list, frame_list = txt2structure(scores_txt)

    for frame_info_dict in prediction_structure_list:
        for (frame_value, frame_info_value_dict) in frame_info_dict.items():
            
            print("frame_value: ", frame_value)
            print("score_list: ", frame_info_value_dict['scores'])
            print("boxes_list: ", frame_info_value_dict['boxes'])
            pdb.set_trace()
            

    print("len(prediction_structure_list): ", len(prediction_structure_list))
    print("len(frame_list): ", len(frame_list))
    # print(frame_list)
    pass
