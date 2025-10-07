import cv2
import numpy as np
import pygame
import threading
import random

# -----------------------------
# STEP 1: SETUP GAME
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("Color Gesture Game")

WHITE = (255,255,255)
BLUE = (0,100,255)
RED = (255,0,0)
BLACK = (0,0,0)

player = pygame.Rect(300,400,50,50)
obstacle = pygame.Rect(random.randint(0,650),0,50,50)
player_speed = 7
obstacle_speed = 5
direction = "stop"
score = 0
running = True

clock = pygame.time.Clock()
font = pygame.font.Font(None,36)

# -----------------------------
# STEP 2: SETUP COLOR DETECTION
# -----------------------------
cap = cv2.VideoCapture(0)

def detect_color_gesture():
    global direction, running
    prev_x, prev_y = 0,0

    while running:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define red color range (you can adjust)
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        mask = mask1 + mask2
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)

            if prev_x != 0 and prev_y != 0:
                dx = x - prev_x
                dy = y - prev_y

                if abs(dx) > abs(dy):
                    if dx > 5:
                        direction = "right"
                    elif dx < -5:
                        direction = "left"
                else:
                    if dy > 5:
                        direction = "down"
                    elif dy < -5:
                        direction = "up"

            prev_x, prev_y = x,y

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow("Color Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

# Run color detection in background
threading.Thread(target=detect_color_gesture, daemon=True).start()

# -----------------------------
# STEP 3: GAME LOOP
# -----------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player based on gesture
    if direction=="up": player.y -= player_speed
    elif direction=="down": player.y += player_speed
    elif direction=="left": player.x -= player_speed
    elif direction=="right": player.x += player_speed

    # Keep player inside screen
    player.x = max(0,min(player.x,650))
    player.y = max(0,min(player.y,450))

    # Move obstacle
    obstacle.y += obstacle_speed
    if obstacle.y > 500:
        obstacle.y = 0
        obstacle.x = random.randint(0,650)
        score += 1

    # Collision detection
    if player.colliderect(obstacle):
        print(f"Game Over! Score: {score}")
        running = False

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, obstacle)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text,(10,10))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
cap.release()
cv2.destroyAllWindows()
