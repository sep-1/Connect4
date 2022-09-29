"""
Name: Sepehr Rajabian
Title: Connect 4!
Date: January 10, 2022
Description: A connect 4 program that allows that allows two players to play a game of connect 4 against each other. Each player moves with different keys which are outlined in the game's how to play section and game experience.
"""
import pygame
import os
pygame.init()
"""
Status Legend: 
0: white
1: red 
2: yellow
"""

#pygame environment setup
FPS = 30
win_height = 1080
win_width = 1920
win = pygame.display.set_mode((win_width, win_height))
center_win = win.get_rect().center
pygame.display.set_caption("Connect4!")
music_theme = pygame.mixer.music.load(os.path.join("assets", "Core.wav"))
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

#images
menu_img = pygame.image.load(os.path.join("assets", "menubackground.jpg"))
game_bg_image = pygame.image.load(os.path.join("assets", "sidebackground.jpg"))
clear_bg_left = pygame.image.load(os.path.join("assets", "clear_left.jpg"))
clear_bg_right = pygame.image.load(os.path.join("assets", "clear_right.jpg"))

#fonts  
menu_title_font = pygame.font.Font("textfonts\GoldenSentry-pXBv.ttf", 200)
menu_text_font = pygame.font.Font(os.path.join("textfonts", "ABSTRACT.TTF"), 20)
common_text_font = pygame.font.Font(os.path.join("textfonts", "upheavtt.ttf"), 30)
keyboard_font = pygame.font.Font(os.path.join("textfonts", "212Keyboard-lmRZ.otf"), 150)

#RGB data
game_bg = (65,105,225)
menu_button_colour = (0,0,240)
menu_selected_colour = (0,0,170)
menu_text_colour = (150, 9, 80)

def draw_board():
    """
    draws a connect 4 board on the UI, and creates a 7 column and 6 row 2D list that contains rect values for drawn blank spaces 
    on the UI (representing open slots). 
    :return: 7 * 6 list containing rect values of a drawn position with a status of 0 (indicating that that space is open)
    """
    board_colour = (0,0,140)
    game_array = [[""] * 7 for _ in range(6)]
    grid_width, grid_height = 1000, 800
    win.blit(game_bg_image, (0,0))
    board_canvas = pygame.Rect(win_width/5, 0, 3*win_width/5, win_height)
    pygame.draw.rect(win, game_bg, board_canvas)
    anchor_width = win_width/2 - grid_width/2
    anchor_height = win_height/2 - grid_height/2
    main_grid = pygame.Rect(0,0, grid_width, grid_height)
    main_grid.center = center_win
    side_legs = pygame.Rect(0, 0, 25, 600)
    side_legs.topright = main_grid.midleft
    pygame.draw.rect(win, board_colour, side_legs)
    side_legs.topleft = main_grid.midright
    pygame.draw.rect(win, board_colour, side_legs)
    pygame.draw.rect(win, board_colour, main_grid)
    height_incrementer = anchor_height + 80
    for r in range(6):
        width_incrementer = anchor_width + 108
        for c in range(7):
            game_array[r][c] = {"coord": pygame.draw.circle(win, game_bg,(width_incrementer, height_incrementer),40), "status": 0}
            width_incrementer += 130
        height_incrementer += 130
    return game_array

