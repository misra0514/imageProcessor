import cv2
import numpy as np
import os
from tqdm import tqdm

IMG_ADDR1 = 'flower_pics/'
IMG_ADDR2 = './'


TESTMODE = 1
VIDEOMODE = 2

'''
图像处理部分
'''
def afternoon(img, gamma = 0.65):
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)]
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)
    img = cv2.LUT(img,gamma_table)
    img = cv2.normalize(img,dst=None,alpha=255,beta=25,norm_type=cv2.NORM_INF)
    return img
def night(img):
    img = cv2.normalize(img,dst=None,alpha=255,beta=30,norm_type=cv2.NORM_MINMAX)
    return img


'''
每1秒钟有n张图片写入，帧率为n。
使用'I','4','2','0'编码得到的是.avi文件。如果需要其他编码格式的话可以尝试修改VideoWriter_fourcc参数，同时修改文件名后缀。
'''
def picToVideo(in_path, size, out_path, fps = 48):
    filelist = os.listdir(in_path)
    filelist.sort()
    out_path = out_path + "test" + ".avi"  # 导出路径
    fourcc = cv2.VideoWriter_fourcc('I','4','2','0') 
    video = cv2.VideoWriter(out_path, fourcc, fps, size)

    for item in  tqdm(filelist):
        img = cv2.imread(in_path + item)
        date = str(item).split("_")[1].split(".")[0]
        if(int(date) > 1900 or int(date) < 510 ): 
            img = night(img)
        elif(int(date) > 1330):
            img = afternoon(img)
        video.write(img) 
    video.release() 

def viewPics(in_path):
    print("find ", len(os.listdir(in_path)) , "files")
    cv2.namedWindow("demo",0)#将显示窗口的大小适应于显示器的分辨率
    files = os.listdir(in_path)
    files.sort()
    for item in tqdm(files):
        img = cv2.imread(in_path+item)
        date = str(item).split("_")[1].split(".")[0]
        print(date)
        if(int(date) > 1900 or int(date) < 510 ):  
            img = night(img)
        elif(int(date) > 1330):
            img = afternoon(img)
        else:
            pass
        cv2.imshow("demo", img)
        k = cv2.waitKey(1)


if __name__ == '__main__':
    IN_ADDR = IMG_ADDR1
    OUT_ADDR = IMG_ADDR2
    mode = VIDEOMODE

    if(mode == TESTMODE):
        viewPics(IN_ADDR)
    elif(mode  == VIDEOMODE):
        picToVideo(IN_ADDR, (3280, 2464), OUT_ADDR)   # 注意这个地方必须和图片的分辨率相同





