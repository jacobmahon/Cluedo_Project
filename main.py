from characters import Character #character class that is used for the six main pieces
import pygame #imports the pygame module
import sys #allows system to exit
import os #used to find the pictures
import random #provides randomness the game needs
from button import Button, set_click, clear_click # Button for interaction
from weapon_pieces import Weapon_Pieces # Represents each ordiment token

#the pictures use relative paths, so always run from the folder this file is in (the game crashed if started from anywhere else)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

locker_part_1 = False #lockers for navigating the three rounds of prompts
locker_part_2 = True #from accusing and suggesting
locker_part_3 = True

#for lower_button
die_roll_lock = False #tracks when to activate dice
player_selects_a_die_roll_locker = False #locker for clicking the amount to move
navigation_selector_locker = False #another locker for flow navigation
movement_lock = False #tracks if player moved during current turn
transition_locker = False #helps with managing prompt screens
just_clicked_tunnel_lock = True #tracks tunnel logic

just_entered_room = False #if true, suggestion occurs

player_turn_tracker = 1 #Tracks current player
player_choice = 0 #Moves to move

player_turn = 1 #tracks who's turn it is
 
show_the_card = None #used for suggestion to show a player's card
guess_1 = None #the three guesses, they start empty so they always exist
guess_2 = None
guess_3 = None
ai_next_action_time = 0 #the AI waits using the clock, pygame.time.wait froze the whole window

weapon_pieces_location = { #grid system for where pieces can move
    '189': (770, 150), 
    '190': (770, 450),
    '191': (770, 750),
    '192': (350, 700),
    '193': (70, 780),
    '194': (70, 550),
    '195': (50, 300),
    '196': (50, 100),
    '197': (400, 100)
}
#grid for pieces
dictionary_of_coordinates_to_spots = { #used for navigation portion, after have a translation for each portion in terms of coordinates
    '1': [None, None, '2', None],
    '2': ['1', None, '3', '14'],
    '3': ['2', None, '4', '15'],  
    '4': ['3', None, '5', '16'], 
    '5': ['4', None, '6', '17'],
    '6': ['5', None, '7', '18'],
    '7': ['6', '8', '21', '19'],
    '8': ['189', '9', '22', '7' ],
    '9': [None, '10', '23', '8'],
    '10': [None, '11', '24', '9'],
    '11': [None, '12', '25', '10'],
    '12': [None, '13', '26', '11'], 
    '13': [None, None, '27', '12'],
    '14': [None, '2', '15', None],
    '15': ['14', '3', '16', None],
    '16': ['15', '4', '17', None], 
    '17': ['16', '5', '18', None],
    '18': ['17', '6', '19', None],
    '19': ['18', '7', '20', None],
    '20': ['19', '21', '36', '50'],
    '21': ['7', '22', '35', '20'],
    '22': ['8', '23', '34', '21'],
    '23': ['9', '24', '33', '22'],
    '24': ['10', '25', '32', '23'],
    '25': ['11', '26', '31', '24'],
    '26': ['12', '27', '30', '25'],
    '27': ['13', '28', '29', '26'],
    '28': [None, None, None, '27'],
    '29': ['27', None, None, '30'],
    '30': ['26', '29', None, '31'],
    '31': ['25', '30', None, '32'],
    '32': ['24', '31', None, '33'],
    '33': ['23', '32', None, '34'],
    '34': ['22', '33', '190', '35'],
    '35': ['21', '34', None, '36'],
    '36': ['20', '35', '37', '49'],
    '37': ['36', None, '38', '48'],
    '38': ['37', None, '39', '47'],
    '39': ['38', None, '40', '46'],
    '40': ['39', '190', '41', '45'],
    '41': ['40', None, '42', '44'], #start coordinate check here, above are good
    '42': ['41', None, '167', '43'],
    '43': ['44', '42', '166', None],
    '44': ['45', '41', '43', None],
    '45': ['46', '40', '44', None],
    '46': ['47', '39', '45', None],
    '47': ['48', '38', '46', None],
    '48': ['49', '37', '47', None],
    '49': ['50', '36', '48', None],
    '50': [None, '20', '49', '51'],
    '51': [None, '50', None, '52'],
    '52': ['197', '51', None, '53'],
    '53': ['197', '52', None, '54'],
    '54': [None, '53', None, '55'],
    '55': [None, '54', None, '56'],
    '56': ['57', '55', '86', '84'],
    '57': ['58', None, '56', '83'],
    '58': ['59', None, '57', '81'],
    '59': ['60', '197', '58', '67'],
    '60': ['61', None, '59', '66'],
    '61': ['62', None, '60', '65'],
    '62': [None, None, '61', '64'],
    '63': [None, None, '64', None],
    '64': ['63', '62', '65', None],
    '65': ['64', '61', '66', None],
    '66': ['65', '60', '67', None],
    '67': ['66', '59', '81', '79'],
    '68': [None, '69', None, None],
    '69': ['70', '72', None, '68'],
    '70': [None, '71', '69', None],
    '71': [None, '74', '72', '70'],
    '72': ['71', '73', None, '69'],
    '73': ['74', '76', None, '72'],
    '74': [None, '75', '73', '71'],
    '75': [None, '78', '76', '74'],
    '76': ['75', '77', None, '73'],
    '77': ['78', '80', None, '76'],
    '78': [None, '79', '77', '75'],
    '79': ['196', '67', '80', '78'],
    '80': ['79', '81', '82', '77'],
    '81': ['67', '58', '83', '80'],
    '82': ['80', '83', None, None],
    '83': ['81', '57', '84', '82'],
    '84': ['83', '56', '85', None],
    '85': ['84', '86', '150', '195'],
    '86': ['56', None, '87', '85'],
    '87': ['86', None, '88', '150'],
    '88': ['87', None, '89', '149'],
    '89': ['88', None, '90', '151'],
    '90': ['89', None, '91', '152'],
    '91': ['90', None, '92', '153'],
    '92': ['91', None, '93', '154'],
    '93': ['92', '161', '120', '155'],
    '94': ['95', None, None, None],
    '95': [None, '96', '94', None],
    '96': [None, '97', None, '95'],
    '97': ['98', None, None, '96'],
    '98': ['99', '178', '97', None],
    '99': ['100', '177', '98', None],
    '100': ['101', '176', '99', None],
    '101': ['102', '175', '100', '192'],
    '102': ['103', '174', '101', None],
    '103': ['104', '173', '102', None],
    '104': ['168', '172', '103', '105'],
    '105': ['167', '104', None, '106'],
    '106': ['166', '105', '192', '107'],
    '107': ['165', '106', None, '108'],
    '108': ['164', '107', None, '123'],
    '109': ['110', None, None, None],
    '110': [None, None, '109', '111'], 
    '111': [None, '110', None, '112'],
    '112': ['113', '111', None, None],
    '113': ['114', None, '112', '160'],
    '114': ['115', None, '113', '159'],
    '115': ['116', None, '114', '158'],
    '116': ['117', '192', '115', '157'],
    '117': ['118', None, '116', '130'],
    '118': ['119', None, '117', '136'],
    '119': ['155', '120', '118', '137'],
    '120': ['93', '121', None, '119'],
    '121': ['161', '122', '192', '120'],
    '122': ['162', '123', None, '121'],
    '123': ['163', '108', None, '122'],
    '124': [None, '125', None, None],
    '125': ['131', '126', None, '124'],
    '126': ['132', '127', None, '125'],
    '127': ['133', '128', None, '126'],
    '128': ['134', '129', None, '127'],
    '129': ['135', '130', '156', '128'],
    '130': ['136', '117', '157', '129'],
    '131': [None, '132', '125', None],
    '132': [None, '133', '126', '131'],
    '133': [None, '134', '127', '132'],
    '134': [None, '135', '128', '133'],
    '135': [None, '136', '129', '134'],
    '136': ['137', '118', '130', '135'],
    '137': ['138', '119', '136', None],
    '138': ['139', '155', '137', '194'],
    '139': ['140', '154', '138', None],
    '140': ['141', '153', '139', None],
    '141': ['142', '152', '140', None],
    '142': ['148', '151', '141', '143'],
    '143': [None, '142', None, '144'],
    '144': [None, '143', None, '145'],
    '145': ['195', '144', None, '146'],
    '146': [None, '145', None, '147'],
    '147': [None, '146', '194', None],
    '148': [None, '149', '142', None],
    '149': ['150', '88', '151', '148'],
    '150': ['85', '87', '149', None],
    '151': ['149', '89', '152', '142'],
    '152': ['151', '90', '153', '141'],
    '153': ['152', '91', '154', '140'],
    '154': ['153', '92', '155', '139'],
    '155': ['154', '93', '119', '138'],
    '156': ['129', '157', None, '193'],
    '157': ['130', '116', '158', '156'],
    '158': ['157', '115', '159', None],
    '159': ['158', '114', '160', None],
    '160': ['159', '113', None, None],
    '161': [None, '162', '121', '93'],
    '162': [None, '163', '122', '161'],
    '163': [None, '164', '123', '162'],
    '164': [None, '165', '108', '163'],
    '165': [None, '166', '107', '164'],
    '166': ['43', '167', '106', '165'],
    '167': ['42', '168', '105', '166'],
    '168': [None, '169', '104', '167'],
    '169': [None, '170', '172', '168'],
    '170': [None, None, '171', '169'],
    '171': ['170', '181', '179', '172'],
    '172': ['169', '171', '173', '104'],
    '173': ['172', '179', '174', '103'],
    '174': ['173', None, '175', '102'],
    '175': ['174', None, '176', '101'],
    '176': ['175', None, '177', '100'],
    '177': ['176', None, '178', '99'],
    '178': ['177', None, None, '98'],
    '179': ['171', '180', None, '173'],
    '180': ['181', '183', '191', '179'],
    '181': [None, '182', '180', '171'],
    '182': [None, '185', '183', '181'],
    '183': ['182', '184', None, '180'],
    '184': ['185', '187', None, '183'],
    '185': [None, '186', '184', '182'],
    '186': [None, None, '187', '185'],
    '187': ['186', '188', None, '184'],
    '188': [None, None, None, '187'],
    '189': [None, None, '8', None],
    '190': ['34', None, None, '40'],
    '191': ['180', None, None, None],
    '192': ['121', '106', '101', '116'],
    '193': [None, '156', None, None],
    '194': ['147', '138', None, None],
    '195': [None, '85', '145', None],
    '196': [None, None, '79', None],
    '197': [None, '52', '53', '59']
}

