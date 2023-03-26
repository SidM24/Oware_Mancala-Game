import sys

import pygame
import game as gamemodule

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
light_black = (60, 35, 23)
blue = (0, 0, 255)
light_blue = (38, 42, 86)

red = (255, 0, 0)
green = (0, 255, 0)
orange = (184, 98, 27)
background = (227, 204, 174)

# Global Variables
x_coordinate = 50
y_coordinate = 100
length = 800
width = 300
turn = -1
obj = gamemodule.Mancala_Board(None)
gameWindow = pygame.display.set_mode((900, 500))

# To quit and close the game
exit_game = False
game_over = False


# To open the Game Window
def open_game_window():
    global gameWindow
    x = pygame.init()
    gameWindow = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("Oware Mancala")
    pygame.display.update()


# To draw a button on the screen
def draw_button(button_x, button_y, button_width, button_height, button_color, button_text, text_color, font_size=40):
    font = pygame.font.SysFont(None, font_size)
    button_rect = pygame.draw.rect(gameWindow, button_color, (button_x, button_y, button_width, button_height),
                                   border_radius=15)
    button_text_surface = font.render(button_text, True, text_color)
    button_text_x = button_x + button_width // 2 - button_text_surface.get_width() // 2
    button_text_y = button_y + button_height // 2 - button_text_surface.get_height() // 2
    gameWindow.blit(button_text_surface, (button_text_x, button_text_y))
    return button_rect


# Design of Display of the home screen
def choice_display():
    gameWindow.fill(background)
    blit(50, black, "Welcome to Oware Mancala !!!", 450, 75, 'didot.ttc')
    blit(35, blue, "Created by Chhichhore", 450, 120)
    pygame.draw.rect(gameWindow, light_blue, (200, 175, 500, 50), border_radius=15)
    blit(50, white, "Select Game Mode", 450, 200)
    single_player_rect = draw_button(100, 275, 250, 50, black, "Player vs CPU", white)
    two_player_rect = draw_button(550, 275, 250, 50, black, "Player vs Player", white)
    pygame.display.update()
    return single_player_rect, two_player_rect


# Function to get the user choice of gameplay
def user_choice():
    single_player_rect, two_player_rect = choice_display()
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if single_player_rect.collidepoint(mouse_pos):
                    print("Player vs CPU")
                    single_player_game()
                elif two_player_rect.collidepoint(mouse_pos):
                    print("Player vs Player")
                    two_player_game()

        pygame.display.update()


# Function to play the single player game
def single_player_game():
    draw_board_again()
    start(1)
    single_game_loop()


# Function to play the multiplayer game
def two_player_game():
    draw_board_again()
    start(2)
    two_player_game_loop()


# Utility function
def blit(size, color, input_text, x, y, style=None):
    font = pygame.font.SysFont(style, size)
    text = font.render(input_text, True, color)
    text_rect = text.get_rect(center=(x, y))
    gameWindow.blit(text, text_rect)


# To draw the board on the game window
def draw_board_again():
    gameWindow.fill(background)
    pygame.draw.rect(gameWindow, light_black, [x_coordinate, y_coordinate, length, width], border_radius=15)
    ssss = 70
    for ii in range(6):
        pygame.draw.circle(gameWindow, background, ((130 + ssss), 330), 30)
        ssss = ssss + 100
    ssss = 70
    for ii in range(6):
        pygame.draw.circle(gameWindow, background, ((130 + ssss), 180), 30)
        ssss = ssss + 100
    # Player 1 score box
    pygame.draw.rect(gameWindow, light_blue, [325, 420, 250, 60], border_radius=20)
    # Player 1 scoring pit
    pygame.draw.rect(gameWindow, background, [70, 180, 60, 150], border_radius=20)
    # Player 2 score box
    pygame.draw.rect(gameWindow, light_blue, [325, 20, 250, 60], border_radius=20)
    # Player 2 scoring pit
    pygame.draw.rect(gameWindow, background, [770, 180, 60, 150], border_radius=20)
    pygame.display.update()


# Function to update the mancala board after every move performed
def draw_board(board, game, player_turn=1):
    draw_board_again()
    home_button = draw_button(30, 25, 100, 40, black, "Home", "white", 30)
    restart_button = draw_button(30, 425, 100, 40, black, "Restart", "white", 30)
    # for player 1
    sp = 0
    for j in range(0, 6, 1):
        blit(20, white, str(j + 1), (200 + sp), 370)
        blit(50, black, str(board[j]), (200 + sp), 330)
        sp = sp + 100
    # for player 2
    player2_list = ['s', 'd', 'f', 'g', 'h', 'j']
    sp = 0
    for j in range(12, 6, -1):
        if game == 2:
            blit(20, white, player2_list[abs(j - 12)], (200 + sp), 140)
        blit(50, black, str(board[j]), (200 + sp), 180)
        sp = sp + 100

    # Displaying the score for player 1
    blit(50, green if player_turn == 1 else white, ("YOU: " if game == 1 else "Player 1: ") + str(board[6]), 450, 450)

    # To display player 1 pit
    blit(50, black, str(board[6]), 800, 250)

    # Displaying the score for player 2
    blit(50, green if player_turn == 2 else white, ("CPU: " if game == 1 else "Player 2: ") + str(board[13]), 450, 50)

    # To display the player 2 pit
    blit(50, black, str(board[13]), 100, 250)

    return home_button, restart_button


