"""
开始菜单场景
"""
import pygame

import uiBase
import sys

from inputBox import create_input_box, message_box
from config import get_config, save_config, get_config_all, get_rank
from eventManager import event_manager
from eventManager import set_event_penetration
from startSceneBtn import StartSceneBtn
from sceneManager import scene_manager
from webbrowser import open

__all__ = [
    "start_menu_scene",
]

# FPS预设列表d
FPS_PRESET = [30, 60, 120, 240]
# 地图大小
MAP_SIZE_PRESET = [[10, 10], [15, 15], [20, 20], [30, 30], [40, 40], [50, 50]]

screen_width = get_config("width")
screen_height = get_config("height")
game_version = get_config("version")

setting_ui_background_img = pygame.image.load("resource/ui_background.png")
rank_ui_background_img = pygame.image.load("resource/ui_rank.png")
create_img = pygame.image.load("resource/create.jpg")

font_path = "resource/font.ttf"

# 音频模块初始化
pygame.mixer.init()
hover_sound_effect = pygame.mixer.Sound("resource/btn_sound effect.mp3")

# 注册自定义事件，防止pygame自带事件来不及更新
event_manager.register_event("打开开始游戏")
event_manager.register_event("打开设置")
event_manager.register_event("打开致谢")
event_manager.register_event("打开排行")

def start_menu_scene(screen: pygame.Surface) -> tuple[list[StartSceneBtn], pygame.Surface]:
    """
    开始菜单场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """

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
    switch_text = uiBase.UIBase(screen, 400, 550, (0,0), text="欢迎", font_size=28, font_color=(125, 125, 125), font_family = "resource/font.ttf", user_font_family=True, center_anchor = True)
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
    btn_create.mouse_up(lambda event, args: open_create(screen, btn_create))
    # 退出按钮
    btn_exit = StartSceneBtn(screen, -52, screen_height - 100, (200, 70), text = "退出", font_size = 22)
    btn_exit_img = pygame.image.load("resource/btn_exit.png")

    # 忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_enter(event: pygame.event.Event, option):
        btn_exit.set_background_image(btn_exit_img)
        switch_img_surface.set_background_image(btn_exit_switch_img)
        switch_text.set_text(content="你真要狠心离开吗")

    # 可以忽略形参类型检查
    # noinspection PyUnusedLocal
    def btn_exit_up(event: pygame.event.Event, option):
        res = message_box("太狠心了", "要离开了吗？")
        if res:
            pygame.quit()
            sys.exit()


    btn_exit.mouse_enter(btn_exit_enter)
    btn_exit.mouse_up(btn_exit_up)
    # 版本号
    version = uiBase.UIBase(screen, screen_width - 118, screen_height - 40, (0,0), text = game_version, font_size = 18,font_family = font_path,user_font_family = True)
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