graph_coordinates = { #physical representation for each piece
    '1': (580, 45), #player 1 start
    '2': (580, 77), 
    '3': (580, 109),
    '4': (580, 141),
    '5': (580, 173),
    '6': (580, 205),
    '7': (582, 237), 
    '8': (615, 237),
    '9': (649, 237),
    '10': (682, 237),
    '11': (715, 237),
    '12': (750, 237),
    '13': (783, 45), 
    '14': (548, 77),
    '15': (548, 109),
    '16': (548, 141),
    '17': (548, 173),
    '18': (548, 205),
    '19': (548, 237),
    '20': (548, 269),
    '21': (582, 271), 
    '22': (616, 271),
    '23': (649, 271),
    '24': (682, 271),
    '25': (715, 271),
    '26': (749, 271),
    '27': (783, 271),
    '28': (815, 270), #player 2
    '29': (783, 304),
    '30': (750, 304),
    '31': (715, 304),
    '32': (682, 304),
    '33': (649, 304),
    '34': (615, 304),
    '35': (581, 304),
    '36': (548, 302),
    '37': (548, 335),
    '38': (548, 366),
    '39': (548, 398),
    '40': (548, 430),
    '41': (548, 463),
    '42': (548, 495),
    '43': (515, 495),
    '44': (515, 462),
    '45': (515, 430),
    '46': (515, 398),
    '47': (515, 366),
    '48': (515, 334),
    '49': (515, 302),
    '50': (515, 269),
    '51': (481, 269),
    '52': (447, 269),
    '53': (415, 269),
    '54': (382, 269),
    '55': (349, 269),
    '56': (315, 271),
    '57': (315, 238),
    '58': (315, 206),
    '59': (315, 173),
    '60': (315, 141),
    '61': (315, 109),
    '62': (315, 77),
    '63': (282, 45),
    '64': (282, 77),
    '65': (282, 109),
    '66': (282, 141),
    '67': (282, 173),
    '68': (50, 205), #player 6
    '69': (83, 206),
    '70': (83, 173),
    '71': (116, 173),
    '72': (116, 206),
    '73': (149, 206),
    '74': (149, 173),
    '75': (182, 173),
    '76': (182, 206),
    '77': (215, 206),
    '78': (215, 173),
    '79': (249, 173),
    '80': (249, 206),
    '81': (282, 206),
    '82': (249, 238),
    '83': (282, 238),
    '84': (282, 271),
    '85': (282, 303),
    '86': (315, 303),
    '87': (315, 335),
    '88': (315, 367),
    '89': (315, 398),
    '90': (315, 431),
    '91': (315, 463),
    '92': (315, 495),
    '93': (316, 526),
    '94': (514, 815), #Player 3
    '95': (514, 782),
    '96': (547, 782),
    '97': (582, 782),
    '98': (582, 750),
    '99': (582, 718),
    '100': (582, 686),
    '101': (582, 654),
    '102': (582, 622),
    '103': (582, 590), 
    '104': (582, 558), 
    '105': (549, 558),
    '106': (515, 558),
    '107': (482, 558),
    '108': (449, 558),
    '109': (347, 815), #Player 4
    '110': (347, 783),
    '111': (315, 783),
    '112': (283, 783),
    '113': (283, 751),
    '114': (283, 719),
    '115': (283, 687),
    '116': (283, 655),
    '117': (283, 623),
    '118': (283, 591),
    '119': (282, 558),
    '120': (315, 558),
    '121': (348, 558),
    '122': (381, 558),
    '123': (415, 558),
    '124': (50, 623), #Player 5
    '125': (83, 623),
    '126': (116, 623),
    '127': (149, 623),
    '128': (182, 623),
    '129': (215, 623),
    '130': (249, 623),
    '131': (82, 591),
    '132': (116, 591),
    '133': (149, 591),
    '134': (182, 591),
    '135': (215, 591),
    '136': (249, 591),
    '137': (249, 558),
    '138': (249, 526),
    '139': (249, 494),
    '140': (249, 462),
    '141': (249, 430),
    '142': (249, 399),
    '143': (216, 399),
    '144': (183, 399),
    '145': (149, 399),
    '146': (116, 399),
    '147': (83, 399),
    '148': (249, 366),
    '149': (282, 367),
    '150': (282, 335),
    '151': (282, 399), 
    '152': (282, 430),
    '153': (282, 463),
    '154': (282, 495),
    '155': (282, 526),
    '156': (215, 656),
    '157': (249, 656),
    '158': (249, 688),
    '159': (249, 719),
    '160': (249, 751),
    '161': (349, 525),
    '162': (382, 525),
    '163': (415, 525),
    '164': (448, 525),
    '165': (481, 525),
    '166': (515, 525),
    '167': (548, 525),
    '168': (582, 525),
    '169': (615, 525),
    '170': (648, 525),
    '171': (648, 558),
    '172': (615, 558),
    '173': (615, 590),
    '174': (615, 624),
    '175': (615, 656),
    '176': (615, 688),
    '177': (615, 719),
    '178': (615, 752),
    '179': (648, 590),
    '180': (681, 590),
    '181': (681, 558),
    '182': (715, 558),
    '183': (715, 590),
    '184': (748, 590),
    '185': (748, 558),
    '186': (782, 558),
    '187': (782, 590),
    '188': (815, 590),
    '189': (670, 150), 
    '190': (670, 470),
    '191': (720, 680),
    '192': (420, 750),
    '193': (120, 700),
    '194': (100, 500),
    '195': (100, 300),
    '196': (100, 100),
    '197': (450, 100)
}

