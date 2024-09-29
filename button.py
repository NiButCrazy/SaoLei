"""
自定义一个pygame的按钮类
"""

from typing import Callable

import pygame
import eventManager


class ButtonBase:
    """
    按钮基类，包含了最基本的按钮样式、事件消息传递和过渡动画
    """
    def __init__(self,screen: pygame.Surface, x: int,y: int, size: tuple, text: str = "",):
        """
        定义了一个按钮最基本的文本、位置、大小
        :param screen: 绘制到该Surface
        :param x: 按钮的位置x
        :param y: 按钮的位置y
        :param size: 按钮的大小(width,height)
        :param (可选) text: 按钮上的文本
        """

        # 鼠标按下回调函数
        self._mouse_down_callback = lambda event, args: print("鼠标按下")
        self._mouse_down_callback_args = ()
        # 鼠标抬起回调函数
        self._mouse_up_callback = lambda event, args: print("鼠标抬起")
        self._mouse_up_callback_args = ()

        self.screen = screen
        self.text = text
        self.pos_x = x
        self.pos_y = y
        self.size = size
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, size[0],size[1])
        # 子节点列表
        self.children = []

        # 每次创建类实例时，会将实例推入事件管理器的emit_children列表中
        eventManager.manager.emit_children.append(self)

    def receive_event(self, event: pygame.event.Event, **option):
        # 如果鼠标在按钮内，则将触发以下事件回调函数
        if hasattr(event,"pos") and self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                pass

            # 给子节点发送事件
            for child in self.children:
                child.receive_event(event, **option)

    def _mouse_down(self, event:pygame.event.Event):
        self._mouse_down_callback(event,self._mouse_down_callback_args)
        return

    def mouse_down(self, callback:Callable[[pygame.event.Event, tuple],None], *args):
        """
        绑定鼠标按下时的回调参数
        :param callback: 回调函数
        :param args: (可选) 回调函数的参数
        :return:
        """
        self._mouse_down_callback = callback
        self._mouse_down_callback_args = args
        return

    def _mouse_up(self, event:pygame.event.Event):
        self._mouse_up_callback(event,self._mouse_up_callback_args)

    def mouse_up(self, callback:Callable[[pygame.event.Event, tuple],None], *args):
        """
        绑定鼠标抬起时的回调参数
        :param callback: 回调函数
        :param args: 回调函数的参数
        :return:
        """
        self._mouse_up_callback = callback
        self._mouse_up_callback_args = args
        return

    def update(self):
        """
        游戏更新回调
        :return:
        """
        # 绘制自己
        pygame.draw.rect(self.screen, self.color, self.rect)
        # 更新子节点
        for child in self.children:
            child.update()


    def mouse_hover(self):
        pass