import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_bounding_box(center_x, center_y, length, width):
    # 计算矩形框的左上角坐标
    x1 = center_x - width / 2
    y1 = center_y - length / 2
    
    # 创建一个新的图形
    fig, ax = plt.subplots(1)
    
    # 绘制胶囊（这里用一个圆表示）
    capsule = plt.Circle((center_x, center_y), min(width, length) / 4, color='blue', fill=False)
    ax.add_artist(capsule)
    
    # 绘制矩形框
    rect = patches.Rectangle((x1, y1), width, length, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    
    # 设置坐标轴范围以确保整个图形可见
    margin = 50
    ax.set_xlim(center_x - width/2 - margin, center_x + width/2 + margin)
    ax.set_ylim(center_y - length/2 - margin, center_y + length/2 + margin)
    
    # 显示图形
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# 胶囊中心坐标
center_x = 100
center_y = 250

# 胶囊长度和宽度
length = 100  # 假设胶囊长度为100像素
width = length / 3  # 宽度大约是长度的三分之一

draw_bounding_box(center_x, center_y, length, width)