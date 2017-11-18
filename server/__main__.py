from server.display.widget import *

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("heyyo")

    vbar_widget = VerticalBarWidget((0, 0), (15, 72), mode=VerticalBarWidget.MODE_CENTER, top_text="", bot_text="M1")
    vbar_widget.value = 1
    border_widget = BorderLayoutWidget((20, 20), center=vbar_widget, spacing=8)
    surface = pygame.display.set_mode((1366, 768))
    border_widget.blit(surface)
    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
