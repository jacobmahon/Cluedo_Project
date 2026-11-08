import pygame #imports the pygame module

# The most recent mouse click, in game coordinates (None means no click this frame).
# main.py sets this once per frame, and the buttons share it.
# When a button uses the click it sets this back to None, so one click can never press two buttons.
click_position = None


def set_click(position): #called by main.py when the mouse is pressed
    global click_position
    if click_position is None: #only keep the first click of the frame
        click_position = position


def clear_click(): #called by main.py at the end of every frame
    global click_position
    click_position = None


class Button:
    def __init__(self, x_coordinate, y_coordinate, picture_value, screen_value): #initial values
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate #location to display
        self.picture_value = picture_value #picture to use
        self.button_bounds = self.picture_value.get_rect(topleft=(self.x_coordinate, self.y_coordinate)) #area that can be clicked
        self.screen_value = screen_value #on the executing screen

    def display_on_screen(self): #draws the button and returns True if it was clicked
        global click_position

        self.screen_value.blit(self.picture_value, (self.x_coordinate, self.y_coordinate)) #draws button

        if click_position is not None and self.button_bounds.collidepoint(click_position): #click landed on this button
            click_position = None #use up the click so no other button can use it
            return True #button was clicked

        return False #nothing clicked
