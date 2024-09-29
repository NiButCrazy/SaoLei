"""
逻辑代码集合处和游戏入口
"""
import pygame
import sys
import eventManager
import button
import time
import config

# 初始化，切记这是所有游戏代码操作之前
pygame.init()

# 设置默认帧率
FPS = config.get_config("FPS")
# 计算出游戏更新循环周期
FPS_CLOCK = 1 / FPS
# 设置一个Surface类的图标
icon = pygame.image.load("./resource/icon.png")
pygame.display.set_icon(icon)
# 设置标题
pygame.display.set_caption("扫雷🤣👉🤡")
# 设置屏幕大小
screen = pygame.display.set_mode((config.get_config("width"), config.get_config("height")))
# 事件管理器
event_manager = eventManager.manager

btn_1 = button.ButtonBase(screen, 0, 0, (100, 100), "1")

while True:
    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        else:
            event_manager.emit(event)

    # UI绘制
    btn_1.update()

    pygame.display.flip()
    time.sleep(FPS_CLOCK)