def take_turn(game_array, team, board_column):
    """
    contains all the functions related to completing a player's turn after completing their choice.
    This includes placing a chip on the 2D list and UI as well as checking for a win.
    :param game_array: - List
    :param team: - integer
    :param board_column: - integer
    :returns game status for whether game is win, invalid move, or nothing: - int
    """
    def place_chip():
        """
        Places a chip on the UI and updates the 2D list to contain a new drawn circle object (different colour) 
        and a new status indicating what type of chip resides there. Checks all rows in the column to find
        the first open row, starting from the top.
        :return: the index of the highest open row that has now been filled OR -1 if no open spots are 
        found in that column. - integer 
        """
        for row in range(5,-1,-1):
            if game_array[row][board_column]["status"] == 0:
                old_circle = game_array[row][board_column]["coord"]
                game_array[row][board_column]["status"] = team
                if team == 1:
                    game_array[row][board_column]["coord"] = pygame.draw.circle(win, (255,0,0),(old_circle.center),40)
                elif team == 2:
                    game_array[row][board_column]["coord"] = pygame.draw.circle(win, (255,255,0),(old_circle.center),40)
                return row
        return -1
    def check_for_win(row, column):
        """
        Iterates around the placed chip to look for any possibility of a connect 4. 
        :param: row - int
        :param: column - int
        :return: returns 1 if a win is found, 0 otherwise. - int
        """
        winner = False
        start_win_point = ""
        end_win_point = ""
        #down vertical check
        for i in range(0,4):
            if row+i > 5 or game_array[row+i][column]["status"] != team:
                break
        else:
            start_win_point = game_array[row][column]["coord"]
            end_win_point = game_array[row+i][column]["coord"]
            winner = True
        #horizontal check
        for dev in range(0,-4,-1):
            for i in range(dev,4+dev):
                if not 0 <= column+i <= 6 or game_array[row][column+i]["status"] != team:
                    break
            else:
                start_win_point = game_array[row][column+dev]["coord"]
                end_win_point = game_array[row][column+i]["coord"]
                winner = True
        #diagonal right down and left up check
        for dev in range(0,-4,-1):
            for i in range(dev,4+dev):
                if not 0 <= column+i <= 6 or not 0 <= row+i <= 5 or game_array[row+i][column+i]["status"] != team:
                    break
            else:
                start_win_point = game_array[row+dev][column+dev]["coord"]
                end_win_point = game_array[row+i][column+i]["coord"]
                winner = True
        #diagonal right up and left down check
        for dev in range(0,-4,-1):
            for i in range(dev,4+dev):
                if not 0 <= column+i <= 6 or not 0 <= row-i <= 5 or game_array[row-i][column+i]["status"] != team:
                    break
            else:
                start_win_point = game_array[row-dev][column+dev]["coord"]
                end_win_point = game_array[row-i][column+i]["coord"]
                winner = True
        if winner:
            pygame.draw.line(win, (150, 9, 80), start_win_point.center, end_win_point.center, 5)
            pygame.draw.circle(win,(150, 9, 80), start_win_point.center, 15)
            pygame.draw.circle(win,(150, 9, 80), end_win_point.center, 15)
            if team == 1:
                draw_text(win, "Red Wins!", menu_title_font, (200, 0, 0), win_width/2, win_height/2)
            elif team == 2:
                draw_text(win, "Yellow Wins!", menu_title_font, (200,200,0), win_width/2, win_height/2)
            return 1 
        else:
            return 0
    board_row = place_chip()
    if board_row == -1: return -1
    game_status = check_for_win(board_row, board_column) 
    pygame.display.update()
    return game_status      
    
    

def draw_text(surface, text, font, colour, x, y):
    """
    draws given text on the UI for user, with given properties.
    :param: surface - pygame.display object
    :param: text - string
    :param: font pygame.font.Font type
    :param: colour - RGB tuple
    :param: x - int
    :param: y - int
    :return: text_obj, a rendered font object
    """
    text_obj = font.render(text, 1, colour)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x - text_obj.get_width()/2,y - text_obj.get_height()/2)
    surface.blit(text_obj, text_rect)
    return text_obj

def draw_button(text, selected_colour, font_colour, font, x,y):
    """
    :param: text - string
    :param: selected_colour - RGB tuple
    :param: font_colour - RGB tuple
    :param: font pygame.font.Font type
    :param: x - int
    :param: y - int
    :return: text_rect, a rect object for the text. 
    """
    text_obj = font.render(text, 1, font_colour)
    text_rect = text_obj.get_rect()
    text_rect.center = (x,y)
    win.blit(text_obj, text_rect)
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos):
        text_obj = font.render(text, 1, selected_colour)
        win.blit(text_obj, text_rect)
    return text_rect


