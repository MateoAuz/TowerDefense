import pygame
from cozy import Cozy
from tower import Tower
from projectile import Projectile
from config import (
    TOWER_LIST, WIDTH, HEIGHT, FPS,
    BG_COLOR,
    TOWER_TYPES, COZY_TYPES,
    path
)
from boss_cozy import BossCozy
from collections import deque

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

# Cargar imágenes de torres para el menú de selección
tower_selection_images = {
    "basic": pygame.transform.scale(pygame.image.load("images/towers/torreBase.png"), (40, 40)),
    "sniper": pygame.transform.scale(pygame.image.load("images/towers/torreMedia.png"), (40, 40)),
    "rapid": pygame.transform.scale(pygame.image.load("images/towers/torreRapida.png"), (40, 40))
}

pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")
game_over_sound.set_volume(0.3)
pygame.mixer.music.load("assets/marcha_imperial.mp3")
pygame.mixer.music.set_volume(0.7)  # Volumen (0.0 a 1.0)

# Load background image
background_img = pygame.image.load("images/snow_forest_background.png")  # renamed your uploaded image to this
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
coin_img = pygame.transform.scale(pygame.image.load("images/coin.png"), (32, 32))


# Game state
game_state = "menu"

# Game variables
wave = 1
wave_in_progress = False
wave_timer = 0
cozy_queue = deque() 
cozies_to_spawn = 0
cozy_spawn_times = []
spawn_index = 0
cozy_timer = 0
wave_message_timer = 0
wave_message_duration = 120
wave_message_text = ""

cozies = []
towers = []
projectiles = []
undo_stack = []
redo_stack = []

player_health = 10
coins = 100
coins_per_kill = 20
score = 0
font = pygame.font.SysFont("arial", 24)
selected_tower_type = "basic"
boss_spawned = False

# Button positions
undo_button_rect = pygame.Rect(WIDTH - 200, 10, 80, 30)
redo_button_rect = pygame.Rect(WIDTH - 110, 10, 80, 30)

def start_wave(n_wave):
    global wave_in_progress, wave_timer, cozy_queue, cozy_spawn_timer
    global wave_message_timer, wave_message_text

    wave_in_progress = True
    wave_timer = 0
    cozy_queue.clear()
    cozy_spawn_timer = 0
    wave_message_text = f"Wave {n_wave}!"
    wave_message_timer = wave_message_duration

    total_cozies = 5 + (n_wave - 1) * 2

    for _ in range(total_cozies):
        cozy = Cozy(path)
        cozy.health += 40 * (n_wave - 1)
        cozy.max_health = cozy.health  
        cozy_queue.append(cozy)


    3
    if n_wave % 3 == 0:
        boss = BossCozy(path)
        incremento = 40 * ((n_wave // 3) - 1)
        boss.health += incremento
        boss.max_health = boss.health
        cozy_queue.append(boss)




def show_start_menu(screen):
    title_font = pygame.font.SysFont("arial", 48)
    info_font = pygame.font.SysFont("arial", 28)
    title = title_font.render("TOWER DEFENSE", True, (255, 255, 0))
    message = info_font.render("Press ENTER to start", True, (255, 255, 255))
    screen.fill(BG_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

def is_on_path(x, y, path, tolerance=30):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            distance = ((x - x1)**2 + (y - y1)**2)**0.5
        else:
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx*dx + dy*dy)))
            px = x1 + t * dx
            py = y1 + t * dy
            distance = ((x - px)**2 + (y - py)**2)**0.5
        if distance < tolerance:
            return True
    return False

