import pygame

def draw_button(screen, rect, text, font, color, progress=0):
    pygame.draw.rect(screen, color, rect, border_radius=15)

    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    if progress > 0:
        pygame.draw.rect(screen, (0,255,0),
                         (rect.x, rect.y + rect.height - 8,
                          rect.width * progress, 8))