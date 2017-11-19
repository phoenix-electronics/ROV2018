from server.display.widget import *

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("heyyo")

    t_bar = VerticalBarWidget((0, 0), (16, 55), mode=VerticalBarWidget.MODE_NORMAL, top_text="+Y")
    b_bar = VerticalBarWidget((0, 0), (16, 55), mode=VerticalBarWidget.MODE_INVERT, bot_text="-Y")
    r_bar = HorizontalBarWidget((0, 0), (55, 16), mode=HorizontalBarWidget.MODE_NORMAL, left_text=" ", right_text="+X")
    l_bar = HorizontalBarWidget((0, 0), (55, 16), mode=HorizontalBarWidget.MODE_INVERT, right_text=" ", left_text="-X")
    bord = BorderLayoutWidget((10, 10), top=t_bar, bottom=b_bar, right=r_bar, left=l_bar, spacing=0)
    surface = pygame.display.set_mode((1366, 768))

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        if pygame.event.wait().type == pygame.QUIT:
            pygame.quit()

        x = -joystick.get_axis(0) * -1.05
        y = joystick.get_axis(1) * -1.05
        x = x if abs(x) >= 0.05 else 0
        y = y if abs(y) >= 0.05 else 0
        t_bar.value = y
        b_bar.value = y
        r_bar.value = x
        l_bar.value = x
        surface.fill((0, 0, 0))
        bord.blit(surface)
        pygame.display.flip()
