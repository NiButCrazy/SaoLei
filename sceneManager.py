"""
管理所有场景的类
"""
import pygame

__all__ = [
    "scene_manager"
]

from config import get_config


class SceneManager:
    """
    管理所有场景的类，也保存游戏的一些基本变量
    """

    def __init__(self):
        self.scene_list = {}
        self.now_scene = None
        self.FPS_CLOCK = 1 / get_config("FPS")

    def push_scene(self, scene_name: str, scene:tuple[list, pygame.Surface]) -> None:
        """
        把场景推入管理列表
        :param scene_name: 场景名称
        :param scene:场景
        :return:
        """
        self.scene_list[scene_name] = scene

    def load_scene(self, scene_name: str) -> None:
        """
        加载场景
        :param scene_name: 需要加载场景的名称
        :return:
        """
        self.now_scene = self.scene_list[scene_name]

    def delete_scene(self, scene_name: str) -> None:
        """
        删除场景
        :param scene_name: 需要删除场景的名称
        :return:
        """

scene_manager = SceneManager()