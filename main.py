import pygame, random
from pygame import mixer

# Initialize
pygame.init()

# Title and Icon
pygame.display.set_caption('Flappy Bird')

# Create Screen
screen = pygame.display.set_mode((500, 900))
clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 40)

# Backgrounds
background = pygame.image.load('assets/background-day.png').convert()
background = pygame.transform.scale2x(background)
backgroundX_position = 0

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floorX_position = 0

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 450))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300, 500, 700]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(250, 450))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 200


def draw_background():
    screen.blit(background, (backgroundX_position, 0))
    screen.blit(background, (backgroundX_position + 500, 0))


def draw_floor():
    screen.blit(floor_surface, (floorX_position, 800))
    screen.blit(floor_surface, (floorX_position + 500, 800))


def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_position - 300))
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_position))
    return top_pipe, bottom_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def isCollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.bottom >= 800:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_surface = bird_frames[bird_index]
    new_bird_rect = new_surface.get_rect(center=(100, bird_rect.centery))

    return new_surface, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 780))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# Game Loop
running = True
while running:

    # Background Loop
    backgroundX_position -= 1
    draw_background()
    if backgroundX_position <= -500:
        backgroundX_position = 0

    # Floor Loop
    floorX_position -= 1
    draw_floor()
    if floorX_position <= -500:
        floorX_position = 0

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = isCollision(pipe_list)

        # Pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        score += 0.005
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 200
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 9
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 450)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index > 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    pygame.display.update()
    clock.tick(120)
