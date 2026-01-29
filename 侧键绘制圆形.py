from pynput import mouse
from pynput import keyboard
import threading
import time
import math

# 核心配置
mouse_controller = mouse.Controller()
RADIUS = 80  # 圆半径（像素）
SEGMENTS = 50  # 分段数（越大越圆滑）

# 控制宏执行的停止开关：各绘制宏在执行过程中定期检查
macro_stop_event = threading.Event()

def draw_circle(center_x, center_y):
    """以指定坐标为圆心绘制圆形"""
    # 计算圆周离散点
    points = [(int(center_x + RADIUS * math.cos(2 * math.pi * i / SEGMENTS)),
               int(center_y + RADIUS * math.sin(2 * math.pi * i / SEGMENTS))) 
              for i in range(SEGMENTS + 1)]
    
    # 移动到起点并开始绘制
    mouse_controller.position = points[0]
    time.sleep(0.01)
    mouse_controller.press(mouse.Button.left)
    time.sleep(0.02)
    
    # 拖动绘制圆周
    for x, y in points[1:]:
        if macro_stop_event.is_set():
            break
        mouse_controller.position = (x, y)
        time.sleep(0.02)
    
    # 结束绘制
    mouse_controller.release(mouse.Button.left)
    print("圆形绘制完成 ")

def handle_draw():
    macro_stop_event.clear()
    try:
        mouse_controller.release(mouse.Button.x2)  # 释放侧键
    except:
        pass
    x, y = mouse_controller.position
    draw_circle(x, y)

def on_click(x, y, button, pressed):
    """监听侧键按下触发绘制"""
    if button == mouse.Button.x2 and pressed:
        print("检测到侧键按下，开始绘制圆形...")
        threading.Thread(target=handle_draw, daemon=True).start()

def on_key_press(key):
    try:
        # P 键：暂停当前宏（不再继续后续绘制）
        if (hasattr(key, "char") and key.char in ("p", "P")) or (hasattr(key, "vk") and key.vk == 80):
            macro_stop_event.set()
            return

        # '-' 键作为上侧键(X2)的替代触发
        if hasattr(key, "char") and key.char == "-":
            threading.Thread(target=handle_draw, daemon=True).start()
            return
    except Exception as e:
        print(f"键盘监听异常: {e}")

# 主程序
print("侧键绘圆脚本启动 | 侧键(X2)或 '-' 键绘制圆形 | P键暂停 | Ctrl+C退出")
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_key_press)

mouse_listener.start()
keyboard_listener.start()

mouse_listener.join()