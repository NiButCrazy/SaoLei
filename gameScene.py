"""
游戏场景
"""

import pygame
import threading
import time

import gameMap
from config import get_config_all, get_config, record_rank, save_rank
from eventManager import event_manager
from inputBox import message_box
from sceneManager import scene_manager
from uiBase import UIBase

# 背景图片的画布，为了调整背景图片的大小和位置
background_surface = pygame.Surface((800,800))
background_surface.fill((255, 255, 255))
# 调整源图片的比例和大小
background_img = pygame.transform.smoothscale(pygame.image.load("resource/background-img2.jpg"),(800,1700))
# 将图片绘制到画布上去
background_surface.blit(background_img,(0,-250))
# 字体路径
font_path = "resource/font.ttf"
# 按钮图片加载
play_img = pygame.image.load("resource/play.png")
pause_img = pygame.image.load("resource/paused.png")
# 游戏背景图片加载
game_background_img = pygame.image.load("resource/game_bg.png")
# 地雷图片加载
bomb_img = pygame.image.load("resource/bomb.png")
sure_bomb_img = pygame.image.load("resource/sure_bomb.png")
not_sure_bomb_img = pygame.image.load("resource/not_sure.png")
# 音效加载
hover_sound_effect = pygame.mixer.Sound("resource/btn_sound effect.mp3")
press_sound_effect = pygame.mixer.Sound("resource/btn_press_sound_effect.mp3")
press_sound_effect.set_volume(0.2)


class TimerThread( threading.Thread ):
    """
    一个定时器线程
    """
    def __init__(self, ui: UIBase = None):
        super().__init__()
        self.seconds = 0
        self.seconds_format = "00:00"
        self.stop = True
        self.ui = ui
        # 设为守护线程
        self.daemon = True
        # 绑定的按钮
        self.btn: UIBase | None = None

    def run(self):
        while True:
            time.sleep( 1 )
            if self.stop:continue
            self.seconds += 1
            self.format_seconds(self.seconds)
            if not self.ui is None:
                self.ui.set_text(self.seconds_format)

    def format_seconds(self,seconds):
        """
        将秒数转换为分秒的格式。
        :param : 秒数
        """
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.seconds_format = f"{minutes:02d}:{seconds:02d}"

    def stop_timer(self):
        self.stop = True


