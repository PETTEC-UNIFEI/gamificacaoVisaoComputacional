import pygame
import time

from config import TEMPO_SELECAO
from ui.button import draw_button
from data.questions import QUESTIONS

# ==========================
# LOGO
# ==========================

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

# ==========================
# ESTADO DO QUIZ
# ==========================

question_index = 0
score = 0

hover_start = None
hovered = None
selected = None

feedback = None
feedback_time = None

correct_answer = None

# ==========================
# ALTERNATIVAS
# ==========================

alternativas = [
    pygame.Rect(70, 250, 300, 80),
    pygame.Rect(430, 250, 300, 80),
    pygame.Rect(70, 370, 300, 80),
    pygame.Rect(430, 370, 300, 80)
]


def update_quiz(screen, dedo_x, dedo_y, font):

    global hover_start
    global hovered
    global selected

    global question_index
    global score

    global feedback
    global feedback_time

    global correct_answer

    pergunta = QUESTIONS[question_index]

    # ==========================
    # DETECÇÃO DE HOVER
    # ==========================

    novo_hover = None

    if dedo_x is not None:

        for i, rect in enumerate(alternativas):

            if rect.collidepoint(dedo_x, dedo_y):
                novo_hover = i

    if novo_hover != hovered:

        hovered = novo_hover
        hover_start = time.time()

    if (
        hovered is not None
        and hover_start
        and selected is None
        and feedback is None
    ):

        if time.time() - hover_start > TEMPO_SELECAO:

            selected = hovered

            correct_answer = pergunta["answer"]

            if selected == pergunta["answer"]:
                feedback = "CORRETO"
                score += 1
            else:
                feedback = "ERRADO"

            feedback_time = time.time()

    # ==========================
    # LOGO
    # ==========================

    screen.blit(
        logo,
        ((800 - nova_largura) // 2, 10)
    )

    # ==========================
    # PERGUNTA
    # ==========================

    font_pergunta = pygame.font.SysFont(
        "Arial",
        34,
        bold=True
    )

    texto = font_pergunta.render(
        pergunta["question"],
        True,
        (255, 255, 255)
    )

    texto_rect = texto.get_rect(
        center=(400, 210)
    )

    screen.blit(texto, texto_rect)

    # ==========================
    # ALTERNATIVAS
    # ==========================

    for i, opcao in enumerate(pergunta["options"]):

        color = (80, 80, 100)

        if i == hovered and feedback is None:
            color = (100, 150, 255)

        if feedback is not None:

            # resposta correta
            if i == correct_answer:
                color = (0, 200, 120)

            # resposta errada escolhida
            if (
                feedback == "ERRADO"
                and i == selected
                and selected != correct_answer
            ):
                color = (220, 50, 50)

        progress = 0

        if (
            i == hovered
            and hover_start
            and selected is None
        ):

            progress = min(
                (time.time() - hover_start)
                / TEMPO_SELECAO,
                1
            )

        draw_button(
            screen,
            alternativas[i],
            opcao,
            font,
            color,
            progress
        )

    # ==========================
    # SCORE
    # ==========================

    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (20, 20))

    # ==========================
    # FEEDBACK
    # ==========================

    if feedback is not None:

        feedback_font = pygame.font.SysFont(
            "Arial",
            40,
            bold=True
        )

        feedback_color = (
            (0, 255, 0)
            if feedback == "CORRETO"
            else (255, 0, 0)
        )

        feedback_text = feedback_font.render(
            feedback,
            True,
            feedback_color
        )

        feedback_rect = feedback_text.get_rect(
            center=(400, 540)
        )

        screen.blit(
            feedback_text,
            feedback_rect
        )

        if time.time() - feedback_time > 1.5:

            question_index += 1

            selected = None
            hovered = None
            hover_start = None

            feedback = None
            correct_answer = None

            if question_index >= len(QUESTIONS):
                question_index = 0