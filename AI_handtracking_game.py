import cv2
import mediapipe as mp
import pygame
import random
import threading

pygame.init()
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gesture Controlled Car Game")

road_img = pygame.image.load("assets/road.png")
road_img = pygame.transform.scale(road_img, (screen_width, screen_height * 2))
car_img = pygame.image.load("assets/car.png")
car_img = pygame.transform.scale(car_img, (60, 100))
obstacle_img = pygame.image.load("assets/obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (60, 100))

WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)
player = pygame.Rect(320, 380, 60, 100)
player_speed = 8
obstacle_speed = 5
score = 0
level = 1
level_threshold = 10
road_y = 0
running = True
gesture_x = screen_width // 2
obstacles = [pygame.Rect(random.randint(0, 640), random.randint(-600, 0), 60, 100)]
clock = pygame.time.Clock()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

def detect_gesture():
    global gesture_x, running
    while running:
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                h, w, _ = frame.shape
                index_x = int(handLms.landmark[8].x * w)
                gesture_x = index_x
        cv2.imshow("Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

gesture_thread = threading.Thread(target=detect_gesture)
gesture_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.centerx = int((gesture_x / 640) * screen_width)
    player.centerx = max(30, min(player.centerx, screen_width - 30))

    road_y += 5
    if road_y >= screen_height:
        road_y = 0

    for obs in obstacles:
        obs.y += obstacle_speed
        if obs.y > screen_height:
            obs.y = random.randint(-200, -100)
            obs.x = random.randint(0, screen_width - 60)
            score += 1
        if player.colliderect(obs):
            print(f"Game Over! Final Score: {score}")
            running = False

    level = (score // level_threshold) + 1
    obstacle_speed = 5 + level
    while len(obstacles) < level + 1:
        obstacles.append(pygame.Rect(random.randint(0, 640), random.randint(-500, 0), 60, 100))

    screen.blit(road_img, (0, road_y - screen_height))
    screen.blit(road_img, (0, road_y))
    screen.blit(car_img, (player.x, player.y))
    for obs in obstacles:
        screen.blit(obstacle_img, (obs.x, obs.y))

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
cap.release()
cv2.destroyAllWindows()
