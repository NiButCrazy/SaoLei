"""
逻辑代码集合处和游戏入口
"""
import sys
import pygame
import startScene
import time
import config
from sceneManager import scene_manager
from eventManager import emit
from inputBox import message_box



# 初始化，切记这是所有游戏代码操作之前
pygame.init()
# 设置一个Surface类的图标
icon = pygame.image.load("./resource/icon.png")
pygame.display.set_icon(icon)
# 设置标题
pygame.display.set_caption("扫雷🤣👉🤡")
# 设置屏幕大小
screen = pygame.display.set_mode((config.get_config("width"), config.get_config("height")))
# ==== 设定初始场景UI ====
# 将菜单场景推入场景列表
scene_manager.push_scene("start_menu", startScene.start_menu_scene(screen))
# 加载现有场景
scene_manager.load_scene("start_menu")

while True:
    # 事件监听
    for event in pygame.event.get():
        # 是否开启事件穿透。只针对鼠标事件
        event.enabled_event_penetration = False
        if event.type == pygame.QUIT:
            res = message_box("太狠心了", "要离开了吗？")
            if res:
                pygame.quit()
                sys.exit()
        else:
            # 向事件管理器发送事件
            emit(event, stop_emit = False)

    # 清屏
    screen.fill((0, 0, 0))
    # 这是背景图片绘制
    screen.blit(scene_manager.now_scene[1], (0, 0))
    # UI绘制
    for ui in scene_manager.now_scene[0]:
        ui.update(scene_manager.FPS_CLOCK)
    # 更新屏幕
    pygame.display.flip()
    # 保证帧率
    time.sleep(scene_manager.FPS_CLOCK)