pygame.init() #starts pygame


lower_border_light_green = (131, 231, 136) #code for light_green
lower_bound_filter = pygame.Rect(0, 890, 890, 200) #for filling in lower portion interaction menu

#defines all options for cards/solutions
character_that_murdered = ["Miss Scarlet", "Colonel Mustard", "Professor Plump", "Mrs. Peacock", "Mr. Green", "Dr. Orchid"] #6 choices
murder_weapons = ["candlestick", "dagger", "lead pipe", "revolver", "rope", "wrench"] #6 choices
murder_room = ["study", "hall", "lounge", "dining room", "kitchen", "ballroom", "conservatory", "billard room", "library"] #9 choices

program_execution = True #starts program
width_part = 890 #global variables initialized at the start
height_part = 1000 #screen paramenters
frame_rate_per_second = 30 #frame rate

sprite_management_group = pygame.sprite.Group() #keeps track of the token pieces


def did_murder_selection(): #chooses player for solution
    murderer = random.choice(character_that_murdered)
    murderer = character_that_murdered.index(murderer)
    return murderer

def murder_weapon_selection(): #chooses weapon for solution
    murder_weapon = random.choice(murder_weapons)
    murder_weapon = murder_weapons.index(murder_weapon)
    return murder_weapon

def murder_room_selection(): #chooses room for solution
    murder_room_selection = random.choice(murder_room)
    murder_room_selection = murder_room.index(murder_room_selection)
    return murder_room_selection


def die_roll(): #simulates dice
    die_value = random.randint(1,6)
    return die_value

def draw_words(text, x_coordinate, y_coordinate, font_size = 30, text_color = (0, 0, 0), font_style = "Times New Roman"): #displays text for menu
    if text is None: #nothing to show (drawing None crashed the game)
        return
    font = pygame.font.SysFont(font_style, font_size)
    texts = font.render(text, True, text_color) #readies the text
    main_screen.blit(texts, (x_coordinate, y_coordinate)) #displays the text

def round_1_guess_buttons(): #tracks process for accusation and suggestion
    global locker_part_1, locker_part_2 #triggers next process
    character_selected = 0
    if locker_part_1 == False:
        draw_words("Click on who you think is the murderer:", 5, 895)
        if button_1.display_on_screen(): #find way to keep this up until condition is met
            print("0") #what each piece clicked is
            character_selected = 0 #uses value to communicate who was selected
            locker_part_1 = True #allows next part to trigger
            locker_part_2 = False
            return character_selected #returns value

        elif button_2.display_on_screen(): 
            print("1")
            character_selected = 1
            locker_part_1 = True
            locker_part_2 = False
            return character_selected

        elif button_3.display_on_screen(): 
            print("2")
            character_selected = 2
            locker_part_1 = True
            locker_part_2 = False
            return character_selected

        elif button_4.display_on_screen(): 
            print("3")
            character_selected = 3
            locker_part_1 = True
            locker_part_2 = False
            return character_selected

        elif button_5.display_on_screen(): 
            print("4")
            character_selected = 4
            locker_part_1 = True
            locker_part_2 = False
            return character_selected

        elif button_6.display_on_screen(): 
            print("5")
            character_selected = 5
            locker_part_1 = True
            locker_part_2 = False
            return character_selected

def round_2_guess_buttons(): #same stuff as round 1 but for weapons
    global locker_part_2, locker_part_3
    weapon_selected = 0
    if locker_part_2 == False:
        draw_words("Click on the weapon involved:", 5, 895)
        if weapon_1_guess_button.display_on_screen(): 
            print("0")
            weapon_selected = 0
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected

        elif weapon_2_guess_button.display_on_screen(): 
            print("1")
            weapon_selected = 1
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected

        elif weapon_3_guess_button.display_on_screen(): 
            print("2")
            weapon_selected = 2
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected

        elif weapon_4_guess_button.display_on_screen(): 
            print("3")
            weapon_selected = 3
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected

        elif weapon_5_guess_button.display_on_screen(): 
            print("4")
            weapon_selected = 4
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected

        elif weapon_6_guess_button.display_on_screen(): 
            print("5")
            weapon_selected = 5
            locker_part_2 = True
            locker_part_3 = False
            return weapon_selected
        
def round_3_guess_buttons(): #same stuff as round 3 but for rooms and no need to trigger another round after this finishes
    global locker_part_3
    weapon_selected = 0
    if locker_part_3 == False:
        draw_words("Click on the room involved:", 5, 895)
        if room_1_guess_button.display_on_screen(): 
            print("0")
            weapon_selected = 0
            locker_part_3 = True
            return weapon_selected

        elif room_2_guess_button.display_on_screen(): 
            print("1")
            weapon_selected = 1
            locker_part_3 = True
            return weapon_selected

        elif room_3_guess_button.display_on_screen(): 
            print("2")
            weapon_selected = 2
            locker_part_3 = True
            return weapon_selected

        elif room_4_guess_button.display_on_screen(): 
            print("3")
            weapon_selected = 3
            locker_part_3 = True
            return weapon_selected

        elif room_5_guess_button.display_on_screen(): 
            print("4")
            weapon_selected = 4
            locker_part_3 = True
            return weapon_selected

        elif room_6_guess_button.display_on_screen(): 
            print("5")
            weapon_selected = 5
            locker_part_3 = True
            return weapon_selected
        
        elif room_7_guess_button.display_on_screen(): 
            print("6")
            weapon_selected = 6
            locker_part_3 = True
            return weapon_selected
        
        elif room_8_guess_button.display_on_screen(): 
            print("7")
            weapon_selected = 7
            locker_part_3 = True
            return weapon_selected
        
        elif room_9_guess_button.display_on_screen(): 
            print("8")
            weapon_selected = 8
            locker_part_3 = True
            return weapon_selected

