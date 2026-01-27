from pynput import mouse
import threading
import time
# 核心配置与全局变量
clicking = False
click_interval = 0.05  # 连点间隔
mouse_ctrl = mouse.Controller()
auto_close_seconds = 5
start_time = 0
def on_click(x, y, button, pressed):
    global clicking, start_time
    # 仅响应侧键（x2）按下动作
    if button == mouse.Button.x2 and pressed:
        clicking = not clicking
        if clicking:
            print("连点开启 ✅（5秒自动关闭）")
            start_time = time.time()
            # 启动连点线程
            threading.Thread(target=auto_click, daemon=True).start()
        else:
            print("连点关闭 ❌")
            start_time = 0
def auto_click():
    global clicking
    while clicking:
        # 超时自动关闭
        if time.time() - start_time > auto_close_seconds:
            clicking = False
            print(f"连点自动关闭 ⏰（超时{auto_close_seconds}秒）")
            break
        # 模拟左键点击
        mouse_ctrl.press(mouse.Button.left)
        mouse_ctrl.release(mouse.Button.left)
        time.sleep(click_interval)

# 主程序
print("脚本启动 🚀 | 侧键(X2)开关连点 | Ctrl+C退出")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()