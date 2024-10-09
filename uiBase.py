"""
自定义一个pygame的UI基类
"""
from typing import Callable,Any

import pygame


class UIChildrenList(list):
    """
    UI节点的子节点列表，提供了一系列方便的操作
    """
    def append(self, __object):
        """
        添加子节点到列表，并设置其父节点为此父节点本身
        :param __object: 一个UIBase对象
        :return:
        """
        super().append(__object)
        __object.parent_node =self


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
                 size: tuple = (0,0),
                 color: tuple = (255,255,255),
                 text: str = "",
                 font_size: int = 16,
                 font_color:tuple | str = (0,0,0),
                 font_family: str = "Microsoft YaHei",
                 user_font_family = False,
                 center_anchor: bool = False,
                 enabled_event:bool = True
                 ):
        """
        定义了一个UI最基本的文本、位置、大小
        :param screen: 绘制到该Surface
        :param x: UI的位置x
        :param y: UI的位置y
        :parameter size: (可选) UI的大小，默认为刚好框住字体大小的尺寸，缩放过渡功能对文本无效，通常用于创建一个透明背景文本
        :parameter color: (可选) UI上的背景颜色
        :parameter text: (可选) UI上的文本
        :parameter font_size: (可选) UI上的文本字体大小
        :parameter font_color: (可选) UI上的文本字体颜色
        :parameter font_family: (可选) 字体
        :parameter user_font_family: (可选) 是否使用用户自定义字体文件
        :parameter center_anchor: (可选) 是否以中心点为锚点
        :parameter enabled_event: (可选) 是否UI接受所有事件
        """

        # 鼠标按下回调函数
        self.__mouse_down_callback = lambda event, option: Any # print(self.name)
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
        self.display = True # UI是否显示，如果为False不会接收事件，也不会渲染显示
        self.enabled_event_penetration = False # 是否允许事件穿透，默认为False
        self.parent_node: UIBase | None = None # 父节点
        self.screen = screen
        self.opacity = 255 # 背景颜色透明度
        self.content = text
        self.font_color = font_color
        self.font_size = font_size
        self.user_font_family = user_font_family # 是否使用用户自定义字体文件
        self.font_family = font_family
        self.text:pygame.Surface | None = None # 最终字体surface对象
        self.pos_x = x # 原始x轴位置，最终渲染位置只靠rect属性
        self.pos_y = y # 原始y轴位置，最终渲染位置只靠rect属性
        self.width = size[0] # 实时宽度
        self.height = size[1] # 实时高度
        self.original_width = size[0] # 原始宽度，缩放时这个值不变
        self.original_height = size[1] # 原始高度，缩放时这个值不变
        self.center_anchor = center_anchor # 是否以中心点为锚点
        self.allow_opacity_transition_follow_parent = True # 是否允许父节点的透明度过渡对此节点的透明度过渡产生影响
        self.color = color # 背景颜色，只针对无背景图片的情况
        self.is_hover = False # 鼠标是否在UI上悬停
        self.enabled_event = enabled_event # UI 是否接收事件
        self.enabled_mouse_event = True # UI 是否接收鼠标事件
        self.enabled_keyboard_event = False # UI 是否接收键盘事件
        self.press_sound_effect: pygame.mixer.Sound | None = None # 用于播放鼠标按下音效
        self.hover_sound_effect: pygame.mixer.Sound | None = None # 用于播放鼠标进入时音效
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
        # 背景图片是否启用了圆形遮罩
        self.__use_circular_mask = False
        # 初始化绘制区域
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # 时间函数回调列表
        self.__timers = {"opacity":Timer(), "move":Timer(), "scale":Timer()}
        # 子节点列表
        self.children:UIChildrenList[UIBase] = UIChildrenList()
        # 初始化文本
        self.set_text(text,font_color,font_size, self.font_family)
        if size == (0,0):
            # 高度与宽度会保持0，这样可以做到透明背景文本
            new_size = self.text.get_size()
            self.rect = pygame.Rect(x, y, new_size[0], new_size[1]) # 初始化绘制区域
        # 设定以中心为锚点的坐标
        if self.center_anchor:
            self.pos_x = self.pos_x - int(self.rect.width / 2)
            self.pos_y = self.pos_y - int(self.rect.height / 2)
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y


    def receive_event(self, event: pygame.event.Event, **option) -> bool:
        """
        接收事件，并给子节点发送事件，且子节点的处理事件函数的时间早于父节点
        :param event: pygame的事件对象
        :param option: 事件所携带的额外参数
        :return: 返回一个布尔值，用于判断是否要把事件往底层图层传递
        """
        # 防止未进入游戏更新循环便触发事件
        if not self.__fps_clock:
            return True

        # 如果当前UI未显示，则直接返回
        if not self.display:
            # 防止鼠标悬停状态还停留在停止接收事件之前
            self.is_hover = False
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

        # 未开启接收事件直接返回
        if not self.enabled_event:
            self.is_hover = False
            return True

        # 设定默认事件穿透状态，只针对鼠标事件
        event.enabled_event_penetration = False

        # 处理键盘输入事件，同一个按键事件只会被最顶层的UI处理
        if self.enabled_keyboard_event and not option["stop_emit"]:
            if event.type == pygame.KEYDOWN:
                if event.key in self.__key_down_event_callback_dict:
                    # 调用绑定的按键函数
                    self.__key_down_event_callback_dict[event.key][0](event, self.__key_down_event_callback_dict[event.key][1])
                    return False
                else:
                    return True
            elif event.type == pygame.KEYUP:
                if event.key in self.__key_up_event_callback_dict:
                    # 调用绑定的按键函数
                    self.__key_up_event_callback_dict[event.key][0](event, self.__key_up_event_callback_dict[event.key][1])
                    return False
                else:
                    # 如果没有按键冲突，则向下传递
                    return True

        # 如果鼠标在UI内，则将触发以下事件回调函数
        if hasattr(event,"pos") and self.rect.collidepoint(event.pos) and not option["stop_emit"] and self.enabled_mouse_event:
            # 鼠标悬停
            if not self.is_hover:
                self.is_hover = True
                self._mouse_enter(event)
            # 处理鼠标输入事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up(event)

            # 是否开启事件穿透
            if event.enabled_event_penetration or self.enabled_event_penetration:
                if hasattr(event, "force_event_penetration"):
                    boolean = event.force_event_penetration
                    delattr(event, "force_event_penetration")
                    return boolean
                return True

            # 截断事件向下传递
            return False

        else:
            # 判断是否离开鼠标悬停状态
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

        if not self.display:
            return

        # 绘制自己（纯矩形图案或者图片）
        if self.background_img is None:
            ui_surface = pygame.Surface((self.width, self.height))
            ui_surface.fill(self.color)
            ui_surface.set_alpha(self.opacity)
            self.screen.blit(ui_surface, self.rect)
        else:
            self.__background_img.set_alpha(self.opacity)
            self.screen.blit(self.__background_img, self.rect)
        # 绘制文本
        self.text.set_alpha(self.opacity)
        self.screen.blit(self.text, self.text.get_rect(center=self.rect.center))
        # 更新子节点
        for child in self.children:
            child.update(fps_clock)

    def set_text(self, content:str | None = None, font_color: tuple | str = (-1,-1,-1), font_size: int = 0, font_family: str = "", bold: bool = False):
        """
        设置文本内容、颜色、字号、字体
        :param content: (可选) 文本内容
        :param font_color: (可选) 颜色
        :param font_size: (可选) 字号
        :param bold: (可选) 是否加粗
        :param font_family: (可选) 字体,如果是自定义字体请填写文件路径，并且一定要设置user_font_family为True
        :return:
        """
        if content is None:content = self.content
        else: self.content = content

        if font_color == (-1,-1,-1):font_color = self.font_color
        else: self.font_color = font_color

        if font_size == 0:font_size = self.font_size
        else: self.font_size = font_size

        if font_family == "": font_family = self.font_family
        else: self.font_family = font_family

        if not self.user_font_family:
            font = pygame.font.SysFont(font_family,font_size)
            if bold:
                font.set_bold(True)
            self.text = font.render(content, True, font_color)
        else:
            font = pygame.font.Font(font_family,font_size)
            if bold:
                font.set_bold(True)
            self.text = font.render(content, True, font_color)

    def transition_scale(self, scale_x, scale_y, duration: float = 0.0) -> Timer:
        """
        UI的缩放过渡效果，注意：不支持文字缩放
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
        # y轴缩放比例
        self.__scale_y = scale_y
        if not duration == 0:
            # x轴缩放步长
            self.__scale_step_x =  ( self.original_width * scale_x - self.width ) / self.__scale_step
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
                # 这中心缩放很稳，基本不会鬼畜
                if self.center_anchor:
                    self.rect.x = self.pos_x - int((self.width - self.original_width) / 2)
                    self.rect.y = self.pos_y - int((self.height - self.original_height) / 2)

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

                if self.center_anchor:
                    self.rect.x = self.pos_x - int(( self.width - self.original_width )/2)
                    self.rect.y = self.pos_y - int(( self.height - self.original_height )/2)

                if self.background_img is not None:
                    self.__background_img = pygame.transform.smoothscale(self.background_img, (self.width, self.height))
                self.__timers["scale"].use_callback()

    def transition_opacity(self, dest_opacity: int, duration: float = 0.0, fps_clock: float = 0.0, children_together: bool = True) -> Timer:
        """
        UI的缩放过渡效果
        :param dest_opacity: 目标透明度（ 0~255 ）
        :param duration: (可选) 过渡动画完成时间
        :param fps_clock: (可选) 游戏更新循环周期，此选项通常用于UI还未被加载进游戏主进程渲染更新中，起到预加载作用
        :param children_together: (可选) 是否让子节点同步进行过渡动画，注意：不管什么情况，子节点必须先添加进父节点的Children列表，才能执行本函数，否则没有效果
        :return:
        """
        # 过渡效果达成时间
        self.__opacity_duration = duration
        # 目标透明度
        self.__dest_opacity = dest_opacity
        if fps_clock == 0.0:
            fps_clock = self.__fps_clock
        # 总过渡步数
        self.__opacity_step = int( duration / fps_clock )
        # 是否已经处于过渡中
        self.__transition_opacity_running = True
        # 过渡步长
        if not duration == 0:
            self.__opacity_step_distance = ( self.opacity - dest_opacity ) / self.__opacity_step
        # 目前过渡步数
        self.__now_opacity_step = 0
        # 是否让子节点同步过渡
        if children_together:
            for child in self.children:
                if child.allow_opacity_transition_follow_parent:
                    child.transition_opacity(dest_opacity, duration, fps_clock)

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

    def set_background_image(self, path: str | pygame.Surface, use_circular_mask: bool = False):
        """
        设置背景图片
        :param path: 接受一个图片路径字符串 或 一个图片的Surface对象
        :parameter use_circular_mask: 是否使用圆形蒙版
        :return:
        """
        if isinstance(path, str):
            # image为路径字符串的情况
            self.background_img = pygame.transform.smoothscale(
                pygame.image.load(path),
                (self.width, self.height)
            )
        else:
            # image为Surface的情况
            self.background_img = pygame.transform.smoothscale(
                path,
                (self.width, self.height)
            )
        # 做过渡动画时，必须要有一个原始背景图片的格式，所以要有两个background_img
        # 是否设置圆形遮罩
        if use_circular_mask:
            circular_image = self.background_img.convert_alpha()
            circular_mask = self.make_circular_mask(circular_image)
            circular_image.blit(circular_mask, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
            self.__background_img = circular_image
        else:
            self.__background_img = self.background_img

    def bind_keyboard_callback(self, key:int, event_type:int, callback: Callable[[pygame.event.Event, dict[str, Any]],Any], **option):
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
        from sceneManager import scene_manager
        if self in scene_manager.now_scene[0]:
            scene_manager.now_scene[0].remove(self)
        if not self.parent_node is None:
            self.parent_node.children.remove(self)

    def move_to(self, x: int, y: int):
        """
        移动UI绝对位置
        :param x: x轴位置
        :param y: y轴位置
        :return:
        """
        self.rect.move_ip(x, y)
        self.pos_x = x
        self.pos_y = y

    def move_by(self, x: int, y: int):
        """
        移动UI相对位置
        :param x: x轴偏移量
        :param y: y轴偏移量
        :return:
        """
        self.rect.x += x
        self.rect.y += y
        self.pos_x += x
        self.pos_y += y

    # 创建圆形蒙版
    def make_circular_mask(self, image:pygame.Surface):
        self.__use_circular_mask = True
        image_width, image_height = image.get_size()
        mask_radius = min(image_width, image_height) // 2
        mask_surface = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
        # color 代表蒙版的滤镜偏色，（255，255，255）代表没有滤镜，后面那一坨参数是抗锯齿
        pygame.draw.circle(mask_surface, (255, 255, 255), (mask_radius, mask_radius), mask_radius)
        return mask_surface

    def get_blit_background_image(self):
        """
        获得被渲染的背景图片
        :return:
        """
        return self.__background_img