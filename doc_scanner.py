'''
"doc_scanner.py" 文件中的 DocScanner 类提供了文档扫描的核心功能，功能包括
    - 加载图片
    - 找到文档的角落
    - 裁剪图片

- 通过将文档扫描功能封装在一个独立的类中，我们可以将其作为一个模块，方便在其他项目中重用。
- 这种模块化的设计使得代码更加模块化、可扩展和可测试。
- 它可以独立于其他部分进行开发、测试和维护，而不会对其他组件产生影响。
- 此外，将文档扫描功能单独放在一个文件中，使得代码结构更清晰、易于理解和维护。
- 通过将不同的功能分割到不同的文件中，我们可以更好地组织代码，减少文件的复杂性，并促进团队合作开发。
'''
import cv2   # 导入 OpenCV 库，用于图片处理和计算机视觉任务
import numpy as np  # 导入 numpy 库，用于进行数值计算

class DocScanner:
    def __init__(self):
        pass  # DocScanner 的初始化方法，目前为空

    def load_image(self, file_path):
        """加载图片并找到文档的四个角落。"""
        img =  cv2.imread(file_path)         #TODO  # 读取图片
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)      #TODO  # 将图片转换为灰度图

        # 对灰度图进行二值化，得到二值图

        #两种方法：1.自动阈值 2.手动阈值
        thresh, binary_img = cv2.threshold(img_gray, 0, 255,  cv2.THRESH_OTSU)   #TODO
        #thresh, binary_img = cv2.threshold(img_gray, 127, 255,  cv2.THRESH_BINARY)   #TODO
        
        # 找到二值图的所有轮廓
        contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)     #TODO
        
        # 找到最大的周长的四边形的四个顶点 extreme_pnts
        #TODO
        max_perimeter = 0
        extreme_pnts = None
        for contour in contours:
            # 计算轮廓的周长
            perimeter = cv2.arcLength(contour, True)
            # approx为轮廓的近似多边形
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)      #perimeter * 0.02为近似精度

            # 如果轮廓是四边形且周长大于之前的最大周长，则更新最大周长和四个顶点
            if len(approx) == 4 and perimeter > max_perimeter:
                max_perimeter = perimeter
                extreme_pnts = approx
        
        corners = self.order_points(extreme_pnts.reshape(4, 2))  # 对四个顶点进行排序

        #print(corners)
        return img, corners  # 返回图片和排序后的顶点


    def order_points(self, pts):
        """对给定的四个点进行排序，返回排序后的点。"""
        rect = np.zeros((4, 2), dtype="float32")  # 初始化排序后的点为全零
        s = pts.sum(axis=1)  # 计算每个点的坐标和
        rect[0] = pts[np.argmin(s)]  # 左上角的点坐标和最小的那个点
        rect[2] = pts[np.argmax(s)]  # 右下角的点坐标和最大的那个点
        diff = np.diff(pts, axis=1)  # 计算每个点的坐标差
        rect[1] = pts[np.argmin(diff)]  # 右上角的点坐标差最小的那个点
        rect[3] = pts[np.argmax(diff)]  # 左下角的点坐标差最大的那个点

        print(f"0:左上角:{rect[0]},因为x,y的坐标和是: np.min(s)={np.min(s)}")
        print(f"1:右上角:{rect[1]},因为x,y的坐标和是: np.min(diff)={np.min(diff)}")
        print(f"2:右下角:{rect[2]},因为x,y的坐标差是: np.max(s)={np.max(s)}")
        print(f"3:左下角:{rect[3]},因为x,y的坐标差是: np.max(diff)={np.max(diff)}")

        return rect  # 返回排序后的点


    def crop_image(self, img, corners):
        """根据四个角落裁剪图片。"""

        # 获取四个角落的坐标
        top_left_corner = corners[0]
        top_right_corner = corners[1]
        bottom_right_corner = corners[2]
        bottom_left_corner = corners[3]

        # 计算目标图片的宽度和高度
        width, height = self.get_image_dimensions((top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner))  

        # 根据以上宽度和高度创建于原有四个点顺序对应的目标四个点的坐标
        dst_points = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]], dtype="float32")
        
        # 通过投影变换展平文档
        # TODO
        M = cv2.getPerspectiveTransform(corners, dst_points)
        dst = cv2.warpPerspective(img, M, (width, height))
        return dst  # 返回展平后的图像

    def get_image_dimensions(self, corners):
        """计算图片的宽度和高度。"""
        #TODO
        # 从 corners 中获取四个角落的坐标
        top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner = corners

        # 计算目标图片的宽度和高度
        width_top = np.sqrt(((top_right_corner[0] - top_left_corner[0]) ** 2) + ((top_right_corner[1] - top_left_corner[1]) ** 2))
        width_bottom = np.sqrt(((bottom_right_corner[0] - bottom_left_corner[0]) ** 2) + ((bottom_right_corner[1] - bottom_left_corner[1]) ** 2))
        height_left = np.sqrt(((bottom_left_corner[0] - top_left_corner[0]) ** 2) + ((bottom_left_corner[1] - top_left_corner[1]) ** 2))
        height_right = np.sqrt(((bottom_right_corner[0] - top_right_corner[0]) ** 2) + ((bottom_right_corner[1] - top_right_corner[1]) ** 2))

        # 取最大值
        width = max(int(width_top), int(width_bottom))
        height = max(int(height_left), int(height_right))

        return width, height  # 返回图片的宽度和高度
    