def open_setting(screen: pygame.Surface, btn: StartSceneBtn):
    """
    打开设置UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = scene_manager.FPS_CLOCK
        # 发送一个打开设置的事件，间接更新渲染视图
        event_manager.post_event("打开设置")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        setting_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color = (0, 0, 0))
        # 创建一个背景图片
        setting_ui = uiBase.UIBase(screen, 100, -30, (600,800))
        setting_ui.set_background_image(setting_ui_background_img)
        # 加载设置选项操作的图片
        btn_right_arrow_img = pygame.image.load("resource/right.png")
        btn_left_arrow_img = pygame.image.load("resource/left.png")
        # 背景图片设为遮罩子节点，方便管理
        setting_ui_mask.children.append(setting_ui)
        # 创建一个关闭设置UI的函数
        def close_setting_ui(event, option):
            if "mouse_btn" in option and not option["mouse_btn"] == event.button:
                return
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {} or not event:
                pass
            btn.has_open_ui = False
            # 保存配置
            save_config()
            # 淡出
            setting_ui_mask.transition_opacity(0, 0.1, fps_clock, children_together = False).then(lambda **options: setting_ui_mask.close())
            setting_ui.transition_opacity(0, 0.2, fps_clock)
        # 开启遮罩的键盘事件
        setting_ui_mask.enabled_keyboard_event = True
        # 将背景图片的鼠标事件开启事件穿透
        setting_ui.mouse_up(lambda event,options: set_event_penetration(event,True))
        # 绑定鼠标右键点击关闭设置UI
        setting_ui_mask.mouse_up(close_setting_ui, mouse_btn = 3)
        setting_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_setting_ui)

        # =========================================创建设置UI的具体内容=============================================
        common_option = {"font_size": 25, "font_color": (0, 0, 0), "font_family": "resource/font.ttf", "user_font_family":True}
        map_info = get_config("map_size")
        setting_ui_dict = {
            "玩家名称": ( f"{get_config('player_names')[get_config('player_name_index')]}", "用于排行榜记录" ),
            "窗口大小": ( f"{get_config('width')} x {get_config('height')}", "暂不支持更改" ),
            "游戏帧率": ( f"{get_config('FPS')} FPS", "你玩的不是3A大作" ),
            "地图大小": ( f"{map_info[0]} x {map_info[1]}", "可在配置文件自定义" ),
            "地雷数量": ( f"{get_config('bomb_number')}", "我劝你善良" ),
            "背景音乐": ( f"{int(get_config('volume') * 100)}", "调整背景音乐的音量" )
        }
        ui_num = 0
        # 用于设置选项的提示文本
        setting_ui_tips = uiBase.UIBase(screen, 400, 580, (0, 0), text = "", center_anchor = True,**common_option)
        setting_ui_tips.set_text(font_color = (150,150,150))
        setting_ui.children.append(setting_ui_tips)
        # 生成设置选项的选项和按钮
        for title, content in setting_ui_dict.items():
            # 设置标题
            setting_info_title = uiBase.UIBase(screen, 250, 230 + ui_num * 50, (0, 0), text = title, **common_option)
            # 设置内容
            setting_info = uiBase.UIBase(screen, 500, 230 + ui_num * 50, (0, 0), text = content[0], **common_option)
            setting_info_title.enabled_event = False
            setting_info.opacity = 0
            setting_info_title.opacity = 0
            if title == "玩家名称":
                setting_info.name = get_config('player_names')[get_config('player_name_index')]
            else:
                setting_info.name = title
            # 扩大判定区域，使得可以按到箭头按钮
            setting_info.rect.width += 80
            size = setting_info.rect.size
            setting_info.move_by(-int( size[0]/2 ),0)
            pos_x_r = int( 483 + size[0] / 2)
            pos_x_l = int(515 - size[0] / 2)
            pos_y = int( 244 + ui_num * 50 )
            # 右箭头按钮
            btn_right_arrow = uiBase.UIBase(screen, pos_x_r, pos_y, (20, 20), center_anchor = True)
            btn_right_arrow.set_background_image(btn_right_arrow_img)
            # 左箭头按钮
            btn_left_arrow = uiBase.UIBase(screen, pos_x_l, pos_y, (20, 20), center_anchor = True)
            btn_left_arrow.set_background_image(btn_left_arrow_img)
            btn_left_arrow.display = False
            btn_right_arrow.display = False
            # 不允许和父元素一起透明度过渡
            btn_left_arrow.allow_opacity_transition_follow_parent = False
            btn_right_arrow.allow_opacity_transition_follow_parent = False
            # 绑定按钮和选项的事件
            setting_info.mouse_enter(setting_info_mouse_enter,btn = (btn_right_arrow,btn_left_arrow), tips = setting_ui_tips, tips_text = content[1],info = setting_info,title = title)
            setting_info.mouse_leave(setting_info_mouse_leave, btn = (btn_right_arrow, btn_left_arrow))
            setting_info.mouse_up(setting_info_mouse_up, btn = (btn_right_arrow,btn_left_arrow), tips = setting_ui_tips, info = setting_info,title = title)
            btn_right_arrow.mouse_up(setting_right_arrow_mouse_up, btn = btn_right_arrow, info = setting_info, title = title)
            btn_right_arrow.mouse_down(setting_arrow_mouse_down, btn = btn_right_arrow)
            btn_right_arrow.mouse_enter(setting_arrow_mouse_enter, btn = btn_right_arrow)
            btn_right_arrow.mouse_leave(setting_arrow_mouse_leave, btn = btn_right_arrow, info = setting_info, title = title)
            btn_left_arrow.mouse_up(setting_left_arrow_mouse_up, btn = btn_left_arrow, info = setting_info, title = title)
            btn_left_arrow.mouse_down(setting_arrow_mouse_down, btn = btn_left_arrow)
            btn_left_arrow.mouse_enter(setting_arrow_mouse_enter, btn = btn_left_arrow)
            btn_left_arrow.mouse_leave(setting_arrow_mouse_leave, btn = btn_left_arrow, info = setting_info, title = title)
            # 设置事件穿透，防止上下层级的事件循环传递导致鬼畜
            btn_right_arrow.enabled_event_penetration = True
            btn_left_arrow.enabled_event_penetration = True
            setting_info.children.append(btn_right_arrow)
            setting_info.children.append(btn_left_arrow)
            setting_ui.children.append(setting_info_title)
            setting_ui.children.append(setting_info)
            ui_num += 1
        # =======================================================================================================
        # 淡入效果
        setting_ui_mask.opacity = 0
        setting_ui.opacity = 0
        # 预加载情况下，必须先把子节点推入children渲染列表中，children_together这个参数才有效
        setting_ui_mask.transition_opacity(70, 0.1, fps_clock, children_together = False)
        setting_ui.transition_opacity(255, 0.15, fps_clock)
        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(setting_ui_mask)

# 箭头按钮进入函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_enter(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

# 箭头按钮离开函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_leave(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1, 1, 0.05)
    setting_info = option["info"]
    if not setting_info.name == "未命名":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# 箭头按钮按下函数
# noinspection PyUnusedLocal
def setting_arrow_mouse_down(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1.3, 1.3, 0.05)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


# 右箭头按钮鼠标抬起函数
def setting_right_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | str]):
    # 通知父级已捕获到事件
    event.has_catch = True
    btn = option["btn"]
    setting_info = option["info"]
    btn.enabled_event = True
    title = option["title"]
    btn.transition_scale(1, 1, 0.05)
    if title == "窗口大小":
        pass
    elif title == "游戏帧率":
        index = FPS_PRESET.index(get_config("FPS"))
        if index + 1 < len(FPS_PRESET):
            now_fps = FPS_PRESET[index + 1]
            setting_info.set_text(str(now_fps) + " FPS")
            get_config_all()["FPS"] = now_fps
            scene_manager.FPS_CLOCK = 1 / now_fps

    elif title == "地图大小":
        index = MAP_SIZE_PRESET.index(get_config("map_size"))
        if index + 1 < len(MAP_SIZE_PRESET):
            now_map_size = MAP_SIZE_PRESET[index + 1]
            setting_info.set_text(f"{now_map_size[0]} x {now_map_size[1]}")
            get_config_all()["map_size"] = now_map_size


    elif title == "地雷数量":
        now_bomb_number = get_config("bomb_number") + 1
        if now_bomb_number == 0:
            now_bomb_number = 1
        setting_info.set_text(str(now_bomb_number))
        get_config_all()["bomb_number"] = now_bomb_number

    elif title == "背景音乐":
        now_volume = get_config("volume")
        now_volume = round(now_volume + 0.1,1)
        if now_volume <= 1:
            setting_info.set_text(str(int(now_volume*100)))
            get_config_all()["volume"] = now_volume
            pygame.mixer.music.set_volume(now_volume)

    elif title == "玩家名称":
        player_names = get_config("player_names")
        name_index = player_names.index(setting_info.name)
        if name_index - 1 >= 0:
            name = player_names[name_index - 1]
            setting_info.set_text(name)
            setting_info.name = name
            get_config_all()["player_name_index"] = name_index - 1

# 左箭头按钮鼠标抬起函数
def setting_left_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | str]):
    # 通知父级已捕获到事件
    event.has_catch = True
    btn = option["btn"]
    btn.enabled_event = True
    setting_info = option["info"]
    title = option["title"]
    btn.transition_scale(1, 1, 0.05)
    if title == "窗口大小":
        pass
    elif title == "游戏帧率":
        index = FPS_PRESET.index(get_config("FPS"))
        if index - 1 >= 0:
            now_fps = FPS_PRESET[index - 1]
            setting_info.set_text(str(now_fps) + " FPS")
            get_config_all()["FPS"] = now_fps
            scene_manager.FPS_CLOCK = 1 / now_fps

    elif title == "地图大小":
        index = MAP_SIZE_PRESET.index(get_config("map_size"))
        if index - 1 >= 0:
            now_map_size = MAP_SIZE_PRESET[index - 1]
            setting_info.set_text(f"{now_map_size[0]} x {now_map_size[1]}")
            get_config_all()["map_size"] = now_map_size

    elif title == "地雷数量":
        now_bomb_number = get_config("bomb_number") - 1
        if now_bomb_number >= -1:
            if now_bomb_number <= 0:
                now_bomb_number = -1
                setting_info.set_text("∞")
            else:
                setting_info.set_text(str(now_bomb_number))
            get_config_all()["bomb_number"] = now_bomb_number

    elif title == "背景音乐":
        now_volume = get_config("volume")
        now_volume = round(now_volume - 0.1,1)
        if now_volume >= 0:
            setting_info.set_text(str(int(now_volume*100)))
            get_config_all()["volume"] = now_volume
            pygame.mixer.music.set_volume(now_volume)

    elif title == "玩家名称":
        player_names = get_config("player_names")
        name_index = player_names.index(setting_info.name)
        if name_index + 1 < len(player_names):
            name = player_names[name_index + 1]
            setting_info.set_text(name)
            setting_info.name = name
            get_config_all()["player_name_index"] = name_index + 1


def setting_info_mouse_up(event: pygame.event.Event, option: dict[str, tuple[uiBase.UIBase] | str | uiBase.UIBase]):
    setting_info = option["info"]
    title = option["title"]
    tips = option["tips"]
    btn_right_arrow: uiBase.UIBase = option["btn"][0]
    btn_left_arrow: uiBase.UIBase = option["btn"][1]
    btn_right_arrow.opacity = 255
    btn_left_arrow.opacity = 255
    btn_left_arrow.enabled_event = True
    btn_right_arrow.enabled_event = True

    if title == "窗口大小":
        btn_right_arrow.opacity = 80
        btn_left_arrow.opacity = 80
        btn_left_arrow.enabled_event = False
        btn_right_arrow.enabled_event = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "游戏帧率":
        now_fps = get_config("FPS")
        if now_fps == 30:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_fps == 240:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "地图大小":
        now_map_size = get_config("map_size")
        if now_map_size not in MAP_SIZE_PRESET:
            return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if now_map_size == [10, 10]:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_map_size == [50, 50]:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "地雷数量":
        now_bomb_number = get_config("bomb_number")
        if now_bomb_number == -1:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            tips.set_text("绝境之中仍有一线生机")
        else:
            tips.set_text("我劝你善良")

    elif title == "背景音乐":
        now_volume = get_config("volume")
        if now_volume == 0:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_volume == 1:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "玩家名称":
        tips.set_text("用于排行榜记录")
        if get_config("player_name_index") == 0:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if setting_info.name == "未命名":
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            tips.set_text("点击新建名称")
            if not hasattr(event, "has_catch"):
                create_input_box("新建名称",setting_info = setting_info, callback = change_setting_info_name)

def change_setting_info_name(setting_info: uiBase.UIBase, name: str):
    if name:
        player_names: list = get_config("player_names")
        if name in player_names:
            setting_info.set_text(font_color = (255,0,0))
            return setting_info.set_text("名称已存在")
        player_names.insert(0, name)
        setting_info.set_text(name,font_color = (0,0,0))
        setting_info.name = name
        get_config_all()["player_name_index"] = 0


# 设置选项操作鼠标进入时
# noinspection PyUnusedLocal
def setting_info_mouse_enter(event: pygame.event.Event, option: dict[str, tuple[uiBase.UIBase] | str | uiBase.UIBase]):
    btn_right_arrow: uiBase.UIBase = option["btn"][0]
    btn_left_arrow: uiBase.UIBase = option["btn"][1]
    setting_info = option["info"]
    tips = option["tips"]
    title = option["title"]
    tips.set_text(option["tips_text"])
    btn_left_arrow.display = True
    btn_right_arrow.display = True
    btn_left_arrow.enabled_event = True
    btn_right_arrow.enabled_event = True
    btn_left_arrow.opacity = 255
    hover_sound_effect.play()
    if title == "玩家名称":
        if get_config("player_name_index") == 0:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if setting_info.name == "未命名":
            if len(get_config("player_names")) > 1:
                btn_left_arrow.opacity = 80
                btn_left_arrow.enabled_event =False
            else:
                btn_left_arrow.display = False
                btn_right_arrow.display = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            tips.set_text("点击新建名称")

    elif title == "窗口大小":
        btn_left_arrow.enabled_event =False
        btn_right_arrow.enabled_event = False
        btn_right_arrow.opacity = 80
        btn_left_arrow.opacity = 80

    elif title == "游戏帧率":
        now_fps = get_config("FPS")
        if now_fps == 30:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_fps == 240:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "地图大小":
        now_map_size = get_config("map_size")
        # 自定义地图
        if now_map_size not in MAP_SIZE_PRESET:
            btn_left_arrow.display = False
            btn_right_arrow.display = False
            tips.set_text("自定义地图")
            return
        if now_map_size == [10, 10]:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_map_size == [50, 50]:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif title == "地雷数量":
        now_bomb_number = get_config("bomb_number")
        if now_bomb_number == -1:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            tips.set_text("绝境之中仍有一线生机")

    elif title == "背景音乐":
        now_volume = get_config("volume")
        if now_volume == 0:
            btn_left_arrow.opacity = 80
            btn_left_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif now_volume == 1:
            btn_right_arrow.opacity = 80
            btn_right_arrow.enabled_event = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# 设置选项操作鼠标离开时
# noinspection PyUnusedLocal
def setting_info_mouse_leave(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn_left_arrow, btn_right_arrow = option["btn"]
    btn_left_arrow.display = False
    btn_right_arrow.display = False
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

press_sound_effect = pygame.mixer.Sound("resource/btn_press_sound_effect.mp3")
press_sound_effect.set_volume(0.2)

def open_rank(screen: pygame.Surface,btn: StartSceneBtn):
    """
    打开排行榜UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = scene_manager.FPS_CLOCK
        # 初始化地图信息切换按钮
        rank_default = get_config("rank_default")
        rank_default_text = str(rank_default[0]) + " x " + str(rank_default[1])
        # 按钮加载图片并初始化按钮
        btn_right_arrow_img = pygame.image.load("resource/right.png")
        btn_left_arrow_img = pygame.image.load("resource/left.png")
        btn_right_arrow = uiBase.UIBase(screen, 585, 162, (25, 25), center_anchor = True)
        btn_right_arrow.set_background_image(btn_right_arrow_img)
        btn_left_arrow = uiBase.UIBase(screen, 455, 162, (25, 25), center_anchor = True)
        btn_left_arrow.set_background_image(btn_left_arrow_img)
        btn_left_arrow.opacity = 0
        btn_right_arrow.opacity = 0
        # 设定地图信息显示
        if not rank_default in MAP_SIZE_PRESET:
            rank_default_text = "自定义"
            btn_right_arrow.display = False
        elif rank_default == [10, 10]:
            btn_left_arrow.display = False

        rank_map_info = uiBase.UIBase(screen, 521, 160, (0,0), text = rank_default_text, font_size = 27, user_font_family = True, font_family = font_path, center_anchor = True)
        # 绑定事件
        btn_left_arrow.mouse_down(rank_right_arrow_mouse_down,btn = btn_left_arrow)
        btn_right_arrow.mouse_down(rank_left_arrow_mouse_down, btn = btn_right_arrow)

        btn_right_arrow.mouse_leave(rank_arrow_mouse_leave, btn = btn_right_arrow)
        btn_left_arrow.mouse_leave(rank_arrow_mouse_leave, btn = btn_left_arrow)
        btn_right_arrow.mouse_enter(rank_arrow_mouse_enter, btn = btn_right_arrow)
        btn_left_arrow.mouse_enter(rank_arrow_mouse_enter, btn = btn_left_arrow)

        # 发送一个打开设置的事件，间接更新渲染视图
        event_manager.post_event("打开设置")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        rank_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color = (0, 0, 0))
        # 创建一个背景图片
        rank_ui = uiBase.UIBase(screen, 160, 40, (500,700))
        rank_ui.set_background_image(rank_ui_background_img)

        # 背景图片设为遮罩子节点，方便管理
        rank_ui_mask.children.append(rank_ui)
        # 按钮设置为背景图片子节点
        rank_ui.children.append(btn_right_arrow)
        rank_ui.children.append(btn_left_arrow)
        rank_ui.children.append(rank_map_info)
        # 创建一个关闭设置UI的函数
        def close_rank_ui(event ,option):
            # 判断是否是指定鼠标按钮按下的
            if "mouse_btn" in option and not option["mouse_btn"] == event.button:
                return
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {} or not event:
                pass
            btn.has_open_ui = False
            save_config()
            # 淡出
            rank_ui_mask.transition_opacity(0, 0.1, fps_clock, children_together = False).then(lambda **options: rank_ui_mask.close())
            rank_ui.transition_opacity(0, 0.2, fps_clock)
        # 开启遮罩的键盘事件
        rank_ui_mask.enabled_keyboard_event = True
        # 将背景图片的鼠标事件开启事件穿透
        rank_ui.mouse_up(lambda event, options: set_event_penetration(event, True))
        rank_ui_mask.mouse_up(close_rank_ui, mouse_btn = 3)
        rank_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_rank_ui)
        # ==========================================UI子节点渲染====================================================
        # 排行榜列表透明区域，方便刷新绘制区域的工具UI
        rank_ui_list = uiBase.UIBase(screen, 0, 0, (0, 0))
        rank_ui_list.enabled_event = False
        rank_ui.children.append(rank_ui_list)
        # 排行榜顶部显示的提示：排名、玩家名、地雷数、时间
        rank_ui_pre = uiBase.UIBase(screen, 200, 200, (0,0),text = "排名       玩家名       地雷数      时间", font_size = 20, user_font_family = True, font_family = font_path)
        rank_ui.children.append(rank_ui_pre)
        update_rank(screen, rank_ui_list, rank_ui_has_open = False)
        # 继续绑定一波事件
        btn_left_arrow.mouse_up(rank_left_arrow_mouse_up, btn = (btn_left_arrow, btn_right_arrow), text = rank_map_info, screen = screen, rank_ui = rank_ui_list)
        btn_right_arrow.mouse_up(rank_right_arrow_mouse_up, btn = (btn_left_arrow, btn_right_arrow), text = rank_map_info, screen = screen, rank_ui = rank_ui_list)
        # ========================================================================================================
        # 淡入效果
        rank_ui_pre.opacity = 0
        rank_ui_list.opacity = 0
        rank_map_info.opacity = 0
        rank_ui_mask.opacity = 0
        rank_ui.opacity = 0
        rank_ui_mask.transition_opacity(70, 0.1, fps_clock, children_together = False)
        rank_ui.transition_opacity(255, 0.15, fps_clock)
        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(rank_ui_mask)