# Function to display the final score on the screen
def final_score(ss, board, t):
    gameWindow.fill(background)
    pygame.draw.rect(gameWindow, black, [x_coordinate, y_coordinate, length, width], border_radius=15)
    font = pygame.font.SysFont(None, 40)

    # Final Score Title
    blit(60, green, "Final Scores", 450, 150)

    # Player 1 final score
    blit(45, blue, "YOU" if t == 1 else "Player 1", 200, 230)
    blit(45, blue, str(board[6]), 200, 265)

    # Player 2 final score
    blit(45, blue, "CPU" if t == 1 else "Player 2", 700, 230)
    blit(45, blue, str(board[13]), 700, 265)

    # Displaying who won
    blit(50, white, ss, 450, 250)
    obj.print_mancala()
    print('GAME ENDED')

    # Play again and Home Buttons
    play_again_rect = draw_button(150, 325, 200, 50, light_blue, "Play Again", white)
    home_rect = draw_button(550, 325, 200, 50, light_blue, "Home", white)
    pygame.display.update()
    return play_again_rect, home_rect


# Function to start the game
def start(xx):
    global exit_game
    exit_game = False
    global obj
    obj = gamemodule.Mancala_Board(None)
    global turn
    turn = 1
    draw_board(obj.mancala, xx)
    pygame.display.update()


# Function to see what to do when a game has finished
def check_the_final_action(s, game):
    play_again_rect, home_rect = final_score(s, obj.mancala, game)
    flag = False
    while not flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    if game == 1:
                        single_player_game()
                    elif game == 2:
                        two_player_game()
                elif home_rect.collidepoint(mouse_pos):
                    user_choice()


def error_message(game, turn_here):
    blit(40, red, "Invalid Move", 450, 250)
    pygame.display.update()
    pygame.time.delay(400)
    draw_board(obj.mancala, game, turn_here)
    pygame.display.update()


# Main game loop for single player
def single_game_loop():
    global exit_game
    global turn
    home_button, restart_button = draw_board(obj.mancala, 1, turn)
    pygame.display.update()
    while not exit_game:
        if obj.isEnd():
            turn = -1
            exit_game = True
        # Player 1 (Human Player turn)
        while turn == 1:
            if obj.isEnd():
                turn = -1
                exit_game = True
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if home_button.collidepoint(mouse_pos):
                        print("Home Button")
                        user_choice()
                    if restart_button.collidepoint(mouse_pos):
                        print("Restart Button")
                        single_player_game()
                # Player 1 moves
                if event.type == pygame.KEYDOWN:
                    if event.unicode not in ['1', '2', '3', '4', '5', '6'] or obj.mancala[int(event.unicode) - 1] == 0:
                        print("You can't Play at this position. Choose another position")
                        error_message(1, turn)
                        continue
                    turn_flag = obj.player_move(int(event.unicode) - 1)
                    obj.print_mancala()
                    if not turn_flag:
                        turn = 2
                    draw_board(obj.mancala, 1, turn)
                    pygame.display.update()

        # while loop for AI-Bot/ Player 2
        while turn == 2:
            if obj.isEnd():
                turn = -1
                exit_game = True
                break
            heurisitic, k = gamemodule.alphabeta(obj, 10, -100000, 100000, True)
            print("AI-BOT TURN >>> ", end="")
            print(k)
            turn_flag = obj.player_move(k)
            obj.print_mancala()
            if not turn_flag:
                turn = 1
            draw_board(obj.mancala, 1, turn)
            pygame.display.update()
        if turn == -1:
            s = ""
            if obj.mancala[6] < obj.mancala[13]:
                s = "CPU WINS"
            else:
                s = "YOU WIN"

            check_the_final_action(s, 1)


# Two Player game loop
def two_player_game_loop():
    global exit_game
    global turn
    home_button, restart_button = draw_board(obj.mancala, 2, turn)
    pygame.display.update()
    while not exit_game:
        if obj.isEnd():
            turn = -1
            exit_game = True
        # Player 1 turn
        while turn == 1:
            if obj.isEnd():
                turn = -1
                exit_game = True
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if home_button.collidepoint(mouse_pos):
                        print("Home Button Clicked")
                        user_choice()
                    if restart_button.collidepoint(mouse_pos):
                        print("Restart Button Clicked")
                        two_player_game()
                # Player 1 moves
                if event.type == pygame.KEYDOWN:
                    if event.unicode not in ['1', '2', '3', '4', '5', '6'] or obj.mancala[int(event.unicode) - 1] == 0:
                        print("You can't Play at this position. Choose another position")
                        error_message(2, turn)
                        continue
                    turn_flag = obj.player_move(int(event.unicode) - 1)
                    obj.print_mancala()
                    if not turn_flag:
                        turn = 2
                    draw_board(obj.mancala, 2, turn)
                    pygame.display.update()
        # Player 2 turn
        while turn == 2:
            if obj.isEnd():
                turn = -1
                exit_game = True
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if home_button.collidepoint(mouse_pos):
                        print("Home Button Clicked")
                        user_choice()
                    if restart_button.collidepoint(mouse_pos):
                        print("Restart Button Clicked")
                        two_player_game()
                # Player 2 moves
                player2_dict = {'s': 12, 'd': 11, 'f': 10, 'g': 9, 'h': 8, 'j': 7}
                if event.type == pygame.KEYDOWN:
                    if event.unicode not in ['s', 'd', 'f', 'g', 'h', 'j'] or obj.mancala[
                        int(player2_dict[event.unicode])] == 0:
                        print("You can't Play at this position. Choose another position")
                        error_message(2, turn)
                        continue

                    turn_flag = obj.player_move(int(player2_dict[event.unicode]))
                    obj.print_mancala()
                    if not turn_flag:
                        turn = 1
                    draw_board(obj.mancala, 2, turn)
                    pygame.display.update()
        if turn == -1:
            s = ""
            if obj.mancala[6] < obj.mancala[13]:
                s = "Player2 Won"
            else:
                s = "Player1 Won"

            check_the_final_action(s, 2)


open_game_window()
user_choice()
pygame.quit()
quit()
