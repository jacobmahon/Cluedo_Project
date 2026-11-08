import random
import pygame
from collections import deque #for BFS algorithm

class Character(pygame.sprite.Sprite):
    def __init__(self, photo_location, logical_representation, physical_representation, starting_dictionary_index, player_number, AI_enabled = False): 
        super().__init__()
        photo_value = pygame.image.load(photo_location).convert_alpha()  #photo loads
        self.image = pygame.transform.smoothscale(photo_value, (30, 30)) #formats image

        #defines the representations that the pieces will use
        self.logical_representation = logical_representation #use for tracking move
        self.physical_representation = physical_representation #use for tracking visuals
        self.current_node = starting_dictionary_index #used for changing visual representation
        self.physical_display_coordinates = self.physical_representation[starting_dictionary_index] #used for updating moves
        self.rect = self.image.get_rect(topleft=self.physical_display_coordinates) #draws piece
        self.in_escape_room = False #tracks escape stuff
        self.player_number = player_number #used for check
        self.AI_enabled = AI_enabled
        self.AI_Dice_Lock = False #lock to make sure the dice rolls one set
        self.movement_turns = 12 #part of locking condition to play, must be greater than 0 for AI to enter
        self.player_is_eliminated_lock = False
        self.card_checker_duplicate_lock = False #if there is no duplicate tracker
        self.past_value = 5 #keeps track of the prior move so the player does not attempt the prior move
        self.turn_start_node = starting_dictionary_index #the tile the AI started its turn on

        self.game_tracking_values_people = [] #need 5 for solution
        self.game_tracking_values_weapons = [] #need 5 for solution
        self.game_tracking_values_rooms = [] #need 8 for solution
        self.player_1_deck = []
        self.player_2_deck = []
        self.player_3_deck = []
        self.player_4_deck = []
        self.player_5_deck = []
        #come up with logical construct

        self.current_player_card_deck = [] #used for tracking cards

        self.player_1_solution_deck = [] #this is the solution set for each player so random can return one of 3, until filled for next player
        self.player_2_solution_deck = [] #this structure can be scaled for any of the AI agents as these can be reused
        self.player_3_solution_deck = []
        self.player_4_solution_deck = []
        self.player_5_solution_deck = []

        self.all_possible_player_decks = ["Miss Scarlet", "Colonel Mustard", "Professor Plump", "Mrs. Peacock", "Mr. Green", "Dr. Orchid"]
        self.all_possible_weapon_decks = ["candlestick", "dagger", "lead pipe", "revolver", "rope", "wrench"] #used when all options are found to calculate solution set
        self.all_possible_rooms_decks =  ["study", "hall", "lounge", "dining room", "kitchen", "ballroom", "conservatory", "billard room", "library"]

        self.AI_solved_the_solution = False

        self.value_list = [] #list that will contain current player's cards

        self.final_offical_deck = []

    def player_movement(self, movement_direction): #used for moving the piece/tracking movement
        movement_checker_list = self.logical_representation[self.current_node] #gets values of where to move next
        if movement_direction == 1: #up
            movement_value = movement_checker_list[0]
            print(movement_value)
            if movement_value != None: #if not wall
                self.current_node = movement_value #moving it logically
                self.physical_display_coordinates = self.physical_representation[self.current_node] #updates current location
                self.rect = self.image.get_rect(topleft=self.physical_display_coordinates) #draws piece
                if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"): #checks if in room
                    return [True, True] #movement true, in room true
                return [True, False] #movement true, in room false

        elif movement_direction == 2: #right
            movement_value = movement_checker_list[1]
            print(movement_value)
            if movement_value != None:
                self.current_node = movement_value #moving it logically
                self.physical_display_coordinates = self.physical_representation[self.current_node]
                self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                    return [True, True]
                return [True, False] #confirmed value locker
            
        elif movement_direction == 3: #down
            movement_value = movement_checker_list[2]
            print(movement_value)
            if movement_value != None:
                self.current_node = movement_value #moving it logically
                self.physical_display_coordinates = self.physical_representation[self.current_node]
                self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                    return [True, True]
                return [True, False] #confirmed value locker

        elif movement_direction == 4: #left
            movement_value = movement_checker_list[3]
            print(movement_value)
            if movement_value != None:
                self.current_node = movement_value #moving it logically
                self.physical_display_coordinates = self.physical_representation[self.current_node]
                self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                    return [True, True]
                return [True, False] #confirmed value locker

    def add_cards(self, c1, c2, c3): #iused to give each character 3 cards for visualization
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3 #taking what the AI already knows and putting it in its knowledge base
        self.value_list = [self.c1, self.c2, self.c3] #defines for final calculation on solution

    def return_cards(self): #returns the cards the player has to show only 1
        self.value_list = [self.c1, self.c2, self.c3]
        return self.value_list
    
    def return_current_position(self): #returns current position of piece for alcuations
        return self.current_node
    
    def set_current_node(self, movement_node): #updates node for teleportation
        self.current_node = movement_node
        self.physical_display_coordinates = self.physical_representation[self.current_node]
        self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)

    def set_in_building(self, value): #updates location of piece for teleportation
        self.in_building = value

    def return_player_number(self): #shows what number each player is
        return int(self.player_number)
    
    def return_AI_Controlled(self): #tells code which player is AI and which is not
        return self.AI_enabled
    
    def return_current_number_of_turns(self): #for communicating when to move next
        return self.movement_turns
    
    def set_lock_back_to_true_for_dice_roll(self):
        self.AI_Dice_Lock = False
    
    def set_movement_lock_to_a_value(self):
        self.movement_turns = 1
    
    def get_player_card_deck(self, card_deck):
        self.current_player_card_deck = card_deck #taking current player's card deck

    def set_player_as_eliminated(self):
        self.player_is_eliminated_lock = True #eliminates the player

    def return_player_elimination_status(self):
        return self.player_is_eliminated_lock #returns lock for checking
    
    def return_p1_card_deck(self):
        return self.player_1_deck #returns cards decks
    
    def return_p2_card_deck(self): #these are used to return the length of the cards and thus determines which player was guessed
        return self.player_2_deck
    
    def return_p3_card_deck(self):
        return self.player_3_deck
    
    def return_p4_card_deck(self):
        return self.player_4_deck
    
    def return_p5_card_deck(self):
        return self.player_5_deck
    
    def return_did_ai_solve_solution(self):
        return self.AI_solved_the_solution #if true, main will end the game
    

    
    def get_all_player_cards(self, p1_card_deck, p2_card_deck, p3_card_deck, p4_card_deck, p5_card_deck): #suggestion mechanism #5 decks for the players
        self.player_1_solution_deck = p1_card_deck
        self.player_2_solution_deck = p2_card_deck
        self.player_3_solution_deck = p3_card_deck
        self.player_4_solution_deck = p4_card_deck
        self.player_5_solution_deck = p5_card_deck #assigns the cards for random computation
    
    #gets chracter details

