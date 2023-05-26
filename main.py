# Imports
import pygame,math,time
import psycopg2
import config
import bd


# Exception Console patterns
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Database
print("Connecting to postgreSQL database...")
params = config.config()
connection = psycopg2.connect(**params)

cursor = connection.cursor()
cursor.execute(bd.table_check())
bd.create_script()
func = bd.create_script()
cursor.execute(func)
insert_value = []

# Pygame
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perfect Circle || Incubator 2023")

# Score
score_val = 0.00
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('Monocraft.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 20)
cc = font1.render("askvizi@bk.ru", True, pygame.Color(255, 255, 255))
cc1 = font1.render("Perfect Circle", True, pygame.Color(255, 255, 255))
cc2 = font1.render("Incubator23", True, pygame.Color(255, 0, 0))

textX = 368
textY = 358

# Game Surface
surface_width = 128
surface_height = 32
surface = pygame.Surface((surface_width, surface_height))

# Sounds
err_sound = pygame.mixer.Sound("error-126627_TC403uZU.mp3")
def err():
    pygame.mixer.Sound.play(err_sound)
    pygame.mixer.music.stop()

# Colors Drawings
GREEN = (0, 225, 0)
RED = (225, 0, 0)
YELLOW = (225, 225, 0)
WHITE = (225, 225, 225)
drawing = False
last_pos = None
main_dot = None
total_sum = 0
count = 0

# over game tools
game_over = False
angle = 0
arc_length = 0
radians = 0

# Error tools
error_font = pygame.font.Font('freesansbold.ttf', 64)
error_font2 = pygame.font.Font('freesansbold.ttf', 48)
is_error = False
is_draw = True

class game_logic:
    def line_color(self, last_pos, crnt_position):
        main_last_poso = math.pow(last_pos[0] - 400, 2)
        main_last_pos1 = math.pow(last_pos[1] - 400, 2)
        after_crnt_poso = math.pow(crnt_position[0] - 400, 2)
        after_crnt_pos1 = math.pow(crnt_position[1] - 400, 2)
        main_rad = math.sqrt(main_last_poso + main_last_pos1)
        after_rad = math.sqrt(after_crnt_poso + after_crnt_pos1)
        if main_rad - 20.0 <= after_rad and after_rad <= main_rad + 20.00:
            return (0, 225, 0)
        if after_rad > main_rad + 30.00:
            return (225, 0, 0)
        if after_rad < main_rad - 30.00:
            return (225, 0, 0)
        if after_rad > main_rad + 20.00:
            return (225, 225, 0)
        if after_rad < main_rad - 20.00:
            return (225, 225, 0)

    def cnt_score(self, total_sum, count, main_dot_val):
        std = math.sqrt(total_sum / count)
        percentage = abs(100 - (std / main_dot_val) * 100)
        return round(percentage, 1)

    def show_score(self, x, y, score_value):
        score = font2.render(str(score_value) + '%', True, GREEN)
        screen.blit(score, (x, y))

    def close_err(self, x, y):
        global is_draw
        is_draw = False
        error_text = error_font2.render('Too close to the center!', True, WHITE)
        restart_text = font.render('Press \'Space\' to try again!', True, WHITE)
        err()
        screen.blit(error_text, (x, y))
        screen.blit(restart_text, (x + 64, y + 64))

    def slow_err(self, x, y):
        global is_draw
        is_draw = False
        error_text = error_font.render('Too slow!', True, WHITE)
        restart_text = font.render('Press \'Space\' to try again!', True, WHITE)
        err()
        screen.blit(restart_text, (x - 30, y + 64))
        screen.blit(error_text, (x, y))

    def full_circle_err(self, x, y):
        global is_draw
        is_draw = False
        error_text = error_font.render('Draw a full circle!', True, WHITE)
        restart_text = font.render('Press \'SPACE\' to try again!', True, WHITE)
        err()
        screen.blit(restart_text, (x + 64, y + 64))
        screen.blit(error_text, (x, y))

    def game_over(self, x, y, score_val):
        global is_draw
        surface.fill((0, 0, 0))
        is_draw = False
        if score_val >= 80.0:
            error_text = error_font.render('Your Result! ' + str(score_val), True, WHITE)
            insert_value.append(score_val)
            screen.blit(error_text, (x + 30, y))
        else:
            err()
            error_text = error_font.render('Practise makes perfect!', True, YELLOW)
            insert_value.append(score_val)
            screen.blit(error_text, (x - 70, y))
        restart_text = font.render('Press \''
                                   'SPACE'
                                   '\' to play again!', True, WHITE)
        screen.blit(restart_text, (x + 64, y + 64))

    def restart_game(self, ):
        screen.fill((0, 0, 0))
        surface.fill((0, 0, 0))
        global drawing, last_pos, main_dot, total_sum, count, game_over, angle, arc_length, radians, is_error, is_draw, score_val
        drawing = False
        last_pos = None
        main_dot = None
        total_sum = 0
        count = 0
        game_over = False
        angle = 0
        arc_length = 0
        radians = 0
        is_error = False
        is_draw = True
        score_val = 0.00

game_logic = game_logic()

running = True
while running:
    screen.blit(surface, (368, 358))
    # Drawing a dot
    pygame.draw.circle(screen, RED, [400, 400],5)
    if score_val > 100.0:
        print(bcolors.FAIL + "OUT OF BOUNDS")
        err()
        game_logic.restart_game()

    # Main event circle drawing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and is_draw == True:
            drawing = True
            last_pos = pygame.mouse.get_pos()
            main_dot = pygame.mouse.get_pos()
            main_dot_val = math.sqrt(math.pow(main_dot[0] - 400, 2) + math.pow(main_dot[1] - 400, 2))
            start = time.time()
            start_ticks = pygame.time.get_ticks()

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if angle > 0 and angle < 2 * math.pi and is_error == False:
                game_logic.full_circle_err(150, 250)
                game_over = True

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                crnt_position = pygame.mouse.get_pos()
                pygame.draw.line(screen, game_logic.line_color(main_dot, crnt_position), last_pos, crnt_position, 5)

                # calculate the arc length
                arc = math.sqrt((crnt_position[0] - last_pos[0]) ** 2 + (crnt_position[1] - last_pos[1]) ** 2)
                arc_length += arc

                crnt_position_val = math.sqrt(math.pow(crnt_position[0] - 400, 2) + math.pow(crnt_position[1] - 400, 2))
                total_sum += (crnt_position_val - main_dot_val) ** 2
                count += 1
                radians += crnt_position_val
                score_val = game_logic.cnt_score(total_sum, count, main_dot_val)
                last_pos = crnt_position
                angle = arc_length / (radians / count)

                # close error
                if crnt_position_val <= 35:
                    game_logic.close_err(150, 250)
                    drawing = False
                    is_error = True
                    game_over = True

                # too slow timer
                end = time.time()
                if end - start >= 5:
                    game_logic.slow_err(250, 250)
                    drawing = False
                    is_error = True
                    game_over = True

                if angle > 2 * math.pi:
                    drawing = False
                    game_over = True
                    game_logic.game_over(100, 100, score_val)

    surface.fill((0, 0, 0))  # Updating results
    game_logic.show_score(textX, textY, score_val)
    screen.blit(cc, (16, 32))
    screen.blit(cc1, (16, 50))
    screen.blit(cc2, (16, 70))
    pygame.display.flip()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_logic.restart_game()

connection.commit()
cursor.close()
pygame.quit()