# noinspection PyUnusedLocal
def rank_right_arrow_mouse_down(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1.2, 1.2, 0.05)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    press_sound_effect.play()

# noinspection PyUnusedLocal
def rank_left_arrow_mouse_down(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1.2, 1.2, 0.05)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    press_sound_effect.play()

# noinspection PyUnusedLocal
def rank_left_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | pygame.Surface]):
    left_btn, right_btn= option["btn"]
    text = option["text"]
    screen = option["screen"]
    rank_ui_list = option["rank_ui"]
    left_btn.transition_scale(1, 1, 0.05)
    rank_default = get_config("rank_default")
    if rank_default in MAP_SIZE_PRESET:
        now_index = MAP_SIZE_PRESET.index(rank_default) - 1
        # 抵达最左侧
        if now_index == 0:
            left_btn.display = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        text.set_text(f"{MAP_SIZE_PRESET[now_index][0]} x {MAP_SIZE_PRESET[now_index][1]}")
        get_config_all()["rank_default"] = MAP_SIZE_PRESET[now_index]
        update_rank(screen, rank_ui_list)
    else:
        # 从最右侧点击
        right_btn.display = True
        now_index = len(MAP_SIZE_PRESET) - 1
        text.set_text(f"{MAP_SIZE_PRESET[now_index][0]} x {MAP_SIZE_PRESET[now_index][1]}")
        get_config_all()["rank_default"] = MAP_SIZE_PRESET[now_index]
        update_rank(screen, rank_ui_list)

