import cv2
import os
import time

# 配置参数
TARGET_WIDTH = 2048  # 2K宽度（常见2K分辨率：2560×1440）
TARGET_HEIGHT = 1536  # 2K高度
SAVE_FOLDER = "captured_photos"  # 存储目录

# 创建存储目录
os.makedirs(SAVE_FOLDER, exist_ok=True)

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 尝试设置分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, TARGET_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, TARGET_HEIGHT)

# 验证实际分辨率
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if (actual_width, actual_height) != (TARGET_WIDTH, TARGET_HEIGHT):
    print(f"警告：相机不支持 {TARGET_WIDTH}x{TARGET_HEIGHT}，当前实际分辨率：{actual_width}x{actual_height}")

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 状态变量
show_message = False
message_start_time = 0

while True:
    # 读取摄像头画面
    ret, frame = cap.read()
    if not ret:
        print("无法获取画面")
        break

    # 显示分辨率提示
    # cv2.putText(frame, f"当前分辨率: {actual_width}x{actual_height}",
    #             (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 显示拍照提示
    if show_message:
        elapsed = time.time() - message_start_time
        if elapsed < 1:
            pass
            # cv2.putText(frame, "照片已保存!", (20, 70),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            show_message = False

    # 显示画面
    cv2.imshow("2K相机", frame)

    # 检测键盘输入
    key = cv2.waitKey(1)

    # 按空格键拍照
    if key == 32:  # 空格键
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_FOLDER, f"2k_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"2K照片已保存: {filename}")
        show_message = True
        message_start_time = time.time()

    # 退出条件
    if key == 27 or key == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()