def main():
    """
    runs the main program
    """
    #main running var
    running = True 

    #tween counters
    x_count = 0
    y_count = 0

    #menu page booleans
    tween = False
    game = False
    menu = True
    tutorial = False
    replay_screen = False
    
    #game data
    selected_column = 0
    chip_tween = -2
    team = 1
    board = 0
    while running:
        pygame.time.Clock().tick(FPS)
        #menu render
        if menu:
            win.blit(menu_img, (0,0))
            draw_text(win, "Connect 4!", menu_title_font, menu_text_colour, win_width/2, win_height*0.15)
            play_button = draw_button("Play!", menu_selected_colour, menu_text_colour , menu_text_font, win_width/2, win_height*.35)
            how_to_play = draw_button("How to Play", menu_selected_colour, menu_text_colour, menu_text_font, win_width/2, win_height*.5)
            exit_button = draw_button("Exit", menu_selected_colour, menu_text_colour, menu_text_font, win_width/2, win_height*.65)
        #tween transitions
        if tween:
            transition_square_rect = pygame.Rect(0,0,0,0)
            transition_square_rect.size = (x_count, y_count)
            transition_square_rect.center = (win_width/2, win_height/2)
            pygame.draw.rect(win, game_bg, transition_square_rect)
            if x_count < 2000:
                x_count += 120
            if y_count < 1150:
                y_count += 120
            if x_count >= 2000 and y_count >= 1150:
                tween = False
                if not board:
                    board = draw_board()
                    game = True
                else:
                    board = 0 
                    team = 1 
                    selected_column = 0
                    replay_screen = True
                x_count = 0
                y_count = 0
        #game render
        if game:
            chip_colour = 0
            if team == 1:
                draw_text(win, "Red Team's Turn!", common_text_font, menu_text_colour, win_width*.1, win_height*.1)
                draw_text(win, "A D", keyboard_font, menu_text_colour, win_width*.1, win_height*.25)
                draw_text(win, "w", keyboard_font, (255, 45, 120), win_width*.1, win_height*.4)
                chip_colour = (255,0,0)
            elif team == 2:
                draw_text(win, "Yellow Team's Turn!", common_text_font, menu_text_colour, win_width*.9, win_height*.1)
                draw_text(win, "s t", keyboard_font, menu_text_colour, win_width*.9, win_height*.25)            
                draw_text(win, "g", keyboard_font, (255, 45, 120), win_width*.9, win_height*.4)
                chip_colour = (255,255,0)
            if selected_column == chip_tween + 1:
                if x_count < (board[0][selected_column]["coord"].x - board[0][chip_tween]["coord"].x):
                    start_pos = board[0][chip_tween]["coord"].center - pygame.Vector2(0,140)
                    pygame.draw.circle(win, game_bg, start_pos + pygame.Vector2(x_count,0), 40)
                    x_count += 26
                    pygame.draw.circle(win, chip_colour , start_pos + pygame.Vector2(x_count,0), 40)
                else:
                    x_count = 0
                    chip_tween = -2
            elif selected_column == chip_tween - 1:
                if x_count < (board[0][chip_tween]["coord"].x - board[0][selected_column]["coord"].x):
                    start_pos = board[0][chip_tween]["coord"].center - pygame.Vector2(0,140)
                    pygame.draw.circle(win, game_bg, start_pos - pygame.Vector2(x_count,0), 40)
                    x_count += 26
                    pygame.draw.circle(win, chip_colour , start_pos - pygame.Vector2(x_count,0), 40)
                else:
                    x_count = 0
                    chip_tween = -2
            else:
                pygame.draw.circle(win, chip_colour , board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
        #how to play section render
        if tutorial:
            win.blit(menu_img, (0,0))
            draw_text(win, "How to play connect 4:", common_text_font, menu_text_colour, win_width*.5, win_height*.15)
            draw_text(win,"A game of connect 4 involves 2 players who each place chips on a 6 by 7 grid.", common_text_font, menu_text_colour,win_width*.5, win_height*.25)
            draw_text(win,"To win, 4 of your chips must align vertically, horizontally, or diagonally.", common_text_font, menu_text_colour,win_width*.5, win_height*.3)
            draw_text(win, "The red player uses [A] and [D] to move left and right respectively across the board.", common_text_font, menu_text_colour,win_width*.5, win_height*.35)
            draw_text(win, "The yellow player uses the [LEFT] and [RIGHT] arrows to move across the board.", common_text_font, menu_text_colour,win_width*.5, win_height*.4)
            draw_text(win, "To confirm a chip placement, the red player presses [SPACE] and the yellow player presses right [SHIFT].", common_text_font, menu_text_colour,win_width*.5, win_height*.45)
            return_button = draw_button("< Back", menu_selected_colour, menu_text_colour,menu_text_font, win_width*.3, win_height*.15)
        #replay screen render
        if replay_screen:
            win.blit(menu_img, (0,0))
            draw_text(win, "Congratulations on your connect 4 win!", common_text_font, menu_text_colour, win_width*.5, win_height*.5)
            menu_return_button = draw_button("Menu", menu_selected_colour, menu_text_colour, menu_text_font, win_width*.4, win_height*.6)
            replay_button = draw_button("Replay", menu_selected_colour, menu_text_colour, menu_text_font, win_width*.6, win_height*.6)
        mouse_pos = pygame.mouse.get_pos()

        #input check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and ((play_button.collidepoint(mouse_pos) and menu) or (replay_screen and replay_button.collidepoint(mouse_pos))):
                menu = False
                replay_screen = False
                tween = True
            elif event.type == pygame.MOUSEBUTTONDOWN and how_to_play.collidepoint(mouse_pos) and menu:
                menu = False
                tutorial = True
            elif event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(mouse_pos) and menu:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and ((tutorial and return_button.collidepoint(mouse_pos)) or (replay_screen and menu_return_button.collidepoint(mouse_pos))):
                tutorial = False
                replay_screen = False
                menu = True
            if event.type == pygame.KEYDOWN and game and not tween:
                if (event.key == pygame.K_d and team == 1) or (event.key == pygame.K_RIGHT and team == 2):
                    if selected_column >= 6:
                        if chip_tween == -2:
                            pygame.draw.circle(win, game_bg , board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
                            selected_column = 0
                    else:
                        if chip_tween == -2:
                            chip_tween = selected_column
                            selected_column += 1
                elif (event.key == pygame.K_a and team == 1) or (event.key == pygame.K_LEFT and team == 2):
                    if selected_column <= 0:
                        if chip_tween == -2:
                            pygame.draw.circle(win, game_bg , board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
                            selected_column = 6
                    else:
                        if chip_tween == -2:
                            chip_tween = selected_column
                            selected_column -= 1
                elif (event.key == pygame.K_SPACE and team == 1) or (event.key == pygame.K_RSHIFT and team == 2):
                    game_status = take_turn(board,team,selected_column)
                    clear_pillar_rects = pygame.Rect(0,0,win_width*.2,win_height)
                    if game_status == 1:
                        game = False
                        pygame.time.delay(3500)
                        tween = True
                    elif game_status == -1:
                        break
                    if team == 1:
                        win.blit(clear_bg_left, clear_pillar_rects)
                        team = 2
                    elif team == 2:
                        clear_pillar_rects.topright = (win_width, 0)
                        win.blit(clear_bg_right, clear_pillar_rects)
                        team = 1 
        pygame.display.update()

if __name__ == "__main__":
    main()


"""
Main Variables/Constants/Initiations:
import pygame
import os
initiate pygame
FPS = 30
win_height = 1080
win_width = 1920
win = pygame.display.set_mode((win_width, win_height))
center_win = win.get_rect().center
pygame.display.set_caption("Connect4!")
music_theme = pygame.mixer.music.load(os.path.join("assets", "Core.wav"))
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

menu_img = pygame.image.load(os.path.join("assets", "menubackground.jpg"))
game_bg_image = pygame.image.load(os.path.join("assets", "sidebackground.jpg"))

menu_title_font = pygame.font.Font("textfonts\GoldenSentry-pXBv.ttf", 200)
menu_text_font = pygame.font.Font(os.path.join("textfonts", "ABSTRACT.TTF"), 20)
common_text_font = pygame.font.Font(os.path.join("textfonts", "upheavtt.ttf"), 30)
keyboard_font = pygame.font.Font(os.path.join("textfonts", "212Keyboard-lmRZ.otf"), 150)
clear_bg_left = pygame.image.load(os.path.join("assets", "clear_left.jpg"))
clear_bg_right = pygame.image.load(os.path.join("assets", "clear_right.jpg"))

game_bg = (65,105,225)
menu_button_colour = (0,0,240)
menu_selected_colour = (0,0,170)
menu_text_colour = (150, 9, 80)

Pseudocode functions:

function draw_board() {
    board_colour = (0,0,140)
    game_array = [[""] * 7 loop for _ = 0,6]
    grid_width, grid_height = 1000, 800
    win.blit(game_bg_image, (0,0))
    board_canvas = pygame.Rect(win_width/5, 0, 3*win_width/5, win_height)
    pygame.draw.rect(win, game_bg, board_canvas)
    anchor_width = win_width/2 - grid_width/2
    anchor_height = win_height/2 - grid_height/2
    main_grid = pygame.Rect(0,0, grid_width, grid_height)
    main_grid.center = center_win
    side_legs = pygame.Rect(0, 0, 25, 600)
    side_legs.topright = main_grid.midleft
    pygame.draw.rect(win, board_colour, side_legs)
    side_legs.topleft = main_grid.midright
    pygame.draw.rect(win, board_colour, side_legs)
    pygame.draw.rect(win, board_colour, main_grid)
    height_incrementer = anchor_height + 80
    loop for r = 0,6
        width_incrementer = anchor_width + 108
        loop for c = 0,7
            game_array[r][c] = {"coord": pygame.draw.circle(win, game_bg,(width_incrementer, height_incrementer),40), "status": 0}
            width_incrementer = width_incrementer + 130
        end for loop
        height_incrementer = height_incrementer + 130
    end for loop
    return game_array
}
end draw_board

function take_turn(game_array, team, board_column) {
    function place_chip() {
        loop for row = 5,-1,-1
            if game_array[row][board_column]["status"] == 0
                old_circle = game_array[row][board_column]["coord"]
                game_array[row][board_column]["status"] = team
                if team == 1
                    game_array[row][board_column]["coord"] = pygame.draw.circle(win, (255,0,0),(old_circle.center),40)
                else if team == 2
                    game_array[row][board_column]["coord"] = pygame.draw.circle(win, (255,255,0),(old_circle.center),40)
                end if 
                return row
            end if 
        return -1
    }
    end place_chip

    function check_for_win(row, column) {
        winner = False
        start_win_point = ""
        end_win_point = ""
        #down vertical check
        loop for i = 0,4
            if row+i > 5 or game_array[row+i][column]["status"] != team
                break
            end if 
        else
            start_win_point = game_array[row][column]["coord"]
            end_win_point = game_array[row+i][column]["coord"]
            winner = True
        end for loop 
        loop for dev = 0,-4,-1
            loop for i = dev,4+dev
                if not 0 <= column+i <= 6 or game_array[row][column+i]["status"] != team
                    break
                end if 
            else
                start_win_point = game_array[row][column+dev]["coord"]
                end_win_point = game_array[row][column+i]["coord"]
                winner = True
            end for loop
        end for loop
        loop for dev = 0,-4,-1
            loop for i = dev, 4+dev
                if not 0 <= column+i <= 6 or not 0 <= row+i <= 5 or game_array[row+i][column+i]["status"] != team
                    break
                end if
            else
                start_win_point = game_array[row+dev][column+dev]["coord"]
                end_win_point = game_array[row+i][column+i]["coord"]
                winner = True
            end for loop
        end for loop
        loop for dev = 0,-4,-1
            loop for i = dev, 4+dev
                if not 0 <= column+i <= 6 or not 0 <= row-i <= 5 or game_array[row-i][column+i]["status"] != team
                    break
                end if 
            else
                start_win_point = game_array[row-dev][column+dev]["coord"]
                end_win_point = game_array[row-i][column+i]["coord"]
                winner = True
            end for loop
        end for loop
        if winner == True
            pygame.draw.line(win, (150, 9, 80), start_win_point.center, end_win_point.center, 5)
            pygame.draw.circle(win,(150, 9, 80), start_win_point.center, 15)
            pygame.draw.circle(win,(150, 9, 80), end_win_point.center, 15)
            if team == 1
                draw_text(win, "Red Wins!", menu_title_font, (200, 0, 0), win_width/2, win_height/2)
            else if team == 2
                draw_text(win, "Yellow Wins!", menu_title_font, (200,200,0), win_width/2, win_height/2)
            end if 
            return 1 
        else
            return 0
        end if 
    }
    end check_for_win

    board_row = place_chip()
    if board_row == -1 return -1 end if 
    game_status = check_for_win(board_row, board_column) 
    pygame.display.update()
    return game_status      
}
    

function draw_text(surface, text, font, colour, x, y) {
    text_obj = font.render(text, 1, colour)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x - text_obj.get_width()/2,y - text_obj.get_height()/2)
    surface.blit(text_obj, text_rect)
    return text_obj
}
end draw_text

function draw_button(text, selected_colour, font_colour, font, x,y) {
    text_obj = font.render(text, 1, font_colour)
    text_rect = text_obj.get_rect()
    text_rect.center = (x,y)
    win.blit(text_obj, text_rect)
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos)
        text_obj = font.render(text, 1, selected_colour)
        win.blit(text_obj, text_rect)
    end if 
    return text_rect
}
end draw_button

Main Program {
    running = True 

    x_count = 0
    y_count = 0

    tween = False
    game = False
    menu = True
    tutorial = False
    replay_screen = False
    
    selected_column = 0
    chip_tween = -2
    team = 1
    board = 0
    loop while running == True
        pygame.time.Clock().tick(FPS)
        if menu == True
            win.blit(menu_img, (0,0))
            draw_text(win, "Connect 4!", menu_title_font, menu_text_colour, win_width/2, win_height*0.15)
            play_button = draw_button("Play!", menu_selected_colour, menu_text_colour , menu_text_font, win_width/2, win_height*.35)
            how_to_play = draw_button("How to Play", menu_selected_colour, menu_text_colour, menu_text_font, win_width/2, win_height*.5)
            exit_button = draw_button("Exit", menu_selected_colour, menu_text_colour, menu_text_font, win_width/2, win_height*.65)
        end if 
        if tween == True
            transition_square_rect = pygame.Rect(0,0,0,0)
            transition_square_rect.size = (x_count, y_count)
            transition_square_rect.center = (win_width/2, win_height/2)
            pygame.draw.rect(win, game_bg, transition_square_rect)
            if x_count < 2000
                x_count = x_count + 120
            if y_count < 1150
                y_count = y_count + 120
            if x_count >= 2000 and y_count >= 1150
                tween = False
                if not board
                    board = draw_board()
                    game = True
                else
                    board = 0 
                    team = 1 
                    selected_column = 0
                    replay_screen = True
                x_count = 0
                y_count = 0
        end if 
        if game == True
            chip_colour = 0
            if team == 1
                draw_text(win, "Red Team's Turn!", common_text_font, menu_text_colour, win_width*.1, win_height*.1)
                draw_text(win, "A D", keyboard_font, menu_text_colour, win_width*.1, win_height*.25)
                draw_text(win, "w", keyboard_font, (255, 45, 120), win_width*.1, win_height*.4)
                chip_colour = (255,0,0)
            else if team == 2
                draw_text(win, "Yellow Team's Turn!", common_text_font, menu_text_colour, win_width*.9, win_height*.1)
                draw_text(win, "s t", keyboard_font, menu_text_colour, win_width*.9, win_height*.25)            
                draw_text(win, "g", keyboard_font, (255, 45, 120), win_width*.9, win_height*.4)
                chip_colour = (255,255,0)
            end if 
            if selected_column == chip_tween + 1 
                if x_count < (board[0][selected_column]["coord"].x - board[0][chip_tween]["coord"].x)
                    start_pos = board[0][chip_tween]["coord"].center - pygame.Vector2(0,140)
                    pygame.draw.circle(win, game_bg, start_pos + pygame.Vector2(x_count,0), 40)
                    x_count = x_count + 26
                    pygame.draw.circle(win, chip_colour , start_pos + pygame.Vector2(x_count,0), 40)
                else
                    x_count = 0
                    chip_tween = -2
                end if 
            else if selected_column == chip_tween - 1
                if x_count < (board[0][chip_tween]["coord"].x - board[0][selected_column]["coord"].x)
                    start_pos = board[0][chip_tween]["coord"].center - pygame.Vector2(0,140)
                    pygame.draw.circle(win, game_bg, start_pos - pygame.Vector2(x_count,0), 40)
                    x_count = x_count + 26
                    pygame.draw.circle(win, chip_colour , start_pos - pygame.Vector2(x_count,0), 40)
                else
                    x_count = 0
                    chip_tween = -2
            else
                pygame.draw.circle(win, chip_colour, board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
            end if 
        if tutorial == True
            win.blit(menu_img, (0,0))
            draw_text(win, "How to play connect 4:", common_text_font, menu_text_colour, win_width*.5, win_height*.15)
            draw_text(win,"A game of connect 4 involves 2 players who each place chips on a 6 by 7 grid.", common_text_font, menu_text_colour,win_width*.5, win_height*.25)
            draw_text(win,"To win, 4 of your chips must align vertically, horizontally, or diagonally.", common_text_font, menu_text_colour,win_width*.5, win_height*.3)
            draw_text(win, "The red player uses [A] and [D] to move left and right respectively across the board.", common_text_font, menu_text_colour,win_width*.5, win_height*.35)
            draw_text(win, "The yellow player uses the [LEFT] and [RIGHT] arrows to move across the board.", common_text_font, menu_text_colour,win_width*.5, win_height*.4)
            draw_text(win, "To confirm a chip placement, the red player presses [SPACE] and the yellow player presses right [SHIFT]", common_text_font, menu_text_colour,win_width*.5, win_height*.45)
            return_button = draw_button("< Back", menu_selected_colour, menu_text_colour,menu_text_font, win_width*.3, win_height*.15)
        end if 
        if replay_screen == True
            win.blit(menu_img, (0,0))
            draw_text(win, "Congratulations on your connect 4 win!", common_text_font, menu_text_colour, win_width*.5, win_height*.5)
            menu_return_button = draw_button("Menu", menu_selected_colour, menu_text_colour, menu_text_font, win_width*.4, win_height*.6)
            replay_button = draw_button("Replay", menu_selected_colour, menu_text_colour, menu_text_font, win_width*.6, win_height*.6)
        end if 
        mouse_pos = get mouse position
        loop for event in pygame.event.get()
            if event.type == pygame.QUIT
                running = False
            end if 
            if event.type == pygame.MOUSEBUTTONDOWN and ((play_button.collidepoint(mouse_pos) and menu) or (replay_screen and replay_button.collidepoint(mouse_pos)))
                menu = False
                replay_screen = False
                tween = True
            else if event.type == pygame.MOUSEBUTTONDOWN and how_to_play.collidepoint(mouse_pos) and menu
                menu = False
                tutorial = True
            else if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(mouse_pos) and menu
                running = False
            else if event.type == pygame.MOUSEBUTTONDOWN and ((tutorial and return_button.collidepoint(mouse_pos)) or (replay_screen and menu_return_button.collidepoint(mouse_pos)))
                tutorial = False
                replay_screen = False
                menu = True
            end if 
            if event.type == pygame.KEYDOWN and game and not tween
                if (event.key == pygame.K_d and team == 1) or (event.key == pygame.K_RIGHT and team == 2)
                    if selected_column >= 6
                        if chip_tween == -2
                            pygame.draw.circle(win, game_bg , board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
                            selected_column = 0
                        end if
                    else
                        if chip_tween == -2
                            chip_tween = selected_column
                            selected_column = selected_column + 1
                        end if
                    end if
                else if (event.key == pygame.K_a and team == 1) or (event.key == pygame.K_LEFT and team == 2)
                    if selected_column <= 0
                        if chip_tween == -2
                            pygame.draw.circle(win, game_bg , board[0][selected_column]["coord"].center - pygame.Vector2(0,140), 40)
                            selected_column = 6
                        end if
                    else
                        if chip_tween == -2
                            chip_tween = selected_column
                            selected_column = selected_column - 1
                        end if 
                    end if
                else if (event.key == pygame.K_SPACE and team == 1) or (event.key == pygame.K_RSHIFT and team == 2)
                    game_status = take_turn(board,team,selected_column)
                    clear_pillar_rects = pygame.Rect(0,0,win_width*.2,win_height)
                    if game_status == 1
                        game = False
                        pygame.time.delay(3500)
                        tween = True
                    else if game_status == -1
                        break
                    end if 
                    if team == 1
                        win.blit(clear_bg_left, clear_pillar_rects)
                        team = 2
                    else if team == 2
                        clear_pillar_rects.topright = (win_width, 0)
                        win.blit(clear_bg_right, clear_pillar_rects)
                        team = 1 
                    end if 
                end if 
            end if 
        pygame.display.update()
}
end main program
if __name__ == "__main__"
    run main program
end if 
"""