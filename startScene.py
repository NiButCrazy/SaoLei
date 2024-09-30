"""
开始菜单场景
"""
import pygame
import uiBase
import sys
from config import get_config
from startSceneBtn import StartSceneBtn
from tkinter import messagebox


screen_width = get_config("width")
screen_height = get_config("height")
game_version = get_config("version")
# 音频模块初始化
pygame.mixer.init()

def load_start_scene(screen: pygame.Surface) -> tuple[list[StartSceneBtn], pygame.Surface]:
    """
    开始菜单场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """
    pygame.mixer.music.load("resource/music2.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # 此场景的背景图片
    background_img = pygame.image.load("resource/background-img.jpg")
    # 加载各选项所关联的图片
    btn_start_game_switch_img = pygame.image.load("resource/start_game.png")
    btn_setting_switch_img = pygame.image.load("resource/setting2.png")
    btn_create_switch_img = pygame.image.load("resource/create.png")
    # 选项所关联的图片
    switch_img_surface = uiBase.UIBase(screen, 200, 170, (400, 400))
    switch_img_surface.set_background_image("resource/setting.png")
    # 选项所关联的文字
    switch_text = uiBase.UIBase(screen, 200, 520, (400, 50), text="欢迎", font_size=25, font_color=(125, 125, 125))
    switch_text.opacity = 0
    # 开始游戏按钮
    btn_start_game = StartSceneBtn(screen, -52, 100, (200, 70), text = "开始",font_size = 22)
    btn_start_game.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_start_game_switch_img), switch_text.set_text(content = "吃雷行动")))
    # 设置按钮
    btn_setting = StartSceneBtn(screen, -52, 180, (200, 70), text = "设置", font_size = 22)
    btn_setting.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_setting_switch_img), switch_text.set_text(content = "懒狗设置")))
    # 致谢按钮
    btn_create = StartSceneBtn(screen, -52, 260, (200, 70), text = "致谢", font_size = 22)
    btn_create.mouse_enter(lambda event, args: ( switch_img_surface.set_background_image(btn_create_switch_img), switch_text.set_text(content = "开发者名单")))


    # 退出按钮
    btn_exit = StartSceneBtn(screen, -52, screen_height - 100, (200, 70), text = "退出", font_size = 22)
    btn_exit_img = pygame.image.load("resource/btn_exit.png")
    def btn_exit_enter(event: pygame.event.Event, args: tuple):
        btn_exit.set_background_image(btn_exit_img)
        switch_img_surface.set_background_image("resource/setting.png")
        switch_text.set_text(content="你真的狠心离开吗")

    def btn_exit_up(event: pygame.event.Event, args: tuple):
        sure = messagebox.askokcancel("提示", "确定退出游戏吗？")
        if sure:
            pygame.quit()
            sys.exit()
    btn_exit.mouse_enter(btn_exit_enter)
    btn_exit.mouse_up(btn_exit_up)
    # 版本号
    version = uiBase.UIBase(screen, screen_width - 128, screen_height - 50, (128, 50), text = game_version, font_size = 18)
    version.opacity = 0
    # 将按钮添加进UI列表
    ui_list= [
        btn_start_game,
        btn_setting,
        btn_create,
        btn_exit,
        version,
        switch_img_surface,
        switch_text
    ]

    return ui_list,background_img
