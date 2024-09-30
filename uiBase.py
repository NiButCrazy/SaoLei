"""
自定义一个pygame的UI基类
"""
from typing import Callable,Any

import pygame

import eventManager


class UIBase:
    """
    UI基类，包含了最基本的UI样式、事件消息传递和过渡动画
    """
    def __init__(self,screen: pygame.Surface, x: int,y: int, size: tuple, color: tuple = (255,255,255), text: str = "", font_size: int = 16, font_color:tuple | str = (0,0,0)):
        """
        定义了一个UI最基本的文本、位置、大小
        :param screen: 绘制到该Surface
        :param x: UI的位置x
        :param y: UI的位置y
        :param size: UI的大小(width,height)
        :param (可选) color: UI上的背景颜色
        :param (可选) text: UI上的文本
        :param (可选) font_size: UI上的文本字体大小
        :param (可选) text: UI上的文本字体颜色
        """

        self.__scale_step = None
        self.__fps_clock = None
        # 鼠标按下回调函数
        self.__mouse_down_callback = lambda event, args: Any # print("鼠标按下")
        self.__mouse_down_callback_args = ()
        # 鼠标抬起回调函数
        self.__mouse_up_callback = lambda event, args: Any # print("鼠标抬起")
        self.__mouse_up_callback_args = ()
        # 鼠标进入UI回调函数
        self.__mouse_enter_callback = lambda event, args: Any # print("鼠标进入")
        self.__mouse_enter_callback_args = ()
        # 鼠标进入UI回调函数
        self.__mouse_leave_callback = lambda event, args: Any # print("鼠标离开")
        self.__mouse_leave_callback_args = ()

        self.screen = screen
        self.opacity = 255 # 背景颜色透明度
        self.content = text
        self.font_color = font_color
        self.font_size = font_size
        self.font_opacity = 255  # 文字透明度
        self.font = pygame.font.SysFont("Microsoft YaHei",font_size)
        self.text = self.font.render(text, True, font_color)
        self.pos_x = x
        self.pos_y = y
        self.width = size[0] # 实时宽度
        self.height = size[1] # 实时高度
        self.original_width = size[0] # 原始宽度，缩放时这个值不变
        self.original_height = size[1] # 原始高度，缩放时这个值不变
        self.color = color
        self.is_hover = False # 鼠标是否在UI上悬停
        self.background_img_opacity = 255  # 背景图片透明度
        self.background_img = None # 记录原始背景图片的变量
        self.__background_img = None # 游戏绘制的是这个图片的变量
        # 缩放过渡各参数
        self.__scale_y = 1
        self.__scale_x = 1
        self.__scale_duration = 0.0
        self.__now_scale_duration = 0.0
        self.__scale_step_x = 0
        self.__scale_step_y = 0
        self.__now_scale_step = 0
        # 缩放过渡动画是否运行中
        self.__transition_scale_running = False
        # 移动过渡动画是否运行中
        self.__transition_move_running = False
        # 绘制区域
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # 子节点列表
        self.children = []

        # 每次创建类实例时，会将实例推入事件管理器的emit_children列表中
        eventManager.manager.emit_children.append(self)

    def receive_event(self, event: pygame.event.Event, **option):
        # 如果鼠标在UI内，则将触发以下事件回调函数
        if hasattr(event,"pos") and self.rect.collidepoint(event.pos):
            # 鼠标悬停
            if not self.is_hover:
                self.is_hover = True
                self._mouse_enter(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up(event)

            # 给子节点发送事件
            for child in self.children:
                child.receive_event(event, **option)
        else:
            if self.is_hover:
                self.is_hover = False
                self._mouse_leave(event)

    def _mouse_down(self, event:pygame.event.Event):
        self.__mouse_down_callback(event,self.__mouse_down_callback_args)

    def mouse_down(self, callback:Callable[[pygame.event.Event, tuple],Any], **option):
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

    def mouse_up(self, callback:Callable[[pygame.event.Event, tuple],Any], **option):
        """
        绑定鼠标抬起时的回调参数
        :param callback: 回调函数
        :param option: (可选) 回调函数的参数
        :return:
        """
        self.__mouse_up_callback = callback
        self.__mouse_up_callback_args = option

    def update(self,fps_clock):
        """
        游戏更新回调
        :return:
        """
        self.__fps_clock = fps_clock
        self.__transition_scale()
        # 绘制自己（纯矩形图案或者图片）
        if self.background_img is None:
            ui_surface = pygame.Surface(self.rect.size)
            ui_surface.fill(self.color)
            ui_surface.set_alpha(self.opacity)
            self.screen.blit(ui_surface, self.rect)
        else:
            self.__background_img.set_alpha(self.background_img_opacity)
            self.screen.blit(self.__background_img, self.rect)
        # 绘制文本
        self.text.set_alpha(self.font_opacity)
        self.screen.blit(self.text, self.text.get_rect(center=self.rect.center))
        # 更新子节点
        for child in self.children:
            child.update(fps_clock)

    def set_text(self, content:str = "", font_color: tuple = (0,0,0), font_size: int = 0, font_family: str = "Microsoft YaHei"):
        """
        设置文本内容、颜色、字号、字体
        :param content: 文本内容
        :param font_color: 颜色
        :param font_size: 字号
        :param font_family: 字体
        :return:
        """
        if not content:
            content = self.content
        if font_color == (0,0,0):
            font_color = self.font_color
        if font_size == 0:
            font_size = self.font_size
        self.text = pygame.font.SysFont(font_family,font_size).render(content, True, font_color)


    def transition_scale(self, scale_x, scale_y, duration: float = 0.0):
        """
        UI的缩放过渡效果
        :param scale_x: x轴缩放倍数
        :param scale_y: y轴缩放倍数
        :param duration: 过渡动画完成时间
        :return:
        """

        self.__scale_duration = duration
        self.__scale_step = int( duration / self.__fps_clock )
        self.__transition_scale_running = True

        if not self.__scale_x == scale_x:
            self.__scale_x = scale_x
            if scale_x == 1:
                # 还原原来缩放大小
                self.__scale_step_x = ( self.original_width - self.width) / self.__scale_step
            else:
                # 这是正式缩放
                self.__scale_step_x = self.width * ( scale_x - 1 ) / self.__scale_step
        else:
            # 防止重复调用后无限放大
            self.__scale_step_x = 0

        if not self.__scale_y == scale_y:
            self.__scale_y = scale_y
            if scale_y == 1:
                # 还原原来缩放大小
                self.__scale_step_y = ( self.original_height - self.height ) / self.__scale_step
            else:
                # 这是正式缩放
                self.__scale_step_y = self.height * (scale_y - 1) / self.__scale_step
        else:
            # 防止重复调用后无限放大
            self.__scale_step_y = 0

        self.__now_scale_step = 0

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


    def mouse_enter(self, callback:Callable[[pygame.event.Event, tuple],Any], **option):
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

    def mouse_leave(self, callback:Callable[[pygame.event.Event, tuple],Any], **option):
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