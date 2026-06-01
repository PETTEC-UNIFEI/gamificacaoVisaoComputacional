import pygame

from ui.button import draw_button
from data.questions import QUESTIONS

# Carrega logo apenas uma vez
logo = pygame.image.load("assets/logo_pet.png")

largura_original = logo.get_width()
altura_original = logo.get_height()

nova_altura = 140

nova_largura = int(
    largura_original * (nova_altura / altura_original)
)

logo = pygame.transform.scale(
    logo,
    (nova_largura, nova_altura)
)

question_index = 0

alternativas = [
    pygame.Rect(70, 250, 300, 80),   # superior esquerda
    pygame.Rect(430, 250, 300, 80),  # superior direita
    pygame.Rect(70, 370, 300, 80),   # inferior esquerda
    pygame.Rect(430, 370, 300, 80)   # inferior direita
]


def update_quiz(screen, font):

    pergunta = QUESTIONS[question_index]

    # LOGO
    screen.blit(
        logo,
        ((800 - nova_largura) // 2, 10)
    )

    # FONTE DA PERGUNTA
    font_pergunta = pygame.font.SysFont(
        "Arial",
        34,
        bold=True
    )

    # TEXTO DA PERGUNTA
    texto = font_pergunta.render(
        pergunta["question"],
        True,
        (255, 255, 255)
    )

    texto_rect = texto.get_rect(
        center=(400, 210)
    )

    screen.blit(texto, texto_rect)

    # ALTERNATIVAS
    for i, opcao in enumerate(pergunta["options"]):

        draw_button(
            screen,
            alternativas[i],
            opcao,
            font,
            (80, 80, 100)
        )