def guess_to_win_game(player_object): #for upper button, allows player to make accusation
    global locker_part_1, locker_part_2, locker_part_3 #tracks lockers
    global guess_1, guess_2, guess_3, solution #tracks guess values
    guess_storage = [] #stores guessed values
    if locker_part_1 == False: #first lock triggers
        guess_1 = round_1_guess_buttons()
        return #keep statement in if until this button finishes
    if locker_part_2 == False: #second lock triggers after round 1
        guess_2 = round_2_guess_buttons()
        return
    if locker_part_3 == False: #third lock triggers after second round
        guess_3 = round_3_guess_buttons()
        return 
    guess_storage.append(guess_1) #puts guess to list
    guess_storage.append(guess_2)
    guess_storage.append(guess_3)
    if guess_storage == solution: #checks if solution is met
        draw_words("You won the game! Click the Yes button above to end the game!", 0, 895)
        draw_words("      <-- Click to finish", 20, 850) #text
        if Lower_Click_Yes_Button.display_on_screen(): #button used to trigger the game to be over
            sys.exit() 
    else: #if accusation did not work, continues the game
        player_object.set_player_as_eliminated() #eliminates current player by changing the lock
        draw_words("Your guess is incorrect. You are eliminated.", 100, 895) #text
        return 
    
def cards_assignment(deck, player): #assigns cards to specific player from deck
    c1 = random.choice(deck) #chooses value from deck
    deck.remove(c1) #removes value so it cannot be selected again

    c2 = random.choice(deck)
    deck.remove(c2)

    c3 = random.choice(deck)
    deck.remove(c3)
    
    player.add_cards(c1, c2, c3) #put three cards in specific deck
    return deck #return this deck

def displaying_buttons_roll(number): #takes dice values and prints button for how far player wants to move
    global player_selects_a_die_roll_locker
    choice_value = None
    if player_selects_a_die_roll_locker == False:
        if number >= 1: 
            if click_number_1_button.display_on_screen():
                choice_value = 1
                player_selects_a_die_roll_locker = True
        if number >= 2: 
            if click_number_2_button.display_on_screen():
                choice_value = 2
                player_selects_a_die_roll_locker = True
        if number >= 3: 
            if click_number_3_button.display_on_screen():
                choice_value = 3
                player_selects_a_die_roll_locker = True
        if number >= 4: 
            if click_number_4_button.display_on_screen():
                choice_value = 4
                player_selects_a_die_roll_locker = True
        if number >= 5: 
            if click_number_5_button.display_on_screen():
                choice_value = 5
                player_selects_a_die_roll_locker = True
        if number >= 6: 
            if click_number_6_button.display_on_screen():
                choice_value = 6
                player_selects_a_die_roll_locker = True
        if number >= 7: 
            if click_number_7_button.display_on_screen():
                choice_value = 7
                player_selects_a_die_roll_locker = True
        if number >= 8: 
            if click_number_8_button.display_on_screen():
                choice_value = 8
                player_selects_a_die_roll_locker = True
        if number >= 9: 
            if click_number_9_button.display_on_screen():
                choice_value = 9
                player_selects_a_die_roll_locker = True
        if number >= 10: 
            if click_number_10_button.display_on_screen():
                choice_value = 10
                player_selects_a_die_roll_locker = True
        if number >= 11: 
            if click_number_11_button.display_on_screen():
                choice_value = 11
                player_selects_a_die_roll_locker = True
        if number >= 12: 
            if click_number_12_button.display_on_screen():
                choice_value = 12
                player_selects_a_die_roll_locker = True
    if player_selects_a_die_roll_locker == True: 
        return choice_value
        

def start_suggestion(): #a room was entered, so the suggestion starts again from round 1
    global just_entered_room, locker_part_1, locker_part_2, locker_part_3
    global guess_1, guess_2, guess_3, show_the_card
    just_entered_room = True
    locker_part_1 = False #old accusation/suggestion values must not leak into this one
    locker_part_2 = True
    locker_part_3 = True
    guess_1 = None
    guess_2 = None
    guess_3 = None
    show_the_card = None

def go_to_next_player(): #the one place a turn ends, it moves on and clears every lock from the old turn
    global player_turn_tracker, player_choice, die_roll_lock, player_selects_a_die_roll_locker
    global navigation_selector_locker, movement_lock, transition_locker, just_entered_room
    for each_try in range(6): #skips players that are eliminated
        if player_turn_tracker < 6: #1-5 just add 1
            player_turn_tracker += 1
        else: #if on 6, go back to 1
            player_turn_tracker = 1
        if all_players[player_turn_tracker - 1].return_player_elimination_status() == False:
            break
    die_roll_lock = False #resets lockers
    player_selects_a_die_roll_locker = False
    navigation_selector_locker = False
    movement_lock = False
    transition_locker = False
    just_entered_room = False
    player_choice = 0

def navigation_selector(player_object): #tracks movement after amount of moves to move are selected
    global player_choice, navigation_selector_locker, movement_lock, transition_locker, just_entered_room #Coordination for other parts of the program
    entered_room = False #tracks 
    if navigation_selector_locker == False: #show all movement options if lock activates
        if click_navigaton_up_button.display_on_screen(): #for up movement
            confirmed_valid = False 
            entered_room = False #lockers for tracking movement action
            unpack_values = player_object.player_movement(1) #gets values to check if movement is legal and/or player entered a room
            if unpack_values != None: #take variables from method and stores them
                confirmed_valid = unpack_values[0]
                entered_room = unpack_values[1]
            if confirmed_valid == True: #if player moved legally
                player_choice = player_choice - 1 #remove a number
                if entered_room == True: #if room is entered
                    start_suggestion()
                    player_choice = 0 #make counter to 0 for next player

        elif click_navigaton_right_button.display_on_screen():
            confirmed_valid = False #for true navigation
            entered_room = False
            unpack_values = player_object.player_movement(2)
            if unpack_values != None: #first lock for navigation, second lock for checking rooms
                confirmed_valid = unpack_values[0]
                entered_room = unpack_values[1]
            if confirmed_valid == True:
                player_choice = player_choice - 1
                if entered_room == True:
                    start_suggestion()
                    player_choice = 0

        elif click_navigaton_down_button.display_on_screen():
            confirmed_valid = False #for true navigation
            entered_room = False
            unpack_values = player_object.player_movement(3)
            if unpack_values != None: #first lock for navigation, second lock for checking rooms
                confirmed_valid = unpack_values[0]
                entered_room = unpack_values[1]
            if confirmed_valid == True:
                player_choice = player_choice - 1
                if entered_room == True:
                    start_suggestion()
                    player_choice = 0

        elif click_navigaton_left_button.display_on_screen(): #+button for player to click guess if they are in a room once grid is built + stop once in room
            confirmed_valid = False #for true navigation
            entered_room = False
            unpack_values = player_object.player_movement(4)
            if unpack_values != None: #first lock for navigation, second lock for checking rooms
                confirmed_valid = unpack_values[0]
                entered_room = unpack_values[1]
            if confirmed_valid == True:
                player_choice = player_choice - 1
                if entered_room == True:
                    start_suggestion()
                    player_choice = 0


        elif click_navigaton_stop_button.display_on_screen(): #option for player to not move
            player_choice = 0

        if player_choice == 0: #When player's turn ends 
            movement_lock = False #resets locks
            transition_locker = False
        
    if player_choice == 0: #adjusts locks accordingly if movement is not triggered
        navigation_selector_locker = True