def start_game_scene(screen: pygame.Surface) -> tuple[list[UIBase], pygame.Surface]:
    """
    游戏场景
    :param screen: 想要绘制的Surface对象
    :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
    """
    # 获取配置主题
    config = get_config_all()

    # 基础信息文本
    base_info_text = "玩家 {0}   地图 {1} x {2}   时间".format(config["player_names"][0], config["map_size"][0], config["map_size"][1])
    timer = UIBase(screen, 550, 13, (0, 0), (255, 255, 255), "00:00", 23, (0, 0, 0), font_path, True,enabled_event = False)
    # 计时器线程
    timer_thread = game_start_time(screen, timer)
    # 基础信息UI
    base_info = UIBase(screen, -50, 0, (800, 50), (255, 255, 255), base_info_text, 23, (0, 0, 0), font_path, True, enabled_event = False)
    # 时间继续与暂停按钮
    play_btn = UIBase(screen,630, 15, (20, 20))
    play_btn.set_background_image(play_img)
    play_btn.opacity = 100
    play_btn.mouse_enter(lambda event, option:(play_btn.transition_opacity(255, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),hover_sound_effect.play()))
    play_btn.mouse_leave(lambda event, option: (play_btn.transition_opacity(100, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)))
    play_btn.mouse_up(play_btn_mouse_up, btn = play_btn, timer_thread = timer_thread)
    timer_thread.btn = play_btn
    play_btn.mouse_down(lambda event, option: (play_btn.transition_scale(1.1, 1.1, 0.1), press_sound_effect.play()))
    play_btn.enabled_event = False
    # 刷新按钮
    refresh_btn = UIBase(screen, 750, 15, (20, 20))
    refresh_btn.set_background_image(path = "resource/refresh.png")
    refresh_btn.opacity = 100
    refresh_btn.mouse_enter(lambda event, option:(refresh_btn.transition_opacity(255, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),hover_sound_effect.play()))
    refresh_btn.mouse_leave(lambda event, option: (refresh_btn.transition_opacity(100, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)))
    refresh_btn.mouse_up(lambda event, option: (load_new_game(game_ui, timer_thread), press_sound_effect.play()))
    refresh_btn.enabled_event = False
    # 返回按钮
    back_btn = UIBase(screen, 25, 27, (30, 30), (255, 255, 255), "", 23, (0, 0, 0), font_path, True,center_anchor = True)
    back_btn.set_background_image(path = "resource/left.png")
    back_btn.opacity = 100
    back_btn.mouse_enter(lambda event, option:(back_btn.transition_opacity(255, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND),hover_sound_effect.play()))
    back_btn.mouse_leave(lambda event, option: (back_btn.transition_opacity(100, 0.0),pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),back_btn.transition_scale(1, 1, 0.05)))
    back_btn.mouse_up(
        lambda event, option: (
            scene_manager.smooth_toggle_scene(screen, "start_menu"),
            scene_manager.ui_dict["btn_start_game"].set_text("继续"),
            back_btn.transition_scale(1, 1, 0.05),
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW),
            play_btn.set_background_image(play_img),
            timer_thread.ui.set_text(font_color = (18,150,219)),
            timer_thread.stop_timer(),
            press_sound_effect.play()
        )
    )
    back_btn.mouse_down(lambda event, option: back_btn.transition_scale(1.1, 1.1, 0.1))
    # 游戏加载渲染区域
    game_ui = UIBase(screen, 75, 75, (650,650))
    game_ui.opacity = 0
    # 开始游戏按钮
    start_game_btn = UIBase(screen, 400, 200, (0, 0), text = "开始游戏", font_size = 30, center_anchor = True, user_font_family = True, font_family = font_path)
    # noinspection PyUnusedLocal
    def start():
        game_ui.transition_opacity(255, 0.5)
        load_new_game(game_ui, timer_thread)
        refresh_btn.enabled_event = True
        play_btn.enabled_event = True
        start_game_btn.close()

    start_game_btn.mouse_enter(lambda event, option: (start_game_btn.set_text(font_size = 33), pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND), hover_sound_effect.play()))
    start_game_btn.mouse_leave(lambda event, option: (pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW), start_game_btn.set_text(font_size = 30)))

    start_game_btn.mouse_up(
        lambda e, a: (
            start_game_btn.transition_opacity(0, 0.5).then(start),
            press_sound_effect.play()
        )
    )
    # UI列表推入
    ui_list = [
        base_info,
        timer,
        back_btn,
        play_btn,
        refresh_btn,
        game_ui,
        start_game_btn
    ]

    # load_new_game(game_ui, timer_thread)
    return ui_list, background_surface

# noinspection PyUnusedLocal
def game_start_time(screen: pygame.Surface, timer: UIBase):
    """
    开始游戏计时
    :param screen: 渲染的画布
    :param timer: 时间UI
    :return:
    """
    timer_thread = TimerThread(timer)
    timer_thread.start()
    return timer_thread

# noinspection PyUnusedLocal
def play_btn_mouse_up(event: pygame.event.Event, option: dict[str, UIBase | TimerThread]):
    """
    游戏时间按钮鼠标抬起回调函数
    :param event: 事件
    :param option: 携带的参数
    :return:
    """
    btn: UIBase = option["btn"]
    time_thread: TimerThread = option["timer_thread"]
    if time_thread.stop:
        time_thread.stop = False
        btn.set_background_image(pause_img)
        time_thread.ui.set_text(font_color = (0, 0, 0))
        event_manager.game_playing = True
    else:
        time_thread.stop = True
        btn.set_background_image(play_img)
        time_thread.ui.set_text(font_color = (18,150,219))
        event_manager.game_playing = False

