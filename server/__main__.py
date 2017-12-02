from server.display.widget import *

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Debug')

    bar_widget = VerticalBarWidget((9, 9), (11, 40), mode=VerticalBarWidget.MODE_NORMAL, top_text='+Y')
    fps_widget = TextWidget((1247, 750), text='last draw: ??? ms')
    surface = pygame.display.set_mode((1366, 768))

    last_draw_time = 0
    while pygame.event.wait().type != pygame.QUIT:
        start_time = pygame.time.get_ticks()
        surface.fill((0, 0, 0))
        fps_widget.text = 'last draw: {:03d} ms'.format(last_draw_time)
        bar_widget.blit(surface)
        fps_widget.blit(surface)
        pygame.display.flip()
        last_draw_time = pygame.time.get_ticks() - start_time

    pygame.quit()
