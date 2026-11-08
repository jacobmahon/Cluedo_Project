import pygame #libraries used

class Weapon_Pieces(pygame.sprite.Sprite): #
    def __init__(self, photo_location, physical_representation, starting_dictionary_index): #imports necessary items
        super().__init__()
        photo_value = pygame.image.load(photo_location).convert_alpha() #loads picture
        self.image = pygame.transform.smoothscale(photo_value, (30, 30)) #adjust picture size

        self.physical_representation = physical_representation #use for tracking visuals
        self.physical_display_coordinates = self.physical_representation[starting_dictionary_index] #used for updating moves
        self.current_node = starting_dictionary_index #used for changing visual representation
        
        self.rect = self.image.get_rect(topleft=self.physical_display_coordinates) #draws initial button

    def set_current_node(self, movement_node): #updates piece location based on guess
        self.current_node = movement_node #updates current location
        self.physical_display_coordinates = self.physical_representation[self.current_node] #puts it in dictionary
        self.rect = self.image.get_rect(topleft=self.physical_display_coordinates) #draws new location