def draw_tower_selection(screen, selected_type):
    # Crear un panel en la parte inferior de la pantalla
    panel_rect = pygame.Rect(10, HEIGHT - 110, 300, 100)
    
    # Dibujar el panel con un fondo semitransparente
    pygame.draw.rect(screen, (40, 40, 80), panel_rect, border_radius=12)
    pygame.draw.rect(screen, (100, 200, 255), panel_rect, 3, border_radius=12)
    
    # Título
    title_font = pygame.font.SysFont("Old English Text MT", 22)
    title = title_font.render("Selección de Torres", True, (255, 255, 255))
    screen.blit(title, (panel_rect.x + panel_rect.width//2 - title.get_width()//2, panel_rect.y + 10))
    
    # Dibujar cada opción de torre con atajo de teclado
    tower_font = pygame.font.SysFont("arial", 16)
    
    # Espaciar torres uniformemente - aumentar el espaciado
    spacing = 90
    
    for i, tower_type in enumerate(TOWER_LIST):
        # Centrar las torres horizontalmente en el panel
        tower_x = panel_rect.x + 50 + (i * spacing)
        tower_y = panel_rect.y + 50
        
        # Dibujar círculo de torre
        tower_color = TOWER_TYPES[tower_type]["color"]
        img = tower_selection_images[tower_type]
        screen.blit(img, (tower_x - 20, tower_y - 20))  # Centrado para imágenes de 40x40
        
        # Dibujar indicador de selección si está seleccionada
        if tower_type == selected_type:
            pygame.draw.circle(screen, (255, 0, 0), (tower_x, tower_y), 18, 2)
        
        # Dibujar número de tecla - ahora por encima del círculo
        key_text = tower_font.render(f"{i+1}", True, (255, 255, 0))
        screen.blit(key_text, (tower_x - 5, tower_y + 25))
        
        # Dibujar costo de la torre - ahora a la derecha del círculo
        cost_text = tower_font.render(f"${TOWER_TYPES[tower_type]['cost']}", True, (255, 255, 255))
        screen.blit(cost_text, (tower_x + 25, tower_y - 5))
        
        
def show_game_over(screen):
    game_over_font = pygame.font.SysFont("arial", 64)
    text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                wave = 1
                start_wave(wave)
                game_state = "playing"
                pygame.mixer.music.play(-1)  # Reproducir música al presionar ENTER


        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_tower_type = "basic"
                elif event.key == pygame.K_2:
                    selected_tower_type = "sniper"
                elif event.key == pygame.K_3:
                    selected_tower_type = "rapid"
                elif event.key == pygame.K_u:
                    if undo_stack:
                        last_tower = undo_stack.pop()
                        towers.remove(last_tower)
                        coins += TOWER_TYPES[last_tower.tipo]["cost"]
                        redo_stack.append(last_tower)
                elif event.key == pygame.K_r:
                    if redo_stack:
                        redo_tower = redo_stack.pop()
                        towers.append(redo_tower)
                        coins -= TOWER_TYPES[redo_tower.tipo]["cost"]
                        undo_stack.append(redo_tower)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if undo_button_rect.collidepoint(event.pos):
                    if undo_stack:
                        last_tower = undo_stack.pop()
                        towers.remove(last_tower)
                        coins += TOWER_TYPES[last_tower.tipo]["cost"]
                        redo_stack.append(last_tower)
                    continue

                if redo_button_rect.collidepoint(event.pos):
                    if redo_stack:
                        redo_tower = redo_stack.pop()
                        towers.append(redo_tower)
                        coins -= TOWER_TYPES[redo_tower.tipo]["cost"]
                        undo_stack.append(redo_tower)
                    continue

                mx, my = pygame.mouse.get_pos()
                tower_type = selected_tower_type
                cost = TOWER_TYPES[tower_type]["cost"]
                if coins >= cost and not is_on_path(mx, my, path):
                    new_tower = Tower(mx, my, tower_type)
                    towers.append(new_tower)
                    coins -= cost
                    undo_stack.append(new_tower)
                    redo_stack.clear()

    if game_state == "menu":
        show_start_menu(screen)

    elif game_state == "playing":
        screen.blit(background_img, (0, 0))

        if not wave_in_progress and len(cozies) == 0:
            wave += 1
            start_wave(wave)

        if wave_in_progress:
            cozy_spawn_timer += 1
        if cozy_spawn_timer >= 40 and cozy_queue:
            cozies.append(cozy_queue.popleft())
            cozy_spawn_timer = 0

        if not cozy_queue and not cozies:
            wave_in_progress = False




        for cozy in cozies[:]:
            reached_end = cozy.move()
            if reached_end:
                cozies.remove(cozy)
                player_health -= 1
            else:
                cozy.draw(screen)

        for cozy in cozies[:]:
            if cozy.health <= 0:
                if isinstance(cozy, BossCozy):
                    score += 3
                else:
                    score += 1
                cozies.remove(cozy)
                coins += coins_per_kill

        for tower in towers:
            tower.shoot(cozies, projectiles)
            tower.draw(screen)

        for p in projectiles[:]:
            if p.move():
                projectiles.remove(p)
            p.draw(screen)

        health_text = font.render(f"Health: {player_health}", True, (30, 30, 30))
        screen.blit(health_text, (10, 10))

        wave_text = font.render(f"Wave: {wave}", True, (30, 30, 30))
        score_text = font.render(f"Score: {score}", True, (30, 30, 30))
        screen.blit(score_text, (10, 70))
        screen.blit(wave_text, (10, 40))

        # Dibujar imagen de la moneda
        screen.blit(coin_img, (320, HEIGHT - 42))

        # Dibujar texto al lado derecho de la imagen
        coins_text = font.render(f"{coins}", True, (255, 255, 0))
        screen.blit(coins_text, (360, HEIGHT - 35))

        pygame.draw.rect(screen, (200, 200, 200), undo_button_rect)
        undo_text = font.render("Undo", True, (0, 0, 0))
        screen.blit(undo_text, (undo_button_rect.x + 10, undo_button_rect.y + 5))

        pygame.draw.rect(screen, (200, 200, 200), redo_button_rect)
        redo_text = font.render("Redo", True, (0, 0, 0))
        screen.blit(redo_text, (redo_button_rect.x + 10, redo_button_rect.y + 5))

        if player_health <= 0:
            game_state = "game_over"

        if wave_message_timer > 0:
            wave_msg_font = pygame.font.SysFont("arial", 36)
            text = wave_msg_font.render(wave_message_text, True, (255, 255, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 80))
            wave_message_timer -= 1

        mouse_x, mouse_y = pygame.mouse.get_pos()
        tower_color = TOWER_TYPES[selected_tower_type]["color"]
        cost = TOWER_TYPES[selected_tower_type]["cost"]
        tower_range = TOWER_TYPES[selected_tower_type]["range"]
        blocked = is_on_path(mouse_x, mouse_y, path)

        if coins < cost:
            preview_color = (255, 0, 0)
        elif blocked:
            preview_color = (150, 150, 150)
        else:
            preview_color = tower_color

        pygame.draw.circle(screen, preview_color, (mouse_x, mouse_y), 20, 2)
        pygame.draw.circle(screen, (100, 100, 100), (mouse_x, mouse_y), tower_range, 1)
        draw_tower_selection(screen, selected_tower_type)


    elif game_state == "game_over":
        pygame.mixer.music.stop()           # Detener música de fondo
        game_over_sound.play()              # Reproducir sonido de derrota
        show_game_over(screen)
        pygame.time.delay(2000)             # Espera opcional para que suene completo
        running = False


    pygame.display.flip()

pygame.quit()
