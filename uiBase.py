"""
自定义一个pygame的UI基类
"""
from typing import Callable,Any

import pygame

from sceneManager import scene_manager


class Timer:
    """
    用于某些计时函数完成后的操作
    """

    def __init__(self):
        self.__callback = None
        self.__option = {}

    def then(self, callback: callable, **option):
        """
        用于某些计时函数完成后调用回调函数
        :param callback: 回调函数
        :param option: 回调函数的参数
        :return:
        """
        self.__callback = callback
        self.__option = option

    def use_callback(self):
        if not self.__callback is None:
            return self.__callback(**self.__option)


class UIBase:
    """
    UI基类，包含了最基本的UI样式、事件消息传递与绑定和过渡动画
    """
    def __init__(self,
                 screen: pygame.Surface,
                 x: int,
                 y: int,
                 size: tuple,
                 color: tuple = (255,255,255),
                 text: str = "",
                 font_size: int = 16,
                 font_color:tuple | str = (0,0,0),
                 font_family: str = "Microsoft YaHei",
                 user_font_family = False
                 ):
        """
        定义了一个UI最基本的文本、位置、大小
        :param screen: 绘制到该Surface
        :param x: UI的位置x
        :param y: UI的位置y
        :param size: UI的大小(width,height)
        :param color: (可选) UI上的背景颜色
        :param text: (可选) UI上的文本
        :param font_size: (可选) UI上的文本字体大小
        :param text: (可选) UI上的文本字体颜色
        :param font_family: (可选) 字体
        :param user_font_family: (可选) 是否使用用户自定义字体文件
        """

        # 鼠标按下回调函数
        self.__mouse_down_callback = lambda event, option: print(self.name)
        self.__mouse_down_callback_args = {}
        # 鼠标抬起回调函数
        self.__mouse_up_callback = lambda event, option: Any # print("鼠标抬起")
        self.__mouse_up_callback_args = {}
        # 鼠标进入UI回调函数
        self.__mouse_enter_callback = lambda event, option: Any # print("鼠标进入")
        self.__mouse_enter_callback_args = {}
        # 鼠标进入UI回调函数
        self.__mouse_leave_callback = lambda event, option: Any # print("鼠标离开")
        self.__mouse_leave_callback_args = {}
        # 基本参数
        self.name = "-1" # 只作为标识符ID，不可重复
        self.screen = screen
        self.opacity = 255 # 背景颜色透明度
        self.content = text
        self.font_color = font_color
        self.font_size = font_size
        self.font_opacity = 255  # 文字透明度
        self.user_font_family = user_font_family # 是否使用用户自定义字体文件
        self.font_family = font_family
        self.text = None # 最终字体surface对象
        self.pos_x = x
        self.pos_y = y
        self.width = size[0] # 实时宽度
        self.height = size[1] # 实时高度
        self.original_width = size[0] # 原始宽度，缩放时这个值不变
        self.original_height = size[1] # 原始高度，缩放时这个值不变
        self.color = color
        self.is_hover = False # 鼠标是否在UI上悬停
        self.enabled_event = True # UI 是否接收事件
        self.enabled_keyboard_event = False # UI 是否接收键盘事件
        self.background_img = None # 记录原始背景图片的变量
        self.__background_img = None # 游戏绘制的是这个图片的变量
        # 缩放过渡各参数
        self.__fps_clock = None
        self.__scale_step = None
        self.__scale_y = 1
        self.__scale_x = 1
        self.__scale_duration = 0.0
        self.__now_scale_duration = 0.0
        self.__scale_step_x = 0
        self.__scale_step_y = 0
        self.__now_scale_step = 0
        # 透明度过渡各参数
        self.__opacity_duration = 0
        self.__dest_opacity = self.opacity
        self.__opacity_step = 0
        self.__opacity_step_distance = 0
        self.__now_opacity_step = 0
        # 缩放过渡动画是否运行中
        self.__transition_scale_running = False
        # 移动过渡动画是否运行中
        self.__transition_move_running = False
        # 透明度过渡动画是否运行中
        self.__transition_opacity_running = False
        # 存储按键事件绑定回调函数的字典
        self.__key_up_event_callback_dict = {}
        self.__key_down_event_callback_dict = {}
        # 绘制区域
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # 时间函数回调列表
        self.__timers = {"opacity":Timer(), "move":Timer(), "scale":Timer()}
        # 子节点列表
        self.children = []
        # 初始化文本
        self.set_text(text,font_color,font_size, self.font_family)

        # # 每次创建类实例时，会将实例推入事件管理器的emit_children列表中
        # eventManager.manager.emit_children.append(self)

    def receive_event(self, event: pygame.event.Event, **option) -> bool:
        """
        接收事件，并给子节点发送事件，且子节点的处理事件函数的时间早于父节点
        :param event: pygame的事件对象
        :param option: 事件所携带的额外参数
        :return: 返回一个布尔值，用于判断是否要把事件往底层图层传递
        """
        if not self.enabled_event:
            return True

        # 记录事件是否被子节点捕获
        children_stop_emit = False

        # 给子节点发送事件
        # 最后渲染的(也就是最顶层的)ui最先接收到事件，防止事件被底层ui吞了，同一个按键事件只会被最顶层的UI处理
        for index in range(len(self.children) - 1, -1, -1):
            if_continue_emit = self.children[index].receive_event(event, **option)
            # 如果已被目标UI截断，则其他UI不再调用的此事件的处理函数
            if not if_continue_emit:
                option["stop_emit"] = True
                children_stop_emit = True

        # 处理键盘输入事件，同一个按键事件只会被最顶层的UI处理
        if self.enabled_keyboard_event and not option["stop_emit"]:
            if event.type == pygame.KEYDOWN:
                if event.key in self.__key_down_event_callback_dict:
                    # 调用绑定的按键函数
                    self.__key_down_event_callback_dict[event.key][0](**self.__key_down_event_callback_dict[event.key][1])
                    return False
                else:
                    return True
            elif event.type == pygame.KEYUP:
                if event.key in self.__key_up_event_callback_dict:
                    # 调用绑定的按键函数
                    self.__key_up_event_callback_dict[event.key][0](**self.__key_up_event_callback_dict[event.key][1])
                    return False
                else:
                    # 如果没有按键冲突，则向下传递
                    return True

        # 如果鼠标在UI内，则将触发以下事件回调函数
        if hasattr(event,"pos") and self.rect.collidepoint(event.pos) and not option["stop_emit"]:
            # 鼠标悬停
            if not self.is_hover:
                self.is_hover = True
                self._mouse_enter(event)
            # 处理鼠标输入事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up(event)

            # 截断事件向下传递
            return False

        else:
            if self.is_hover:
                self.is_hover = False
                self._mouse_leave(event)

            # 事件向下传递
            if children_stop_emit:
                return False
            return True

    def _mouse_down(self, event:pygame.event.Event):
        self.__mouse_down_callback(event,self.__mouse_down_callback_args)

    def mouse_down(self, callback:Callable[[pygame.event.Event, dict[str,Any]],Any], **option):
        """
        绑定鼠标按下时的回调参数
        :param callback: 回调函数
        :param option: (可选) 回调函数的参数
        :return:
        """
        self.__mouse_down_callback = callback
        self.__mouse_down_callback_args = option

    def _mouse_up(self, event:pygame.event.Event):
        self.__mouse_up_callback(event,self.__mouse_up_callback_args)

    def mouse_up(self, callback:Callable[[pygame.event.Event, dict[str,Any]],Any], **option):
        """
        绑定鼠标抬起时的回调参数
        :param callback: 回调函数
        :param option: (可选) 回调函数的参数
        :return:
        """
        self.__mouse_up_callback = callback
        self.__mouse_up_callback_args = option

    def mouse_enter(self, callback:Callable[[pygame.event.Event, dict[str,Any]],Any], **option):
        """
        绑定鼠标进入时的回调参数
        :param callback: 回调函数
        :param option: (可选) 回调函数的参数
        :return:
        """
        self.__mouse_enter_callback = callback
        self.__mouse_enter_callback_args = option

    def _mouse_enter(self, event: pygame.event.Event):
        self.__mouse_enter_callback(event, self.__mouse_enter_callback_args)

    def mouse_leave(self, callback:Callable[[pygame.event.Event, dict[str,Any]],Any], **option):
        """
        绑定鼠标离开时的回调参数
        :param callback: 回调函数
        :param option: (可选) 回调函数的参数
        :return:
        """
        self.__mouse_leave_callback = callback
        self.__mouse_leave_callback_args = option

    def _mouse_leave(self, event: pygame.event.Event):
        self.__mouse_leave_callback(event, self.__mouse_leave_callback_args)

    def update(self, fps_clock):
        """
        游戏更新回调
        :return:
        """
        self.__fps_clock = fps_clock
        self.__transition_scale()
        self.__transition_opacity()
        # 绘制自己（纯矩形图案或者图片）
        if self.background_img is None:
            ui_surface = pygame.Surface(self.rect.size)
            ui_surface.fill(self.color)
            ui_surface.set_alpha(self.opacity)
            self.screen.blit(ui_surface, self.rect)
        else:
            self.__background_img.set_alpha(self.opacity)
            self.screen.blit(self.__background_img, self.rect)
        # 绘制文本
        self.text.set_alpha(self.font_opacity)
        self.screen.blit(self.text, self.text.get_rect(center=self.rect.center))
        # 更新子节点
        for child in self.children:
            child.update(fps_clock)

    def set_text(self, content:str = "", font_color: tuple = (0,0,0), font_size: int = 0, font_family: str = ""):
        """
        设置文本内容、颜色、字号、字体
        :param content: 文本内容
        :param font_color: 颜色
        :param font_size: 字号
        :param font_family: 字体,如果是自定义字体请填写文件路径，并且一定要提前设置user_font_family为True
        :return:
        """
        if not content:
            content = self.content
        if font_color == (0,0,0):
            font_color = self.font_color
        if font_size == 0:
            font_size = self.font_size
        if font_family == "":
            font_family = self.font_family

        if not self.user_font_family:
            self.text = pygame.font.SysFont(font_family,font_size).render(content, True, font_color)
        else:
            self.text = pygame.font.Font(font_family, font_size).render(content, True, font_color)

    def transition_scale(self, scale_x, scale_y, duration: float = 0.0) -> Timer:
        """
        UI的缩放过渡效果
        :param scale_x: x轴缩放倍数
        :param scale_y: y轴缩放倍数
        :param duration: 过渡动画完成时间
        :return:
        """
        # 过渡效果达成时间
        self.__scale_duration = duration
        # 总缩放步数
        self.__scale_step = int( duration / self.__fps_clock )
        # 是否已经处于过渡中
        self.__transition_scale_running = True
        # x轴缩放比例
        self.__scale_x = scale_x
        # x轴缩放步长
        self.__scale_step_x =  ( self.original_width * scale_x - self.width ) / self.__scale_step
        # y轴缩放比例
        self.__scale_y = scale_y
        # y轴缩放步长
        self.__scale_step_y = ( self.original_height * scale_y - self.height ) / self.__scale_step
        # 目前缩放步数
        self.__now_scale_step = 0
        # 方便绑定过渡完成后的回调函数
        return self.__timers["scale"]

    def __transition_scale(self):
        if self.__transition_scale_running:
            if self.__now_scale_step < self.__scale_step:
                self.__now_scale_step += 1
                # 新建两个个变量存储计算结果，节约性能
                step_width = self.width + self.__scale_step_x
                step_height = self.height + self.__scale_step_y
                self.width = step_width
                self.height = step_height
                # 更新rect绘制区域
                self.rect.size = (
                    step_width,
                    step_height
                )
                # 如果存在背景图片则对其缩放
                if self.background_img is not None:
                    self.__background_img = pygame.transform.smoothscale(
                        self.background_img,
                        (step_width, step_height)
                    )
            else:
                # 防止过渡后缩放值有误差
                self.width = self.original_width * self.__scale_x
                self.height = self.original_height * self.__scale_y
                self.__transition_scale_running = False
                self.rect.size = (
                    self.width,
                    self.height
                )
                if self.background_img is not None:
                    self.__background_img = pygame.transform.smoothscale(self.background_img, (self.width, self.height))
                self.__timers["scale"].use_callback()

    def transition_opacity(self, dest_opacity: int, duration: float = 0.0, fps_clock: float = 0.0) -> Timer:
        """
        UI的缩放过渡效果
        :param dest_opacity: 目标透明度（ 0~255 ）
        :param duration: (可选) 过渡动画完成时间
        :param fps_clock: (可选) 游戏更新循环周期，此选项通常用于UI还未被加载进游戏主进程渲染更新中，起到预加载作用
        :return:
        """
        # 过渡效果达成时间
        self.__opacity_duration = duration
        # 目标透明度
        self.__dest_opacity = dest_opacity
        if self.__fps_clock == 0.0:
            fps_clock = self.__fps_clock
        # 总过渡步数
        self.__opacity_step = int( duration / fps_clock )
        # 是否已经处于过渡中
        self.__transition_opacity_running = True
        # 过渡步长
        self.__opacity_step_distance = ( self.opacity - dest_opacity ) / self.__opacity_step
        # 目前过渡步数
        self.__now_opacity_step = 0
        # 方便绑定过渡完成后的回调函数
        return self.__timers["opacity"]

    def __transition_opacity(self):
        if self.__transition_opacity_running:
            if self.__now_opacity_step < self.__opacity_step:
                self.__now_opacity_step += 1
                self.opacity -= self.__opacity_step_distance
            else:
                # 防止过渡后缩放值有误差
                self.opacity = self.__dest_opacity
                self.__transition_opacity_running = False
                self.__timers["opacity"].use_callback()

    def set_background_image(self, image: str | pygame.Surface):
        """
        设置背景图片
        :param image: 接受一个图片路径字符串 或 一个图片的Surface对象
        :return:
        """
        if isinstance(image, str):
            # image为路径字符串的情况
            self.background_img = pygame.transform.smoothscale(
                pygame.image.load(image),
                (self.width, self.height)
            )
        else:
            # image为Surface的情况
            self.background_img = pygame.transform.smoothscale(
                image,
                (self.width, self.height)
            )
        # 做过渡动画时，必须要有一个原始背景图片的格式，所以要有两个background_img
        self.__background_img = self.background_img

    def bind_keyboard_callback(self, key:int, event_type:int, callback: callable, **option):
        """
        绑定按键事件
        :param key: pygame 的 key
        :param event_type: 表示 [ pygame.KEYUP ] 还是 [ pygame.KEYDOWN ]
        :param callback: 回调函数
        :param option: 传递给回调函数的参数
        :return:
        """
        if event_type == pygame.KEYUP:
            self.__key_up_event_callback_dict[key] = (callback, option)
        else:
            self.__key_down_event_callback_dict[key] = (callback, option)

    def close(self):
        """
        从渲染列表中删除该UI
        :return:
        """
        if self in scene_manager.now_scene[0]:
            scene_manager.now_scene[0].remove(self)
