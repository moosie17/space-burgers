import pygame
import sys
import random
from pygame.locals import *
import time

def score_display(game_state):
    # Function to add current score at the top and high score at the bottom of the screen --
    if(game_state == 'main_game'):
        # Making surface out of a text
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (screen_width/2,(screen_height/2) - 200))
        screen.blit(score_surface, score_rect)

    elif(game_state == 'game_over'):
        # score_surface = game_font.render("Score: {}".format(str(int(score))),True,(255,255,255))
        score_surface = game_font.render("Score: {}".format(str(int(score))),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (screen_width/2,(screen_height/2) - 200))
        screen.blit(score_surface, score_rect)

        # Also display high score at the end of the game --
        high_score_surface = game_font.render("High Score: {}".format(str(int(high_score))),True,(255,255,255))
        # high_score_surface = game_font.render(str(int(high_score)),True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (screen_width/2,(screen_height/2) + 200))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    # Function to update high score
    if score > high_score:
        high_score = score
    
    return high_score

def check_collision(stripe, enemy_strip_group):
    # Function to check collision between player and enemies --
    # If collision occurs, the below if condition returns a boolean as True:
    if pygame.sprite.spritecollideany(stripe, enemy_strip_group):
        # Kill player --
        stripe.kill()

        # Stop background music --
        pygame.mixer.music.stop()
        time.sleep(1)

        # Play collision sound --
        collision_sound.play()
        time.sleep(3)
        # Change game_active to False to end game
        game_active = False
        return game_active
    
    else:
        game_active = True
        return game_active


# Initalize pygame --
pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.mixer.music.load("game_sounds/background_sound.ogg")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

# Define screen/display constants --
screen_height = 600
screen_width = 800
fps = 30

# Define game variables --
score = 0
high_score = 0
game_active = True

# Adding fonts to the game to show scores --
game_font = pygame.font.Font('04B_19.ttf', 40)

# Generate display window for the game --
screen = pygame.display.set_mode((screen_width,screen_height))

# Display the window using flip() --
pygame.display.flip()

# Define a Player (surface) object by extending pygame.sprite.Sprite --
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Import the parent class (Sprite's) constructor --
        super().__init__()
        # Let's create instance variables for the player object --
        # self.surf = pygame.image.load("game_images/rocket_small.png").convert_alpha()
        self.surf = pygame.image.load("game_images/boy_head.png").convert_alpha()
        # Make the player surface white in color --
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center = (screen_width/2,screen_height/2))
    
    def update(self, pressed_keys):
        # Function which takes in the keys being pressed by the user
        # and moves the player accordingly --
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
            # move_up_sound.play()

        elif pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
            # move_down_sound.play()
        
        elif pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        
        elif pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        # To keep the player movements within the screen --
        # Check int value of the X-coordinate of the left side of the rectangle
        if self.rect.left < 0:
            self.rect.left = 0

        # Check int value of the X-coordinate of the right side of the rectangle
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        
        # Check int value of the Y-coordinate of the top side of the rectangle
        if self.rect.top <= 0:
            self.rect.top = 0
        
        #  Check int value of the Y-coordinate of the bottom side
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