def suggestion(player_object): #suggestion mechanism
    global locker_part_1, locker_part_2, locker_part_3
    global guess_1, guess_2, guess_3, show_the_card #globals for communcation access
    global cards_p1, cards_p2, cards_p3, cards_p4, cards_p5, cards_p6
    global Miss_Scarlet, Colonel_Mustard, Professor_Plump, Mrs_Peacock, Mr_Green, Dr_Orchid
    global candlestick_piece, dagger_piece, lead_pipe_piece, revolver_piece, rope_piece, wrench_piece
    guess_storage = [] #stores values
    if locker_part_1 == False: #triggers first part
        guess_1 = round_1_guess_buttons() #get round 1 guess items
        if guess_1 == 0: #conditions to check which player to take random card from
            show_the_card = random.choice(cards_p1)
        elif guess_1 == 1:
            show_the_card = random.choice(cards_p2)
        elif guess_1 == 2:
            show_the_card = random.choice(cards_p3)
        elif guess_1 == 3:
            show_the_card = random.choice(cards_p4)
        elif guess_1 == 4:
            show_the_card = random.choice(cards_p5)
        elif guess_1 == 5:
            show_the_card = random.choice(cards_p6)
        return #keeps folow in this area until items have finished
    if locker_part_2 == False: #Triggers second round
        guess_2 = round_2_guess_buttons()
        return
    if locker_part_3 == False: #triggers third round
        guess_3 = round_3_guess_buttons()
        return
    
    guess_storage.append(guess_1) #take the three guesses and put it in a list
    guess_storage.append(guess_2)
    guess_storage.append(guess_3)

    place_to_go = player_object.return_current_position()#gets suggesting player clordinates

    #triggers logic for the player's card they see below
    if guess_1 == 0: #Miss_Scarlet  
        draw_words("The below card is in Miss. Scarlet's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20) #used for card showing
        Miss_Scarlet.set_current_node(place_to_go) #moves figure to current location
    elif guess_1 == 1: #Colonel_Mustard
        draw_words("The below card is in Colonel Mustard's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20)
        Colonel_Mustard.set_current_node(place_to_go)
    elif guess_1 == 2: #Professor Plump
        draw_words("The below card is in Professor Plump's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20)
        Professor_Plump.set_current_node(place_to_go)
    elif guess_1 == 3: #Mrs. Peacock
        draw_words("The below card is in Mrs. Peacock's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20)
        Mrs_Peacock.set_current_node(place_to_go)
    elif guess_1 == 4: #Mr. Green
        draw_words("The below card is in Mr. Green's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20)
        Mr_Green.set_current_node(place_to_go)
    elif guess_1 == 5: #Dr. Orchid
        draw_words("The below card is in Dr. Orchid's deck:", 5, 950, 20)
        draw_words(show_the_card, 5, 970, 20)
        Dr_Orchid.set_current_node(place_to_go) 

    #triggers logic for the weapon's token movement they see
    if guess_2 == 0: #candlestick 
        candlestick_piece.set_current_node(place_to_go) #moves specific piece
    elif guess_2 == 1: #dagger
        dagger_piece.set_current_node(place_to_go)
    elif guess_2 == 2: #lead pipe
        lead_pipe_piece.set_current_node(place_to_go)
    elif guess_2 == 3: #revolver
        revolver_piece.set_current_node(place_to_go)
    elif guess_2 == 4: #rope
        rope_piece.set_current_node(place_to_go)
    elif guess_2 == 5: #wrench
        wrench_piece.set_current_node(place_to_go)
    
def player_movement(player_object): #main executable for all other methods
    global die_roll_lock, player_selects_a_die_roll_locker, navigation_selector_locker, just_clicked_tunnel_lock, locker_part_1
    global total_die_roll, player_choice, player_turn_tracker, movement_lock, transition_locker, just_entered_room
    global ai_next_action_time
    coordinate_checker = player_object.return_current_position() #have coordinate checker
    is_AI = player_object.return_AI_Controlled()
    is_eliminated = player_object.return_player_elimination_status()
    
    if is_eliminated == False: #if the player is not eliminated continue
        if is_AI == False: #if the player is not AI, then run
            if just_entered_room == True: #executes suggestion
                suggestion(player_object) #the player that entered the room makes the suggestion
                if locker_part_1 == True and locker_part_2 == True and locker_part_3 == True: #the finish button only shows once the guess is done
                    draw_words("      <-- Click to finish", 20, 850) #text
                    if Lower_Click_Yes_Button.display_on_screen(): #button so that once everything executes, this follows logically
                        just_entered_room = False
                        go_to_next_player() #suggestion is over, so the turn is over
                return #nothing else happens while the suggestion is on screen




            if coordinate_checker in ('189', '193', '191', '196') and transition_locker == False: #triggers escape room
                draw_words("Would you like to utilize the escape tunnel?:", 5, 895)
                if Click_Yes_Button.display_on_screen():
                    transition_locker = True
                    start_suggestion()
                    if coordinate_checker == '189':
                        player_object.set_current_node('193')
                    elif coordinate_checker == '191':
                        player_object.set_current_node('196')
                    elif coordinate_checker == '193':
                        player_object.set_current_node('189')
                    elif coordinate_checker == '196':
                        player_object.set_current_node('191')
                elif Click_No_Button.display_on_screen():
                    transition_locker = True
                return
        
            if die_roll_lock == False and (coordinate_checker not in ('189', '193', '191', '196') or transition_locker == True) and just_entered_room == False: #rolling dice conditions
                first_die = die_roll()
                second_die = die_roll() #dice process
                total_die_roll = first_die + second_die
                die_roll_lock = True #stops rolling dice/hides dice text

            if player_selects_a_die_roll_locker == False and (coordinate_checker not in ('189', '193', '191', '196') or transition_locker == True) and just_entered_room == False: #condition for choosing move amount
                draw_words(f"Player {player_turn_tracker}'s turn:", 5, 895) #text
                draw_words(f"You rolled a {total_die_roll}. How far do you want to move?", 5, 930) #text
                choice = displaying_buttons_roll(total_die_roll) #displays buttons to click only one
                if choice != None: #choice could be made
                    player_choice = choice
        
            elif player_choice > 0 and (coordinate_checker not in ('189', '193', '191', '196') or transition_locker == True): #navigation menu
                draw_words(f"You have {player_choice} moves left", 5, 895)
                draw_words("Click direction to move", 5, 930)
                navigation_selector(player_object)


            if player_choice <= 0 and player_selects_a_die_roll_locker and (coordinate_checker not in ('189', '193', '191', '196') or transition_locker == True) and just_entered_room == False:
                go_to_next_player()
        
        else: #if the player is AI
            draw_words(f"Player {player_turn_tracker} is the AI player playing currently playing.", 5, 895)
            did_ai_solve_the_puzzle = player_object.return_did_ai_solve_solution() #checks if this AI solved the solution
            if pygame.time.get_ticks() < ai_next_action_time: #waits between AI steps without freezing the window
                return
            ai_next_action_time = pygame.time.get_ticks() + 500
            current_turn_value = player_object.return_current_number_of_turns()
            if current_turn_value > 0:
                player_object.AI_player_movement() #moves piece, need way for dice to be saved
                entered_room_checker = player_object.return_current_position() #checks current player's location as it entered a room coordinate's locations
                if entered_room_checker in ('189', '190', '191', '192', '193', '194', '195', '196', '197'): #checks if the player entered a room, does movement calculations after card could be inserted
                    AI_player_location = player_object.return_current_position() #gets the guessing player's coordinates

                    deck_1_actual = player_object.return_p1_card_deck() #used to compare updated to prior
                    deck_2_actual = player_object.return_p2_card_deck() 
                    deck_3_actual = player_object.return_p3_card_deck() 
                    deck_4_actual = player_object.return_p4_card_deck() 
                    deck_5_actual = player_object.return_p5_card_deck() 

                    if (len(deck_1_actual) < 3) or (len(deck_1_actual) == 3) and (len(deck_2_actual) == 0): #if deck is less than three or it is 3 and next deck has nothing
                        Miss_Scarlet.set_current_node(AI_player_location) #changes the player's location in alignment AI player
                    elif (len(deck_2_actual) < 3) or (len(deck_2_actual) == 3) and (len(deck_3_actual) == 0): #if deck is less than three or it is 3 and next deck has nothing
                        Colonel_Mustard.set_current_node(AI_player_location) #changes the player's location in alignment AI player
                    elif (len(deck_3_actual) < 3) or (len(deck_3_actual) == 3) and (len(deck_4_actual) == 0): #if deck is less than three or it is 3 and next deck has nothing
                        Professor_Plump.set_current_node(AI_player_location) #changes the player's location in alignment AI player
                    elif (len(deck_4_actual) < 3) or (len(deck_4_actual) == 3) and (len(deck_5_actual) == 0): #if deck is less than three or it is 3 and next deck has nothing
                        Mrs_Peacock.set_current_node(AI_player_location) #changes the player's location in alignment AI player
                    else: #since there is no card deck after 5, easiest way to describe this condition as if the top does not occur, it assumes the last deck is what was added
                        Mr_Green.set_current_node(AI_player_location) #moves this player
                    
                    random_weapon_value = random.randint(1, 6) #chooses a random weapon from 1 to 6, mainly for weapon visuals
                    if random_weapon_value == 1: #selected weapon is then teleported
                        candlestick_piece.set_current_node(AI_player_location) #Takes current dictionary key and passes it for the weapon piece to move it to the current location
                    elif random_weapon_value == 2:
                        dagger_piece.set_current_node(AI_player_location)
                    elif random_weapon_value == 3:
                        lead_pipe_piece.set_current_node(AI_player_location)
                    elif random_weapon_value == 4:
                        revolver_piece.set_current_node(AI_player_location)
                    elif random_weapon_value == 5:
                        rope_piece.set_current_node(AI_player_location)
                    elif random_weapon_value == 6:
                        wrench_piece.set_current_node(AI_player_location)



                #second part will be AI weapons
                    
            else: #executes at the end of the turn
                if did_ai_solve_the_puzzle == True: #shows text
                    name_1 = character_that_murdered[solution[0]] #in solution 0, retrieve the name
                    name_2 = murder_weapons[solution[1]] #in solution 1, retrieve the weapon
                    name_3 = murder_room[solution[2]] #in solution 2, retrieve the room
                    print(f"The AI solved the game! The solution is {name_1, name_2, name_3}.") #prints the solution
                    sys.exit() #yes button lock used to show text and end the game
                
                player_object.set_lock_back_to_true_for_dice_roll() #set back to False
                player_object.set_movement_lock_to_a_value() #restores the value for next turn
                go_to_next_player()
    else: #if player is eliminated
        go_to_next_player() #skips them

def game_advancement(): #logic for controlling the whole game
    global player_turn_tracker
    global c1_p1, c2_p1, c3_p1, c1_p2, c2_p2, c3_p2, c1_p3, c2_p3, c3_p3 #coordination
    global c1_p4, c2_p4, c3_p4, c1_p5, c2_p5, c3_p5, c1_p6, c2_p6, c3_p6

    draw_words("Cards:", 390, 970, 25)

    if player_turn_tracker == 1: #player 1 trigger their turn and cards
        player_movement(Miss_Scarlet)
        draw_words(c1_p1, 460, 970, 25) #specific player cards
        draw_words(c2_p1, 650, 970, 25 )
        draw_words(c3_p1, 650, 940, 25)

    elif player_turn_tracker == 2: #player 2 trigger their turn and cards
        player_movement(Colonel_Mustard)
        draw_words(c1_p2, 460, 970, 25)
        draw_words(c2_p2, 650, 970, 25 )
        draw_words(c3_p2, 650, 940, 25)

    elif player_turn_tracker == 3: #player 3 trigger their turn and cards
        player_movement(Professor_Plump)
        draw_words(c1_p3, 460, 970, 25)
        draw_words(c2_p3, 650, 970, 25)
        draw_words(c3_p3, 650, 940, 25)

    elif player_turn_tracker == 4: #player 4 trigger their turn and cards
        player_movement(Mrs_Peacock)
        draw_words(c1_p4, 460, 970, 25)
        draw_words(c2_p4, 650, 970, 25)
        draw_words(c3_p4, 650, 940, 25)
    
    elif player_turn_tracker == 5: #player 5 trigger their turn and cards
        player_movement(Mr_Green)
        draw_words(c1_p5, 460, 970, 25)
        draw_words(c2_p5, 650, 970, 25)
        draw_words(c3_p5, 650, 940, 25)
    
    elif player_turn_tracker == 6: #player 6 trigger their turn and cards
        player_movement(Dr_Orchid)
        draw_words(c1_p6, 460, 970, 25)
        draw_words(c2_p6, 650, 970, 25)
        draw_words(c3_p6, 650, 940, 25)
    
#---------- screen scaling ----------
#The game is always drawn on main_screen (890 x 1000), then scaled to fit the window each frame.
#Mouse clicks are converted back to game coordinates so they still hit the right button.
view_scale = 1.0
view_offset_x = 0
view_offset_y = 0

def update_view_size(): #works out how big the game is drawn inside the current window
    global view_scale, view_offset_x, view_offset_y
    window_width, window_height = pygame.display.get_surface().get_size()
    if window_width < 1 or window_height < 1: #window is minimized
        return
    view_scale = min(window_width / width_part, window_height / height_part) #keeps the same shape
    view_offset_x = (window_width - int(width_part * view_scale)) // 2 #black bars if the window has a different shape
    view_offset_y = (window_height - int(height_part * view_scale)) // 2

def window_to_game(window_position): #turns a click on the window into a click on the game picture
    game_x = (window_position[0] - view_offset_x) / view_scale
    game_y = (window_position[1] - view_offset_y) / view_scale
    if 0 <= game_x < width_part and 0 <= game_y < height_part:
        return (int(game_x), int(game_y))
    return None #click was on the black bars

def show_frame(): #scales the game picture onto the window
    window = pygame.display.get_surface()
    window.fill((0, 0, 0))
    scaled_size = (max(1, int(width_part * view_scale)), max(1, int(height_part * view_scale)))
    if scaled_size == (width_part, height_part):
        window.blit(main_screen, (view_offset_x, view_offset_y))
    else:
        window.blit(pygame.transform.smoothscale(main_screen, scaled_size), (view_offset_x, view_offset_y))
    pygame.display.update()

#start with a window that fits the desktop, it can be resized after that
desktop_info = pygame.display.Info()
start_scale = 1.0
if desktop_info.current_w > 0 and desktop_info.current_h > 0:
    start_scale = min(1.0, (desktop_info.current_w - 100) / width_part, (desktop_info.current_h - 120) / height_part)
pygame.display.set_mode((int(width_part * start_scale), int(height_part * start_scale)), pygame.RESIZABLE) #initialized window dimensions
main_screen = pygame.Surface((width_part, height_part)) #the game is drawn here at full size
view_scale = start_scale

pygame.display.set_caption("Cluedo") #tab name
fps_controller_and_clock = pygame.time.Clock() #controls frames

game_board = pygame.image.load("Picture_storage/final_board_display.jpg") #loads board image

the_murderer = did_murder_selection() #get each solution instance
the_weapon = murder_weapon_selection()
the_room = murder_room_selection()

new_character_that_murdered = character_that_murdered.copy() #copy items to new list
new_murder_weapons = murder_weapons.copy() #so changes do not affect initial
new_murder_room = murder_room.copy()

murder_name = new_character_that_murdered[the_murderer]
murder_weapon_name = new_murder_weapons[the_weapon] #saving the variables
murder_room_name = new_murder_room[the_room]

new_character_that_murdered.remove(murder_name)
new_murder_weapons.remove(murder_weapon_name) #removing the solution from the deck
new_murder_room.remove(murder_room_name)

official_card_deck = [] #deck for distributing to players
for person_card in new_character_that_murdered:
    official_card_deck.append(person_card) #take remaining decks without solition and add them to the deck
for a_weapon in new_murder_weapons:
    official_card_deck.append(a_weapon)
for a_room in new_murder_room:
    official_card_deck.append(a_room)

solution = [the_murderer, the_weapon, the_room] #initializes the solution set

#initializes all characters
Miss_Scarlet = Character("Picture_storage/player_1.png", dictionary_of_coordinates_to_spots, graph_coordinates, "1", 1)
Colonel_Mustard = Character("Picture_storage/player_2.png", dictionary_of_coordinates_to_spots, graph_coordinates, "28", 2)
Professor_Plump = Character("Picture_storage/player_3.png", dictionary_of_coordinates_to_spots, graph_coordinates, "94", 3)
Mrs_Peacock = Character("Picture_storage/player_4.png", dictionary_of_coordinates_to_spots, graph_coordinates, "109", 4)
Mr_Green = Character("Picture_storage/player_5.png", dictionary_of_coordinates_to_spots, graph_coordinates, "124", 5)
Dr_Orchid = Character("Picture_storage/player_6.png", dictionary_of_coordinates_to_spots, graph_coordinates, "68", 6, True) #marks this player as the AI controlled one

all_players = [Miss_Scarlet, Colonel_Mustard, Professor_Plump, Mrs_Peacock, Mr_Green, Dr_Orchid] #in player order

#weapon piece locations set up
coordinate_locations_for_weapon_pieces = ['189', '190', '191', '192', '193', '194', '195', '196', '197']

#assigns each weapon to a random place
location_1 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_1) #removes the weapon so it cannot be selected again

location_2 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_2)

location_3 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_3)

location_4 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_4)

location_5 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_5)

