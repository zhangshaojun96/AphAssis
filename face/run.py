##以下是整个系统需要加载的模型，为了避免重复加载
import face.CNN_MODEL as cnn
import cv2
import face.FACE as FACE

# 识别，返回数组
def get_emotion(snap_base64):
    #print(snap_base64)
    print("模型收到的base64参数长度")
    print(len(snap_base64))
    res = FACE.get_emotion(str(snap_base64))
    print("识别结果")
    print(res)
    return res