# Define a Eneny (surface) object by extending pygame.sprite.Sprite --
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Import the parent class (Sprite's) constructor --
        super().__init__()
        # Let's create instance variables for the enemy --
        self.surf = pygame.image.load("game_images/space_burger_2.png").convert_alpha()
        # Make the enemy surface white in color --
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # Assigning the rect for enemy as follows -- the center's x coordinate is a random position
        # between screen_width + 20 ... screen_width + 100 --> we want enemies to come from the right
        # side of the game. And the enemy center's y coordiate is a random position between 0 to 
        # screen_height
        self.rect = self.surf.get_rect(
            center = (random.randint(screen_width + 20, screen_width + 100),
            random.randint(0, screen_height)))
        
        # Speed at which the enemy moves on the screen --
        self.speed = random.randint(5,8)

    def update(self):
        # Function to move the enemy at a random speed from right to left in a straight line
        # Note: that's why for example: the move_ip coordinates would be something like (-5,0)
        self.rect.move_ip(- self.speed, 0)

        # Check int value of the X-coordinate of the right side of the rectangle
        # This means as soon as the enemy passes the left side of the screen, we kill it --
        if self.rect.right < 0:
            self.kill()
            # .kill() is a method of Sprite Groups which stops the enemy which has crossed 
            # the left screen from further processing in the game 

# Define a Cloud (surface) object by extending pygame.sprite.Sprite --
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("game_images/cloud_small.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (random.randint(screen_width + 20, screen_width + 100),
            random.randint(0, screen_height)))

    # This means as soon as the CLOUD passes the left side of the screen, we kill it --
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Instantiate a player. Right now, this is just a rectangle.
player = Player()

# Create a custom event for adding a new enemy --
# Note: pygame defines events internally as integers, so when you need to define a new event 
# you do a +1 to make sure your event is created internally with a unique integer
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
# Now invoke this custom event inside the GAME LOOP

# Create a custom event for adding a new CLOUD --
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
# Now invoke this custom CLOUD event inside the GAME LOOP


# Creating 2 SPRITE GROUPS --
# enemies_sprites is a sprite group used for collision detection and position updates --
enemies_sprites = pygame.sprite.Group()

# all_sprites is a sprite group used for rendering --
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Creating a new sprite group for clouds --
clouds = pygame.sprite.Group()

# Adding sounds to the player's movements --
move_up_sound = pygame.mixer.Sound('game_sounds/move_up_sound.ogg')
move_down_sound = pygame.mixer.Sound('game_sounds/move_down_sound.ogg')
collision_sound = pygame.mixer.Sound('game_sounds/game_over_sound.ogg')

game_over_surface = pygame.image.load('game_images/game_over_small.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (screen_width/2,screen_height/2))


# Writing the game loop which controls game logic and
# does event handling -- that means the game exits when the user closes the game
# or when the spaceship collides with the enemy

running = True

while running:
    # Looking at the event queue for user input
    for event in pygame.event.get():
        # Did user try to close the game window?
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Did the user press down on a key?
        elif event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        elif event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active == True
                # player.rect.center = (screen_width/2,screen_height/2)
                score = 0
            
        # Event which adds a new enemy to the screen --
        elif(event.type == ADDENEMY):
            # Create a enemy object from the class Enemy()
            new_enemy = Enemy()
            # Add this enemy to the enemy sprite group --
            enemies_sprites.add(new_enemy)
            # Add this enemy to the all_sprite group --
            all_sprites.add(new_enemy)
        
        # Event which adds a new cloud to the game --
        elif(event.type == ADDCLOUD):
            # Create a cloud object from the class Cloud()
            new_cloud = Cloud()
            # Add this enemy to the clouds sprite group --
            clouds.add(new_cloud)
             # Add this enemy to the all_sprite group --
            all_sprites.add(new_cloud)

    if game_active == True:       
        # Extending the game loop to get the combination of keys which
        # the user is pressing at any given moment --
        pressed_keys = pygame.key.get_pressed()

        # Pass the keys which the user is pressing to the update function
        # in the Player class to make the player move in place (rect.move_ip) --
        player.update(pressed_keys)
        
        # Update enemy's movement in the game using the enemies_sprites group--
        enemies_sprites.update()
        clouds.update()

        # Updating game score --
        score += 0.1
        # score_display('main_game')

        # Change background color of display window to black --
        screen.fill((135, 206, 250))

        # Drawing the player and all enemies to the display window by iterating over all_sprites group --
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check collision between player and enemies --
        game_active = check_collision(player, enemies_sprites)

    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')


    pygame.display.flip()
    clock.tick(fps)