location_6 = random.choice(coordinate_locations_for_weapon_pieces)
coordinate_locations_for_weapon_pieces.remove(location_6)

#initializes weapon pieces
candlestick_piece = Weapon_Pieces("Picture_storage/5_candlestick.png", weapon_pieces_location, location_1)
dagger_piece = Weapon_Pieces("Picture_storage/5_dagger.png", weapon_pieces_location, location_2)
lead_pipe_piece = Weapon_Pieces("Picture_storage/5_lead_pipe.png", weapon_pieces_location, location_3)
revolver_piece = Weapon_Pieces("Picture_storage/5_revolver.png", weapon_pieces_location, location_4)
rope_piece = Weapon_Pieces("Picture_storage/5_rope.png", weapon_pieces_location, location_5)
wrench_piece = Weapon_Pieces("Picture_storage/5_wrench.png", weapon_pieces_location, location_6)

#adds sprites to group so pygame can work with them
sprite_management_group.add(Miss_Scarlet, Colonel_Mustard, Professor_Plump, Mrs_Peacock, Mr_Green, Dr_Orchid)
sprite_management_group.add(candlestick_piece, dagger_piece, lead_pipe_piece, revolver_piece, rope_piece, wrench_piece)

#distributes 3 cards to each deck based on offical deck and removes selected cards so no duplicates
modified_deck = cards_assignment(official_card_deck, Miss_Scarlet) #player 1
modified_deck = cards_assignment(modified_deck, Colonel_Mustard) #player 2
modified_deck = cards_assignment(modified_deck, Professor_Plump) #player 3
modified_deck = cards_assignment(modified_deck, Mrs_Peacock) #player 4
modified_deck = cards_assignment(modified_deck, Mr_Green) #player 5
modified_deck = cards_assignment(modified_deck, Dr_Orchid) #player 6

