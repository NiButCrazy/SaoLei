"""
这是一个事件管理类，用于处理事件消息的传递与发送
"""
import pygame

class EventManager:
    """
    事件管理类，拥有传递与接收消息的功能
    """
    def __init__(self):
        # 记录所有需要接收事件的实例
        self.emit_children = []

    def emit(self, event: pygame.event.Event, **option) -> None:
        """
        给所有需要接收事件的实例发送事件消息
        :param event: pygame的Event类
        :param option: (可选) 携带的参数
        :return:
        """
        for child in self.emit_children:
            child.receive_event(event, **option)

# 单例类
manager = EventManager()