#in flow control this executes once
    def AI_suggestions(self):
        self.card_checker_duplicate_lock = False #resets lock/sets lock
        card_checker_duplicate = False #checks if duplicate occured
        the_value = None #initializes this value that is used for computations

        if len(self.player_1_deck) != 3 and self.card_checker_duplicate_lock == False:  #and check for card value#start with player 1 and move up (each player has up to 3 cards)
            the_value = random.choice(self.player_1_solution_deck) #takes random value from player 1 deck
            for i in self.player_1_deck:
                if i == the_value:
                    card_checker_duplicate = True #marks duplicate
            self.card_checker_duplicate_lock = True #locks out the lock so it does not run again
            if card_checker_duplicate == False: #if after running the check, there are no duplicates
                self.player_1_deck.append(the_value) #if all is good, adds value to list #this appears to work
                
            

        elif len(self.player_2_deck) != 3 and self.card_checker_duplicate_lock == False:  #and check for card value#start with player 1 and move up (each player has up to 3 cards)
            the_value = random.choice(self.player_2_solution_deck) #takes random value from player 1 deck
            for i in self.player_2_deck:
                if i == the_value:
                    card_checker_duplicate = True #marks duplicate
            self.card_checker_duplicate_lock = True #locks out the lock so it does not run again
            if card_checker_duplicate == False: #if after running the check, there are no duplicates
                self.player_2_deck.append(the_value) #if all is good, adds value to list #this appears to work
        
        elif len(self.player_3_deck) != 3 and self.card_checker_duplicate_lock == False:  #and check for card value#start with player 1 and move up (each player has up to 3 cards)
            the_value = random.choice(self.player_3_solution_deck) #takes random value from player 1 deck
            for i in self.player_3_deck:
                if i == the_value:
                    card_checker_duplicate = True #marks duplicate
            self.card_checker_duplicate_lock = True #locks out the lock so it does not run again
            if card_checker_duplicate == False: #if after running the check, there are no duplicates
                self.player_3_deck.append(the_value) #if all is good, adds value to list #this appears to work
            
        elif len(self.player_4_deck) != 3 and self.card_checker_duplicate_lock == False:  #and check for card value#start with player 1 and move up (each player has up to 3 cards)
            the_value = random.choice(self.player_4_solution_deck) #takes random value from player 1 deck
            for i in self.player_4_deck:
                if i == the_value:
                    card_checker_duplicate = True #marks duplicate
            self.card_checker_duplicate_lock = True #locks out the lock so it does not run again
            if card_checker_duplicate == False: #if after running the check, there are no duplicates
                self.player_4_deck.append(the_value) #if all is good, adds value to list #this appears to work
        
        elif len(self.player_5_deck) != 3 and self.card_checker_duplicate_lock == False:  #and check for card value#start with player 1 and move up (each player has up to 3 cards)
            the_value = random.choice(self.player_5_solution_deck) #takes random value from player 1 deck
            for i in self.player_5_deck:
                if i == the_value:
                    card_checker_duplicate = True #marks duplicate
            self.card_checker_duplicate_lock = True #locks out the lock so it does not run again
            if card_checker_duplicate == False: #if after running the check, there are no duplicates
                self.player_5_deck.append(the_value) #if all is good, adds value to list #this appears to work

        else: #this means that when everything is collected, organize the pieces to come with the solution
            pass #does nothing

    def bfs_movement_grid(self):
        rooms = ("189", "190", "191", "192", "193", "194", "195", "196", "197")
        visited = set()
        queue = deque() #data structures so that visited and unvisited can be checked
        visited.add(self.current_node)
        visited.add(self.turn_start_node) #do not walk straight back into the room the turn started in

        neighbors = self.logical_representation.get(self.current_node, [None, None, None, None])
        for direction, neighbor in enumerate(neighbors, start=1): #first step can be up, right, down or left
            if neighbor and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, direction)) #remembers which first step started this path

        while queue: #while there is something in the queue
            current_node, first_direction = queue.popleft() #closest tile first
            if current_node in rooms: #closest room found
                return first_direction #go the way that starts the path to it
            neighbors = self.logical_representation.get(current_node, [None, None, None, None])
            for neighbor in neighbors:
                if neighbor and neighbor not in visited: #if neighbor is not visited
                    visited.add(neighbor)
                    queue.append((neighbor, first_direction))

        return random.randint(1, 4) #no room found, so try any direction


    def AI_player_movement(self): #used for AI movement
        if self.AI_Dice_Lock == False: #run once
            self.movement_turns = random.randint(2,12) #simulates the two dice
            self.turn_start_node = self.current_node #remember where this turn started
            self.AI_Dice_Lock = True #lock it out

        movement_direction = random.randint(1, 4) #random value incase things do not work 
        movement_checker_list = self.logical_representation[self.current_node] #gets values of where to move next
        movement_value = None #initializes movement_value

        direction_to_go = self.bfs_movement_grid() #gets BFS coordinate

        movement_direction = direction_to_go #takes the BFS value and moves it to the general variable


        current_position = self.logical_representation[self.current_node] #separate check that if the BFS hits a room value, it will always go to the room 
        if current_position[0] in ("189", "190", "191", "192", "193", "194", "195", "196", "197") and current_position[0] != self.turn_start_node: 
            movement_direction = 1
        elif current_position[1] in ("189", "190", "191", "192", "193", "194", "195", "196", "197") and current_position[1] != self.turn_start_node: 
            movement_direction = 2
        elif current_position[2] in ("189", "190", "191", "192", "193", "194", "195", "196", "197") and current_position[2] != self.turn_start_node: 
            movement_direction = 3
        elif current_position[3] in ("189", "190", "191", "192", "193", "194", "195", "196", "197") and current_position[3] != self.turn_start_node: #if player comes close to door, go to the room
            movement_direction = 4
        
        

        turns_before_move = self.movement_turns #used to notice a blocked step

        if self.movement_turns > 0: #if you can move do one of the choices below

            if movement_direction == 1: #up
                movement_value = movement_checker_list[0] #if valid, move
                if movement_value != None: #if not wall
                    self.current_node = movement_value #moving it logically
                    self.physical_display_coordinates = self.physical_representation[self.current_node] #updates current location
                    self.rect = self.image.get_rect(topleft=self.physical_display_coordinates) #draws piece
                    self.movement_turns -= 1 #remove 1 from the counter
                    if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                        self.movement_turns = 0 #entered, room now stop for suggestion
                        self.AI_suggestions() #gets suggestion to occur

            elif movement_direction == 2: #right
                movement_value = movement_checker_list[1]
                if movement_value != None:
                    self.current_node = movement_value #moving it logically
                    self.physical_display_coordinates = self.physical_representation[self.current_node]
                    self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                    self.movement_turns -= 1 #remove 1 from the counter
                    if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                        self.movement_turns = 0
                        self.AI_suggestions()
                
            elif movement_direction == 3: #down
                movement_value = movement_checker_list[2]
                if movement_value != None:
                    self.current_node = movement_value #moving it logically
                    self.physical_display_coordinates = self.physical_representation[self.current_node]
                    self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                    self.movement_turns -= 1 #remove 1 from the counter
                    if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"): #this works, make it do suggestions
                        self.movement_turns = 0
                        self.AI_suggestions()

            elif movement_direction == 4: #left
                movement_value = movement_checker_list[3]
                if movement_value != None:
                    self.current_node = movement_value #moving it logically
                    self.physical_display_coordinates = self.physical_representation[self.current_node]
                    self.rect = self.image.get_rect(topleft=self.physical_display_coordinates)
                    self.movement_turns -= 1 #remove 1 from the counter
                    if self.current_node in ("189", "190", "191", "192", "193", "194", "195", "196", "197"):
                        self.movement_turns = 0
                        self.AI_suggestions()

        if self.movement_turns == turns_before_move and self.movement_turns > 0: #the step was blocked, so the AI would be stuck forever
            self.movement_turns -= 1

        if self.movement_turns == 0: #at the end of each turn if the AI has enough to solve the game, then the AI will solve the game
            length_deck_1 = len(self.player_1_deck) #takes the length of each deck before appending to allow testing for total deck with cards
            length_deck_2 = len(self.player_2_deck) #check makes sure that the player can get the right solution before suggesting
            length_deck_3 = len(self.player_3_deck)
            length_deck_4 = len(self.player_4_deck)
            length_deck_5 = len(self.player_5_deck) #for each deck
            
            length_of_total_deck = length_deck_1 + length_deck_2 + length_deck_3 + length_deck_4 + length_deck_5 #total card amount for each player
            if length_of_total_deck == 15: #means the player has all of the cards needed to solve the game
                
                self.AI_solved_the_solution = True #sends signal to lock to end the game in main eventually
                
                return True #means they solved it, in the main code the solved mechanism fires
                

            return False #executes return at the end of the turns to end the round
            