cards_p1 = Miss_Scarlet.return_cards() #Initializes specific card values for displaying in the game
c1_p1 = cards_p1[0]
c2_p1 = cards_p1[1]
c3_p1 = cards_p1[2]

cards_p2 = Colonel_Mustard.return_cards()
c1_p2 = cards_p2[0]
c2_p2 = cards_p2[1]
c3_p2 = cards_p2[2]

cards_p3 = Professor_Plump.return_cards()
c1_p3 = cards_p3[0]
c2_p3 = cards_p3[1]
c3_p3 = cards_p3[2]

cards_p4 = Mrs_Peacock.return_cards()
c1_p4 = cards_p4[0]
c2_p4 = cards_p4[1]
c3_p4 = cards_p4[2]

cards_p5 = Mr_Green.return_cards()
c1_p5 = cards_p5[0]
c2_p5 = cards_p5[1]
c3_p5 = cards_p5[2]

cards_p6 = Dr_Orchid.return_cards()
c1_p6 = cards_p6[0]
c2_p6 = cards_p6[1]
c3_p6 = cards_p6[2]

#below gives cards to the AI to make computations
Dr_Orchid.get_all_player_cards(cards_p1, cards_p2, cards_p3, cards_p4, cards_p5)




#Saves image on location
button_guess = pygame.image.load("Picture_storage/guess_button.png")
button_advance = pygame.image.load("Picture_storage/advance_button.png") #main buttons

character_1_guess = pygame.image.load("Picture_storage/1_Miss_Scarlet.png")
character_2_guess = pygame.image.load("Picture_storage/1_Colonel_Mustard.png")
character_3_guess = pygame.image.load("Picture_storage/1_Professor_Plump.png")
character_4_guess = pygame.image.load("Picture_storage/1_Mrs_Peacock.png")
character_5_guess = pygame.image.load("Picture_storage/1_Mr_Green.png")
character_6_guess = pygame.image.load("Picture_storage/1_Dr_Orchid.png")

#creates button and gives its dimensions
button_1 = Button(500, 895, character_1_guess, main_screen)
button_2 = Button(675, 895, character_2_guess, main_screen)
button_3 = Button(4, 930, character_3_guess, main_screen)
button_4 = Button(225, 930, character_4_guess, main_screen)
button_5 = Button(410, 930, character_5_guess, main_screen)
button_6 = Button(575, 930, character_6_guess, main_screen)

#saves image on location
weapon_1_guess = pygame.image.load("Picture_storage/2_candlestick.png")
weapon_2_guess = pygame.image.load("Picture_storage/2_dagger.png")
weapon_3_guess = pygame.image.load("Picture_storage/2_lead_pipe.png")
weapon_4_guess = pygame.image.load("Picture_storage/2_revolver.png")
weapon_5_guess = pygame.image.load("Picture_storage/2_rope.png")
weapon_6_guess = pygame.image.load("Picture_storage/2_wrench.png")

#creates button and gives its dimensions
weapon_1_guess_button = Button(500, 895, weapon_1_guess, main_screen)
weapon_2_guess_button = Button(675, 895, weapon_2_guess, main_screen)
weapon_3_guess_button = Button(4, 930, weapon_3_guess, main_screen)
weapon_4_guess_button = Button(225, 930, weapon_4_guess, main_screen)
weapon_5_guess_button = Button(410, 930, weapon_5_guess, main_screen)
weapon_6_guess_button = Button(575, 930, weapon_6_guess, main_screen)