# noinspection PyUnusedLocal
def rank_right_arrow_mouse_up(event: pygame.event.Event, option: dict[str, uiBase.UIBase | pygame.Surface]):
    left_btn, right_btn = option["btn"]
    text = option["text"]
    screen = option["screen"]
    rank_ui_list = option["rank_ui"]
    right_btn.transition_scale(1, 1, 0.05)
    rank_default = get_config("rank_default")
    if rank_default in MAP_SIZE_PRESET:
        now_index = MAP_SIZE_PRESET.index(rank_default) + 1
        if now_index == len(MAP_SIZE_PRESET):
            right_btn.display = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            text.set_text("自定义")
            get_config_all()["rank_default"] = "自定义"
            update_rank(screen, rank_ui_list)

        else:
            if now_index == 1:
                left_btn.display = True
            text.set_text(f"{MAP_SIZE_PRESET[now_index][0]} x {MAP_SIZE_PRESET[now_index][1]}")
            get_config_all()["rank_default"] = MAP_SIZE_PRESET[now_index]
            update_rank(screen, rank_ui_list)


# noinspection PyUnusedLocal
def rank_arrow_mouse_enter(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    btn.transition_scale(1.1, 1.1)

# noinspection PyUnusedLocal
def rank_arrow_mouse_leave(event: pygame.event.Event, option: dict[str, uiBase.UIBase]):
    btn = option["btn"]
    btn.transition_scale(1, 1, 0.05)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def format_seconds(seconds):
    """
    将秒数转换为分秒的格式。
    :param : 秒数
    """
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


def update_rank(screen: pygame.Surface, rank_ui: uiBase.UIBase, rank_ui_has_open: bool = True):
    """
    创建一个根据地图大小所产生的排行榜的UI
    :param screen: 绘制在的surface对象
    :param rank_ui: 添加到某个UIBase作为其子节点
    :parameter rank_ui_has_open: (可选) 排行榜是否已经打开，如果未打开内容会设置为透明
    :return:
    """
    rank_ui.children.clear()
    map_size = get_config("rank_default")
    if map_size in MAP_SIZE_PRESET:
        map_size = f"{map_size[0]}x{map_size[1]}"
    else:
        map_size = "自定义"
    # 控制排行榜项目的x轴位置
    rank_list_pos_x = ( 220, 335, 458, 562 )
    rank_list = get_rank()[map_size]
    # 如果排行榜为空
    if not rank_list:
        rank_text = uiBase.UIBase(screen, 400, 380, (0,0), text = "暂无排行榜", font_family = font_path, user_font_family = True, enabled_event = False, center_anchor = True, font_size = 25)
        rank_ui.children.append(rank_text)
        if not rank_ui_has_open:
            rank_text.opacity = 0
        return
    # 初始化排行索引
    num = 0
    for rank_list_info in rank_list:
        rank_num = uiBase.UIBase(screen, rank_list_pos_x[0], 255 + num * 35, (0, 0), text = str(num + 1), font_family = font_path, user_font_family = True, enabled_event = False, center_anchor = True, font_size = 25)
        rank_name = uiBase.UIBase(screen, rank_list_pos_x[1], 255 + num * 35, (0, 0), text = rank_list_info[1], font_family = font_path, user_font_family = True, enabled_event = False, center_anchor = True, font_size = 25)
        rank_bomb_num = uiBase.UIBase(screen, rank_list_pos_x[2], 255 + num * 35, (0, 0), text = str(rank_list_info[0]), font_family = font_path, user_font_family = True, enabled_event = False, center_anchor = True, font_size = 25)
        rank_time = uiBase.UIBase(screen, rank_list_pos_x[3], 255 + num * 35, (0, 0), text = format_seconds(rank_list_info[2]), font_family = font_path, user_font_family = True, enabled_event = False, center_anchor = True, font_size = 25)
        rank_ui.children.append(rank_num)
        rank_ui.children.append(rank_name)
        rank_ui.children.append(rank_bomb_num)
        rank_ui.children.append(rank_time)
        if not rank_ui_has_open:
            rank_num.opacity = 0
            rank_name.opacity = 0
            rank_bomb_num.opacity = 0
            rank_time.opacity = 0
        num += 1

# noinspection PyUnusedLocal
def open_create(screen: pygame.Surface, btn: StartSceneBtn):
    """
    打开致谢UI
    :param screen: 要绘制的surface
    :param btn: 绑定的按钮
    :return:
    """
    if not btn.has_open_ui:
        # 计算出游戏更新循环周期
        fps_clock = scene_manager.FPS_CLOCK
        # 发送一个打开致谢的事件，间接更新渲染视图
        event_manager.post_event("打开致谢")
        btn.has_open_ui = True
        # 创建半透明的黑色遮罩
        create_ui_mask = uiBase.UIBase(screen, 0, 0, (screen_width, screen_height), color=(0, 0, 0))
        # 创建一个背景图片
        create_ui = uiBase.UIBase(screen, 400, 200, (150, 150), enabled_event = False, center_anchor = True)
        create_ui.set_background_image(create_img, use_circular_mask = True)
        # 背景图片设为遮罩子节点，方便管理
        create_ui_mask.children.append(create_ui)
        # 创建一个关闭创建UI的函数
        def close_create_ui(event, option):
            if "mouse_btn" in option and not option["mouse_btn"] == event.button:
                return
            # 防止这傻逼pycharm给我弹一个未使用形参的警告
            if not option == {} or not event:
                pass
            btn.has_open_ui = False
            # 保存配置
            save_config()
            # 淡出
            create_ui_mask.transition_opacity(0, 0.1, fps_clock, children_together=False).then(lambda **options: create_ui_mask.close())
            create_ui.transition_opacity(0, 0.2, fps_clock)
        # 开启遮罩的键盘事件
        create_ui_mask.enabled_keyboard_event = True
        # 将背景图片的鼠标事件开启事件穿透
        create_ui.enabled_event = False
        # 绑定鼠标右键点击关闭创建UI
        create_ui_mask.mouse_up(close_create_ui, mouse_btn=3)
        create_ui_mask.bind_keyboard_callback(pygame.K_ESCAPE, pygame.KEYUP, close_create_ui)
        create_ui_mask.opacity = 0
        create_ui.opacity = 0

        create_title = uiBase.UIBase(screen, 400, 350, (0,0), text = "游戏开发", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 40, font_color = (255, 255, 255), enabled_event = False)
        create_member = uiBase.UIBase(screen, 400, 400, (0, 0), text = "Ni But Crazy", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 30, font_color = (255, 255, 255))
        create_thank = uiBase.UIBase(screen, 400, 460, (0,0), text = "感谢睿哥的扫雷脚本提供了逻辑基础", font_family = font_path, user_font_family = True, center_anchor = True, font_size = 20, font_color = (255, 255, 255), enabled_event = False)
        create_member.name = "member"
        create_member.opacity = 0
        create_title.opacity = 0
        create_thank.opacity = 0
        create_ui.children.append(create_member)
        create_ui.children.append(create_title)
        create_ui.children.append(create_thank)
        create_member.mouse_enter(lambda event, option: (create_member.set_text(font_color = (150, 150, 205), font_size = 33),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)))
        create_member.mouse_leave(lambda event, option: (create_member.set_text(font_color = (255, 255, 255), font_size = 30),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)))
        create_member.mouse_up(lambda event, option: open("https://github.com/NiButCrazy/SaoLei"))

        create_ui_mask.transition_opacity(200, 0.1, fps_clock, children_together = False)
        create_ui.transition_opacity(255, 1, fps_clock)
        # 把遮罩推入渲染UI列表
        scene_manager.now_scene[0].append(create_ui_mask)