def load_new_game(ui: UIBase, timer_thread: TimerThread):
    """
    把游戏图像渲染到指定UI上面
    :param ui: 渲染的UI，也就是父级节点
    :param timer_thread: 一个计时器类型
    :return:
    """
    ui.enabled_event = True
    timer_thread.btn.enabled_event = True
    timer_thread.ui.set_text(content = "00:00",font_color = (0, 0, 0))
    timer_thread.seconds = 0
    timer_thread.stop = True
    timer_thread.btn.set_background_image(play_img)
    event_manager.game_playing = False
    map_width, map_height = get_config("map_size")
    block_width, block_height = (0, 0)
    # 设为透明颜色
    map_surface = pygame.Surface((650,650), pygame.SRCALPHA)
    map_surface.fill((255,255,255, 0))
    color_x = 255 / ( map_width + 1 )
    color_y = 255 / ( map_height + 1 )
    if map_width == map_height:
        block_width = 650 / map_width
        block_height = 650 / map_height
    elif map_width > map_height:
        block_width = block_height = 650 / map_width
    elif map_width < map_height:
        block_height = block_width = 650 / map_height

    for y in range(map_height):
        for x in range(map_width):
            block = pygame.Surface((block_width - 1, block_height - 1), pygame.SRCALPHA)
            block.fill((x * color_x, y * color_y, 255))
            map_surface.blit(block, (x * block_width,y * block_height))

    ui.set_background_image(map_surface)
    game_map = gameMap.GameMap(map_width, map_height, get_config("bomb_number"),timer_thread)
    ui.mouse_down(get_list_pos_from_ui_pos, block_size = (block_width, block_height), game_map = game_map, ui = ui, timer_thread = timer_thread)
    # 如果游戏是第一次开始，则淡化背景图片
    if not event_manager.game_has_started:
        fade_out_bg_img(2)
        event_manager.game_has_started = True

block_type_color = {
    "emtpy": (245, 245, 245),
    "1" : (100, 130, 250),
    "2" : (50, 150, 50),
    "3" : (255, 150, 80),
    "4" : (255, 0, 0),
    "5" : (255, 0, 0),
    "6" : (255, 0, 0),
    "7" : (255, 0, 0),
    "8" : (255, 0, 255),
}

