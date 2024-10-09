"""
管理所有场景的类
"""
import pygame

__all__ = [
    "scene_manager"
]
from uiBase import UIBase
from config import get_config


class SceneManager:
    """
    管理所有场景的类，也保存游戏的一些基本变量
    """

    def __init__(self):
        self.scene_list: dict[str, tuple[list[UIBase], pygame.Surface]] = {}
        self.scene_music_list: dict[str, str] = {}
        self.now_scene: tuple[list[UIBase], pygame.Surface] | None = None
        self.FPS_CLOCK = 1 / get_config("FPS")
        # 存储一些特殊的UI， 方便在所有模块调用
        self.ui_dict: dict[str, UIBase] = {}

    def push_scene(self, scene_name: str, scene:tuple[list, pygame.Surface], bg_music:str = None) -> None:
        """
        把场景推入管理列表
        :param scene_name: 场景名称
        :param scene:场景
        :parameter bg_music: (可选) 背景音乐名
        :return:
        """
        self.scene_music_list[scene_name] = bg_music
        self.scene_list[scene_name] = scene

    def load_scene(self, scene_name: str) -> None:
        """
        加载场景
        :param scene_name: 需要加载场景的名称
        :return:
        """
        self.now_scene = self.scene_list[scene_name]
        pygame.mixer.music.load( self.scene_music_list[scene_name] )
        pygame.mixer.music.set_volume( get_config("volume"))
        pygame.mixer.music.play( -1 )

    def smooth_toggle_scene(self, screen: pygame.Surface, scene_name: str):
        """
        在场景切换时添加一个黑屏的过渡动画
        :param screen: 渲染的画布
        :param scene_name: 场景名
        :return:
        """
        # 音乐淡出
        pygame.mixer.music.fadeout( 1000 )
        black_surface = UIBase(screen, 0, 0, ( screen.get_width(), screen.get_height() ),color = (0,0,0))
        black_surface.opacity = 0
        self.now_scene[0].append(black_surface)
        black_surface.transition_opacity(255, 0.5, self.FPS_CLOCK).then(
            lambda: (
                # 从原本场景列表删除这玩意儿的引用，因为now_scene[0]是列表的引用指针，所以现在不删除的话，就永远无法从scene_list[scene_name]被释放了
                black_surface.close(),
                # 切换场景相当于切换指针，原本的场景列表本身是毫无变化的，依旧未被释放的
                self.load_scene(scene_name),
                # 继续把旧场景的过渡背景加入到现有背景列表中
                self.now_scene[0].append(black_surface),
                black_surface.transition_opacity(0, 0.5, self.FPS_CLOCK).then(
                    lambda : (
                        black_surface.close()
                    )
                ),

            )
        )



    def delete_scene(self, scene_name: str) -> None:
        """
        删除场景
        :param scene_name: 需要删除场景的名称
        :return:
        """
        del self.scene_list[scene_name]

    def load_welcome_scene(self, screen: pygame.Surface) -> None:
        """
        加载启动游戏的场景
        :param screen: 渲染的画布
        :return: 返回一个列表，list[0]是包含所有UIBase实例的列表，list[1]是一个背景图片的Surface对象
        """
        pygame.time.wait(500)
        img = pygame.image.load("resource/welcome.png")
        bg_img = pygame.Surface((800, 800))
        text = UIBase(screen, 300, 550, (0, 0),text = "好活当赏", font_size = 40,font_color = (255,255,255),enabled_event = False, center_anchor = True, user_font_family = True, font_family = "resource/font.ttf")
        img_ui = UIBase(screen, 0, 150, (800,500), color=(0, 0, 0))
        img_ui.set_background_image(img)
        img_ui.opacity = 0
        text.opacity = 0
        img_ui.children.append( text )
        img_ui.transition_opacity(255, 0.5, self.FPS_CLOCK).then(
            lambda : (
                pygame.time.wait(1000),
                self.smooth_toggle_scene(screen, "start_menu"),
            )
        )

        ui_list = [
            img_ui,
        ]

        self.now_scene = (ui_list, bg_img)


scene_manager = SceneManager()