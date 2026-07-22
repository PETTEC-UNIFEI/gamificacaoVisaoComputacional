import pygame
import time
from config import TEMPO_SELECAO, WIDTH, HEIGHT
from ui.button import draw_button

# layout original foi desenhado para 800x600; escalamos proporcionalmente
SCALE_X = WIDTH / 800
SCALE_Y = HEIGHT / 600


def scaled_rect(x, y, w, h):
    return pygame.Rect(
        int(x * SCALE_X), int(y * SCALE_Y),
        int(w * SCALE_X), int(h * SCALE_Y)
    )


buttons = {
    "Iniciar": scaled_rect(250, 220, 300, 60),
    "Score": scaled_rect(250, 300, 300, 60),
    "Sair": scaled_rect(250, 380, 300, 60)
}

hover_start = None
hovered = None
selected = None


def update_menu(screen, dedo_x, dedo_y, font):

    global hover_start, hovered, selected

    novo_hover = None

    if dedo_x is not None:
        for nome, rect in buttons.items():
            if rect.collidepoint(dedo_x, dedo_y):
                novo_hover = nome

    if novo_hover != hovered:
        hovered = novo_hover
        hover_start = time.time()

    if hovered and hover_start:
        if time.time() - hover_start > TEMPO_SELECAO:
            selected = hovered

    # título
    title = font.render("TOUCHLESS QUIZ", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, int(120 * SCALE_Y)))
    screen.blit(title, title_rect)

    for nome, rect in buttons.items():

        color = (80, 80, 100)

        if nome == hovered:
            color = (100, 150, 255)

        if nome == selected:
            color = (0, 200, 120)

        progress = 0

        if nome == hovered and hover_start:
            progress = min(
                (time.time() - hover_start) / TEMPO_SELECAO,
                1
            )

        draw_button(
            screen,
            rect,
            nome,
            font,
            color,
            progress
        )

    return selected