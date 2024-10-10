"""
这是一个事件管理类，用于处理事件消息的传递与发送
"""
import pygame
from sceneManager import scene_manager

class EventManager:
    """
    事件管理类，拥有传递与接收消息的功能
    """
    def __init__(self):
        # 用于存储用户自己创建的事件名称与对应的事件id
        self.user_events = {}
        # 现在最新注册的事件id
        self.now_event_id = pygame.USEREVENT
        # 记录游戏是否暂停
        self.game_stop = False
        # 记录游戏是否已经开始过一次
        self.game_has_started = False
        # 记录是否在游戏中
        self.game_playing = False

    def register_event(self, event_name: str) -> None:
        """
        注册用户自定义事件
        :param event_name: 事件名称
        :return:
        """
        self.now_event_id += 1
        self.user_events[event_name] = self.now_event_id

    def post_event(self, event_name: str, **option) -> None:
        """
        发送用户自定义事件
        :param event_name: 事件名称
        :param option: 事件参数
        :return:
        """
        pygame.event.post(pygame.event.Event(self.user_events[event_name], **option))

def emit(event: pygame.event.Event, **option) -> None:
    """
    给所有需要接收事件的实例发送事件消息
    :param event: pygame的Event类
    :param option: (可选) 携带的参数
    :return:
    """
    # 最后渲染的(也就是最顶层的)ui最先接收到事件，防止事件被底层ui吞了
    for index in range(len(scene_manager.now_scene[0]) - 1, -1, -1):
        if_continue_emit = scene_manager.now_scene[0][index].receive_event(event, **option)
        # 如果已被目标UI截断，则其他UI不再调用的此事件的处理函数
        if not if_continue_emit:
            option["stop_emit"] = True

def set_event_penetration(event: pygame.event.Event, boolean:bool, force:bool = False):
    """
    切换某个事件穿透状态
    :param event: 一个pygame的事件
    :param boolean: 是否开启事件穿透
    :param force: 是否开启强制事件穿透，可以无视UI本身设置的事件穿透属性
    :return:
    """
    if force:
        event.force_event_penetration = boolean
    event.enabled_event_penetration = boolean

# 单例类
event_manager = EventManager()