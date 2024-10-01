"""
开始菜单场景
"""
import pygame
import uiBase
import sys

from config import get_config
from eventManager import event_manager
from startSceneBtn import StartSceneBtn
from tkinter import messagebox
from sceneManager import scene_manager


screen_width = get_config("width")
screen_height = get_config("height")
game_version = get_config("version")

setting_ui_background_img = pygame.image.load("resource/ui_background.png")
rank_ui_background_img = pygame.image.load("resource/ui_rank.png")

font_path = "resource/font.ttf"

# 音频模块初始化
pygame.mixer.init()

def start_menu_scene(screen: pygame.Surface) -> tuple[list[StartSceneBtn], pygame.Surface]:
    """
    开始菜单场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """
    # 注册自定义事件，防止pygame自带事件来不及更新
    event_manager.register_event("打开开始游戏")
    event_manager.register_event("打开设置")
    event_manager.register_event("打开致谢")
    event_manager.register_event("打开排行")

    # 播放背景音乐
    pygame.mixer.music.load("resource/music2.mp3")
    pygame.mixer.music.set_volume(get_config("volume"))
    pygame.mixer.music.play(-1)

    # 此场景的背景图片
    background_img = pygame.image.load("resource/background-img.jpg")
    # 加载各选项所关联的图片
    btn_start_game_switch_img = pygame.image.load("resource/start_game.png")
    btn_setting_switch_img = pygame.image.load("resource/setting2.png")
    btn_rank_switch_img = pygame.image.load("resource/rank.png")
    btn_create_switch_img = pygame.image.load("resource/create.png")
    btn_exit_switch_img = pygame.image.load("resource/setting.png")

    # 选项所关联的图片
    switch_img_surface = uiBase.UIBase(screen, 200, 170, (400, 400))
    switch_img_surface.set_background_image("resource/setting.png")
    switch_img_surface.enabled_event = False
    # 选项所关联的文字
    switch_text = uiBase.UIBase(screen, 200, 520, (400, 50), text="欢迎", font_size=28, font_color=(125, 125, 125), font_family = "resource/font.ttf", user_font_family=True)
    switch_text.opacity = 0
    switch_text.enabled_event =False
    # 开始游戏按钮
    btn_start_game = StartSceneBtn(screen, -52, 100, (200, 70), text = "开始",font_size = 22)
    btn_start_game.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_start_game_switch_img), switch_text.set_text(content = "吃雷行动")))
    # 设置按钮
    btn_setting = StartSceneBtn(screen, -52, 180, (200, 70), text = "设置", font_size = 22)
    btn_setting.mouse_enter(lambda event, args: (switch_img_surface.set_background_image(btn_setting_switch_img), switch_text.set_text(content = "懒狗设置")))
    btn_setting.mouse_up(lambda event, args: open_setting(screen,btn_setting))
    # 排行按钮
    btn_rank = StartSceneBtn(screen, -52, 260, (200, 70), text = "排行", font_size = 22)
    btn_rank.mouse_enter(lambda event, args: ( switch_img_surface.set_background_image(btn_rank_switch_img), switch_text.set_text(content = "历史记录排行")))
    btn_rank.mouse_up(lambda event, args: open_rank(screen, btn_rank))
    # 致谢按钮
    btn_create = StartSceneBtn(screen, -52, 340, (200, 70), text = "致谢", font_size = 22)
    btn_create.mouse_enter(lambda event, args: ( switch_img_surface.set_background_image(btn_create_switch_img), switch_text.set_text(content = "开发者名单")))
    # 退出按钮
    btn_exit = StartSceneBtn(screen, -52, screen_height - 100, (200, 70), text = "退出", font_size = 22)
    btn_exit_img = pygame.image.load("resource/btn_exit.png")

    # 忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_enter(event: pygame.event.Event, args: tuple):
        btn_exit.set_background_image(btn_exit_img)
        switch_img_surface.set_background_image(btn_exit_switch_img)
        switch_text.set_text(content="你真要狠心离开吗")

    # 可以忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_up(event: pygame.event.Event, args: tuple):
        sure = messagebox.askokcancel("太狠心了", "要离开了吗？")
        if sure:
            pygame.quit()
            sys.exit()

    btn_exit.mouse_enter(btn_exit_enter)
    btn_exit.mouse_up(btn_exit_up)
    # 版本号
    version = uiBase.UIBase(screen, screen_width - 128, screen_height - 50, (128, 50), text = game_version, font_size = 18)
    version.opacity = 0
    version.enabled_event = False
    # 将按钮添加进UI列表
    ui_list= [
        btn_start_game,
        btn_setting,
        btn_rank,
        btn_create,
        btn_exit,
        version,
        switch_img_surface,
        switch_text
    ]
    return ui_list,background_img

def open_setting(screen: pygame.Surface,btn: StartSceneBtn):
    """
    打开设置UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = 1 / get_config("FPS")
        # 发送一个打开设置的事件，间接更新渲染视图
        event_manager.post_event("打开设置")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        setting_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color = (0, 0, 0))
        # 创建一个背景图片
        setting_ui = uiBase.UIBase(screen, 100, -30, (600,800))
        setting_ui.set_background_image(setting_ui_background_img)
        # 淡入效果
        setting_ui_mask.opacity = 0
        setting_ui.opacity = 0
        setting_ui_mask.transition_opacity(70, 0.1, fps_clock)
        setting_ui.transition_opacity(255, 0.2, fps_clock)
        # 背景图片设为遮罩子节点，方便管理
        setting_ui_mask.children.append(setting_ui)
        # 创建一个关闭设置UI的函数
        def close_setting_ui(**option):
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {}:
                pass
            btn.has_open_ui = False
            # 淡出
            setting_ui_mask.transition_opacity(0, 0.1, fps_clock).then(lambda **options: setting_ui_mask.close())
            setting_ui.transition_opacity(0, 0.1, fps_clock)
        # 开启遮罩的键盘事件
        setting_ui_mask.enabled_keyboard_event = True
        setting_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_setting_ui)

        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(setting_ui_mask)

def open_rank(screen: pygame.Surface,btn: StartSceneBtn):
    """
    打开设置UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = 1 / get_config("FPS")
        # 发送一个打开设置的事件，间接更新渲染视图
        event_manager.post_event("打开设置")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        setting_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color = (0, 0, 0))
        # 创建一个背景图片
        setting_ui = uiBase.UIBase(screen, 160, 40, (500,700))
        setting_ui.set_background_image(rank_ui_background_img)
        # 淡入效果
        setting_ui_mask.opacity = 0
        setting_ui.opacity = 0
        setting_ui_mask.transition_opacity(70, 0.1, fps_clock)
        setting_ui.transition_opacity(255, 0.2, fps_clock)
        # 背景图片设为遮罩子节点，方便管理
        setting_ui_mask.children.append(setting_ui)
        # 创建一个关闭设置UI的函数
        def close_setting_ui(**option):
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {}:
                pass
            btn.has_open_ui = False
            # 淡出
            setting_ui_mask.transition_opacity(0, 0.1, fps_clock).then(lambda **options: setting_ui_mask.close())
            setting_ui.transition_opacity(0, 0.1, fps_clock)
        # 开启遮罩的键盘事件
        setting_ui_mask.enabled_keyboard_event = True
        setting_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_setting_ui)

        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(setting_ui_mask)