def get_list_pos_from_ui_pos(event: pygame.event.Event, option):
    """
    获取鼠标位置并映射成列表坐标，然后进行相应的渲染
    :param event:
    :param option:
    :return:
    """
    # 暂停时点击任意地图处继续游戏
    if not event_manager.game_playing:
        time_thread = option["timer_thread"]
        time_thread.stop = False
        time_thread.btn.set_background_image(pause_img)
        time_thread.ui.set_text(font_color = (0, 0, 0))
    event_manager.game_playing = True

    block_width, block_height = option["block_size"]
    game_map:gameMap.GameMap = option["game_map"]
    ui:UIBase = option["ui"]
    map_surface:pygame.Surface = ui.get_blit_background_image()
    pos_x = int( (event.pos[0] - 75) // block_width)
    pos_y = int( (event.pos[1] - 75) // block_height)
    if game_map.judge_ground[pos_y][pos_x] == 11:
        return
    if event.button == 1: # 鼠标左键
        game_map.detection(pos_y,pos_x)
        for update_block in game_map.update_block:
            x = update_block[0]
            y = update_block[1]
            block_type = str(update_block[2])
            if block_type == "empty":
                block = pygame.Surface((block_width - 1, block_height - 1), pygame.SRCALPHA)
                block.fill((245, 245, 245))
                map_surface.blit(block, (x * block_width,y * block_height))
            elif block_type == "bomb":
                bomb = pygame.transform.smoothscale(bomb_img,(block_width * 4/5, block_height * 4 / 5))
                block = pygame.Surface((block_width - 1, block_height - 1), pygame.SRCALPHA)
                block.fill((245, 245, 245))
                map_surface.blit(block, (x * block_width,y * block_height))
                map_surface.blit(bomb, (x * block_width + block_width / 10, y * block_height + block_height / 10))
            else:
                block = pygame.Surface((block_width - 1, block_height - 1), pygame.SRCALPHA)
                block.fill((245, 245, 245))
                map_surface.blit(block, (x * block_width,y * block_height))
                font = pygame.font.Font(font_path, int(block_width)).render(block_type, True, block_type_color[block_type])
                width = font.get_width()
                map_surface.blit(font, (x * block_width + width/2, y * block_height - 2))
        game_map.update_block.clear()
        if game_map.ground[pos_y][pos_x] == 9:
            message_box("游戏结束", "你🐎炸了", "info", True)
            ui.enabled_event = False
            time_thread = option["timer_thread"]
            time_thread.stop = True
            time_thread.btn.set_background_image(play_img)
            time_thread.btn.enabled_event = False
            time_thread.ui.set_text(font_color = (18, 150, 219))
            return

    elif event.button == 3: # 鼠标右键
        block_state = game_map.has_clicked_state[pos_y][pos_x]
        color_x = 255 / ( game_map.width + 1 )
        color_y = 255 / ( game_map.height + 1 )
        block = pygame.Surface((block_width - 1, block_height - 1), pygame.SRCALPHA)
        block.fill((pos_x * color_x, pos_y * color_y, 255))
        map_surface.blit(block, (pos_x * block_width,pos_y * block_height))
        game_map.has_clicked_state[pos_y][pos_x] = "empty"
        if block_state == "empty":
            bomb = pygame.transform.scale(sure_bomb_img,(block_width * 4/5, block_height * 4 / 5))
            map_surface.blit(bomb, (pos_x * block_width + block_width / 10, pos_y * block_height + block_height / 10))
            game_map.has_clicked_state[pos_y][pos_x] = "sure"
            game_map.sure_num.append((pos_y, pos_x))
            if game_map.ground[pos_y][pos_x] == 9:
                game_map.bomb_found_num += 1
                if game_map.bomb_found_num == game_map.bomb_num and len(game_map.sure_num) == game_map.bomb_num:
                    message_box("圆满完成", "恭喜您取得了游戏胜利！", "info", True)
                    rank = record_rank(game_map.timer.seconds)
                    save_rank(rank)
                    ui.enabled_event = False
                    time_thread:TimerThread = option["timer_thread"]
                    time_thread.stop = True
                    time_thread.btn.set_background_image(play_img)
                    time_thread.btn.enabled_event = False
                    time_thread.ui.set_text(font_color = (18, 150, 219))

        elif block_state == "sure":
            bomb = pygame.transform.scale(not_sure_bomb_img,(block_width * 4/5, block_height * 4 / 5))
            map_surface.blit(bomb, (pos_x * block_width + block_width / 10, pos_y * block_height + block_height / 10))
            game_map.has_clicked_state[pos_y][pos_x] = "not sure"
            game_map.sure_num.remove((pos_y, pos_x))
            if game_map.ground[pos_y][pos_x] == 9:
                game_map.bomb_found_num -= 1


def __fade_out_bg_img(duration: float = 0.5):
    fps_clock = scene_manager.FPS_CLOCK
    step = duration / fps_clock
    now_step = 0
    fade_step = 255 / step
    while now_step < step:
        now_step += 1
        background_surface.fill((255, 255, 255))
        background_img.set_alpha(255 - now_step * fade_step)
        background_surface.blit(background_img, (0,-250))
        time.sleep(fps_clock)
    background_surface.fill((255, 255, 255))
    background_img.set_alpha(0)
    background_surface.blit(background_img, (0,-250))

def fade_out_bg_img(duration: float = 0.5):
    """
    背景图片淡出
    :param duration:
    :return:
    """
    thread = threading.Thread(target = __fade_out_bg_img, args = (duration,))
    thread.daemon = True
    thread.start()