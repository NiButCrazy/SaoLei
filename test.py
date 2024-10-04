import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("圆形图片")

# 加载图片
image_path = "resource/create.jpg"
image = pygame.image.load(image_path).convert_alpha()

# 获取图片尺寸
image_width, image_height = image.get_size()

# 创建圆形蒙版
def make_circular_mask(image):
    mask_radius = min(image_width, image_height) // 2
    mask_surface = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
    pygame.draw.circle(mask_surface, (255, 255, 255), (mask_radius, mask_radius), mask_radius)
    return mask_surface

# 应用圆形蒙版
circular_mask = make_circular_mask(image)
circular_image = image.copy()
circular_image.blit(circular_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# 主循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 清屏
    screen.fill((255, 255, 255))

    # 绘制圆形图片
    screen.blit(circular_image, ((screen_width - image_width) // 2, (screen_height - image_height) // 2))

    # 更新屏幕
    pygame.display.flip()
    clock.tick(30)