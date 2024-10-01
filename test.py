import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((800, 600))

# 设置标题
pygame.display.set_caption("键盘事件示例")
# pygame.key.stop_text_input()

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print("按下了键", event.key)
            if event.key == pygame.K_LEFT:
                print("向左键被按下")
            elif event.key == pygame.K_RIGHT:
                print("向右键被按下")
            elif event.key == pygame.K_UP:
                print("向上键被按下")
            elif event.key == pygame.K_DOWN:
                print("向下键被按下")

    # 更新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()