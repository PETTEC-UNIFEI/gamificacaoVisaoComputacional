import cv2
import mediapipe as mp
import pygame
import time

# MEDIA PIPE CONFIG
model_path = "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

detector = HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)

# PYGAME CONFIG
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Touchless Quiz")

font = pygame.font.SysFont("Arial", 32)

# BOTÕES
buttons = {
    "Iniciar": pygame.Rect(250, 220, 300, 60),
    "Score": pygame.Rect(250, 300, 300, 60),
    "Sair": pygame.Rect(250, 380, 300, 60)
}

hover_start = None
hovered = None
selected = None
tempo_selecao = 1.0

# LOOP PRINCIPAL
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # CAMERA
    ret, frame = cap.read()
    if not ret:
        break

    # corrigir espelho
    frame = cv2.flip(frame, 1)

    # BLUR (EFEITO IPHONE)
    blurred = cv2.GaussianBlur(frame, (35, 35), 0)

    frame_rgb = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (WIDTH, HEIGHT))

    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0,1))

    screen.blit(frame_surface, (0, 0))

    # overlay leve (vidro fosco)
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(80)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # DETECÇÃO DA MÃO
    frame_mp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_mp)
    result = detector.detect(mp_image)

    dedo_x, dedo_y = None, None

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            h, w, _ = frame.shape
            dedo_x = int(hand_landmarks[8].x * WIDTH)
            dedo_y = int(hand_landmarks[8].y * HEIGHT)

    # HOVER / SELEÇÃO
    novo_hover = None

    if dedo_x is not None:
        for nome, rect in buttons.items():
            if rect.collidepoint(dedo_x, dedo_y):
                novo_hover = nome

    if novo_hover != hovered:
        hovered = novo_hover
        hover_start = time.time()

    if hovered and hover_start:
        if time.time() - hover_start > tempo_selecao:
            selected = hovered

    # UI

    # título
    title = font.render("TOUCHLESS QUIZ", True, (255,255,255))
    screen.blit(title, (WIDTH//2 - 140, 120))

    for nome, rect in buttons.items():

        color = (80, 80, 100)

        if nome == hovered:
            color = (100, 150, 255)

        if nome == selected:
            color = (0, 200, 120)

        # botão arredondado
        pygame.draw.rect(screen, color, rect, border_radius=15)

        # texto centralizado
        text = font.render(nome, True, (255,255,255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        # barra de progresso
        if nome == hovered and hover_start:
            progress = min((time.time() - hover_start)/tempo_selecao, 1)
            pygame.draw.rect(screen, (0,255,0),
                             (rect.x, rect.y + rect.height - 8,
                              rect.width * progress, 8))

    # cursor (dedo)
    if dedo_x is not None:
        pygame.draw.circle(screen, (0,255,0), (dedo_x, dedo_y), 10)

    pygame.display.flip()

# FINALIZAÇÃO
cap.release()
pygame.quit()