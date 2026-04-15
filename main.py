# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


# def print_hi(name):
#     # 在下面的代码行中使用断点来调试脚本。
#     print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。
import random

def get_user_location() -> str:
    return random.choice(["上海","苏州","杭州"])

def get_weather(city:str) -> str:
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print(get_weather(get_user_location()))

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
