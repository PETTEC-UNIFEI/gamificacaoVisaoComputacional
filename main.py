import pygame
import cv2

from config import WIDTH, HEIGHT
from vision.hand_tracking import get_frame_and_finger, release_camera
from ui.menu import update_menu
from ui.quiz import update_quiz

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Touchless Quiz")

font = pygame.font.SysFont("Arial", 32)

estado = "MENU"

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame, dedo_x, dedo_y = get_frame_and_finger()

    if frame is None:
        break

    # fundo desfocado
    blurred = cv2.GaussianBlur(frame, (35, 35), 0)

    frame_rgb = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2RGB
    )

    frame_rgb = cv2.resize(
        frame_rgb,
        (WIDTH, HEIGHT)
    )

    frame_surface = pygame.surfarray.make_surface(
        frame_rgb.swapaxes(0, 1)
    )

    screen.blit(frame_surface, (0, 0))

    # overlay escuro
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # ESTADOS DO JOGO

    if estado == "MENU":

        opcao = update_menu(
            screen,
            dedo_x,
            dedo_y,
            font
        )

        if opcao == "Iniciar":
            estado = "QUIZ"

        elif opcao == "Sair":
            running = False

    elif estado == "QUIZ":
        update_quiz(
            screen,
            dedo_x,
            dedo_y,
            font
        )

    # cursor do dedo
    if dedo_x is not None:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (dedo_x, dedo_y),
            10
        )

    pygame.display.flip()

release_camera()
pygame.quit()