import pygame
import time
from config import TEMPO_SELECAO
from ui.button import draw_button

buttons = {
    "Iniciar": pygame.Rect(250, 220, 300, 60),
    "Score": pygame.Rect(250, 300, 300, 60),
    "Sair": pygame.Rect(250, 380, 300, 60)
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
    title = font.render("TOUCHLESS QUIZ", True, (255,255,255))
    screen.blit(title, (400 - 140, 120))

    for nome, rect in buttons.items():

        color = (80, 80, 100)

        if nome == hovered:
            color = (100, 150, 255)

        if nome == selected:
            color = (0, 200, 120)

        progress = 0
        if nome == hovered and hover_start:
            progress = min((time.time() - hover_start)/TEMPO_SELECAO, 1)

        draw_button(screen, rect, nome, font, color, progress)