#saves image on location
room_1_guess = pygame.image.load("Picture_storage/3_study.png")
room_2_guess = pygame.image.load("Picture_storage/3_hall.png")
room_3_guess = pygame.image.load("Picture_storage/3_lounge.png")
room_4_guess = pygame.image.load("Picture_storage/3_dining_room.png")
room_5_guess = pygame.image.load("Picture_storage/3_kitchen.png")
room_6_guess =pygame.image.load("Picture_storage/3_ballroom.png")
room_7_guess = pygame.image.load("Picture_storage/3_conservatory.png")
room_8_guess = pygame.image.load("Picture_storage/3_billard_room.png")
room_9_guess = pygame.image.load("Picture_storage/3_library.png")

#creates button and gives its dimensions
room_1_guess_button = Button(500, 895, room_1_guess, main_screen)
room_2_guess_button = Button(625, 895, room_2_guess, main_screen)
room_3_guess_button = Button(725, 895, room_3_guess, main_screen)
room_4_guess_button = Button(4, 930, room_4_guess, main_screen)
room_5_guess_button = Button(200, 930, room_5_guess, main_screen)
room_6_guess_button = Button(350, 930, room_6_guess, main_screen)
room_7_guess_button = Button(525, 930, room_7_guess, main_screen) #when time comes, adjust last 3 coordinates
room_8_guess_button = Button(4, 965, room_8_guess, main_screen)
room_9_guess_button = Button(200, 965, room_9_guess, main_screen)

#saves image on location
click_number_1 = pygame.image.load("Picture_storage/number_1.png")
click_number_2 = pygame.image.load("Picture_storage/number_2.png")
click_number_3 = pygame.image.load("Picture_storage/number_3.png")
click_number_4 = pygame.image.load("Picture_storage/number_4.png")
click_number_5 = pygame.image.load("Picture_storage/number_5.png")
click_number_6 = pygame.image.load("Picture_storage/number_6.png")
click_number_7 = pygame.image.load("Picture_storage/number_7.png")
click_number_8 = pygame.image.load("Picture_storage/number_8.png")
click_number_9 = pygame.image.load("Picture_storage/number_9.png")
click_number_10 = pygame.image.load("Picture_storage/number_10.png")
click_number_11 = pygame.image.load("Picture_storage/number_11.png")
click_number_12 = pygame.image.load("Picture_storage/number_12.png")

#creates button and gives its dimensions
click_number_1_button = Button(0, 960, click_number_1, main_screen) 
click_number_2_button = Button(30, 960, click_number_2, main_screen)
click_number_3_button = Button(60, 960, click_number_3, main_screen)
click_number_4_button = Button(90, 960, click_number_4, main_screen)
click_number_5_button = Button(120, 960, click_number_5, main_screen)
click_number_6_button = Button(150, 960, click_number_6, main_screen)
click_number_7_button = Button(180, 960, click_number_7, main_screen)
click_number_8_button = Button(210, 960, click_number_8, main_screen)
click_number_9_button = Button(240, 960, click_number_9, main_screen)
click_number_10_button = Button(270, 960, click_number_10, main_screen)
click_number_11_button = Button(310, 960, click_number_11, main_screen)
click_number_12_button = Button(350, 960, click_number_12, main_screen)

#Yes and No Button image saved
Click_Yes = pygame.image.load("Picture_storage/4_Yes.png")
Click_No = pygame.image.load("Picture_storage/4_No.png")

#creates button and gives its dimensions
Click_Yes_Button = Button(400, 930, Click_Yes, main_screen)
Lower_Click_Yes_Button = Button(5, 850, Click_Yes, main_screen) 
Click_No_Button = Button(500, 930, Click_No, main_screen) 

#saves image on location
click_navigaton_left = pygame.image.load("Picture_storage/movement_left_navigation.png")
click_navigaton_right = pygame.image.load("Picture_storage/movement_right_navigation.png")
click_navigaton_up = pygame.image.load("Picture_storage/movement_up_navigation.png")
click_navigaton_down = pygame.image.load("Picture_storage/movement_down_navigation.png")
click_navigaton_stop = pygame.image.load("Picture_storage/movement_stop_navigation.png")

#creates button and gives its dimensions
click_navigaton_left_button = Button(350, 895, click_navigaton_left, main_screen) #fix coordinates later
click_navigaton_right_button = Button(650, 895, click_navigaton_right, main_screen)
click_navigaton_up_button = Button(500, 895, click_navigaton_up, main_screen)
click_navigaton_down_button = Button(485, 935, click_navigaton_down, main_screen)
click_navigaton_stop_button = Button(800, 895, click_navigaton_stop, main_screen)

#creates button and gives its dimensions
navigation = Button(500, 895, click_number_1, main_screen)
the_button_guess = Button(450, -1, button_guess, main_screen)
the_button_advance = Button(411, 847, button_advance, main_screen)

the_button_advance.display_on_screen() #displays button on screen


guess_button_activate = False #lockers for managing which starting buttons show up or not
advancement_turn = False

while program_execution: #runs main program
    update_view_size() #the window may have been resized
    main_screen.blit(game_board, (0, 0)) #displays the board
    pygame.draw.rect(main_screen, lower_border_light_green, lower_bound_filter) #displays lower menu for interaction

    for game_event in pygame.event.get(): #gets event and loops through all of them
        if game_event.type == pygame.QUIT: #Used to end game when x button is clicked in upper right
            pygame.quit()
            sys.exit()
        elif game_event.type == pygame.MOUSEBUTTONDOWN and game_event.button == 1: #left click
            click_spot = window_to_game(game_event.pos) #converts to game coordinates
            if click_spot is not None:
                set_click(click_spot) #the buttons check this click

    sprite_management_group.draw(main_screen) #manages the sprites/checks on them

    accuser = all_players[player_turn_tracker - 1] #the player whose turn it is
    #only a human that is not eliminated and not in the middle of a suggestion can accuse
    if the_button_guess.display_on_screen() and accuser.return_AI_Controlled() == False and accuser.return_player_elimination_status() == False and just_entered_room == False: #displays accusation button
        guess_button_activate = True
        advancement_turn = False #triggers locks to start events and hide necessay text

        locker_part_1 = False #when navigation is complete, add condition to only click the button when the player is in the room
        locker_part_2 = True
        locker_part_3 = True

    if guess_button_activate: #triggers accusation
        if player_turn_tracker == 1: #tracking which player is making the guess to win the game
            guess_to_win_game(Miss_Scarlet)
        elif player_turn_tracker == 2:
            guess_to_win_game(Colonel_Mustard)
        elif player_turn_tracker == 3:
            guess_to_win_game(Professor_Plump)
        elif player_turn_tracker == 4:
            guess_to_win_game(Mrs_Peacock)
        elif player_turn_tracker == 5:
            guess_to_win_game(Mr_Green)
        elif player_turn_tracker == 6:
            guess_to_win_game(Dr_Orchid)

    if the_button_advance.display_on_screen():
        guess_button_activate = False #when another button is clicked, text from the other is hidden
        advancement_turn = True #activates code

    if advancement_turn: #if triggered true
        game_advancement() #advances the game

    clear_click() #a click only lasts for one frame
    show_frame() #scales the game to the window and updates it
    fps_controller_and_clock.tick(frame_rate_per_second) #controls framerate
    

