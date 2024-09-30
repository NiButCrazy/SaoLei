"""
开始菜单的通用按钮
"""

import uiBase
import pygame


class StartSceneBtn(uiBase.UIBase):
    """
    开始菜单的通用按钮类，继承自uiBase.UIBase
    """
    def __init__(self,screen: pygame.Surface, x: int,y: int, size: tuple, color: tuple = (255,255,255), text: str = "", font_size: int = 16, font_color:tuple | str = (0,0,0)):
        super().__init__(screen, x,y, size, color, text, font_size, font_color)
        self.btn_img = pygame.image.load("resource/btn4.png")
        self.btn_press_img = pygame.image.load("resource/btn3.png")
        self.set_background_image(self.btn_img)

    def _mouse_down(self, event:pygame.event.Event):
        self.background_img_opacity = 150
        super()._mouse_down(event)

    def _mouse_up(self, event:pygame.event.Event):
        self.background_img_opacity = 255
        super()._mouse_up(event)

    def _mouse_enter(self, event:pygame.event.Event):
        self.transition_scale(1.3, 1, 0.1)
        self.set_background_image(self.btn_press_img)
        self.set_text(font_color=(255, 255, 255), font_size=24)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        super()._mouse_enter(event)

    def _mouse_leave(self, event:pygame.event.Event):
        self.transition_scale(1, 1, 0.1)
        self.set_background_image(self.btn_img)
        self.set_text(font_color=(0, 0, 0), font_size=22)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        super()._mouse_leave(event)
