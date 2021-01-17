import pygame
import math
import random

pygame.init()

running = True

#IMAGES
background = pygame.image.load("images/background.png")
ship = pygame.image.load("images/ship.png")
asteroid_small = pygame.image.load("images/asteroid_small.png")
asteroid_medium = pygame.image.load("images/asteroid_medium.png")
asteroid_large = pygame.image.load("images/asteroid_large.png")

#SOUNDS
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
big_hit_sound = pygame.mixer.Sound("sounds/big_hit.wav")
light_hit_sound = pygame.mixer.Sound("sounds/light_hit.wav")
damage_sound = pygame.mixer.Sound("sounds/damage.wav")




lives = 3
score = 0
game_over = False


pygame.display.set_caption("Asteroids")

class Player(object):
    def __init__(self):
        self.sprite = ship
        self.width = 16
        self.height = 16
        self.x = scr_width//2
        self.y = scr_height//2
        self.angle = 0
        self.rotate_surface = pygame.transform.rotate(self.sprite, self.angle)

        #get_rect is used to create a rectangle to get the location of the blit, then to pass the center argument to get the center of the ship because it rotates from its center
        self.rotate_rect = self.rotate_surface.get_rect()
        self.rotate_rect.center = (self.x, self.y)

        #finds cosine of angle, +90 is used to fix offset since the start of the angle is 0 so i want it to face upwards instead of to the right
        self.cos = math.cos(math.radians(self.angle + 90))  
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width//2, self.y - self.sin * self.height//2)

    #drawing ship
    def draw(self, window):
        window.blit(self.rotate_surface, self.rotate_rect)

    def turn_left(self):
        self.angle += 5
        self.rotate_surface = pygame.transform.rotate(self.sprite, self.angle)
        self.rotate_rect = self.rotate_surface.get_rect()
        self.rotate_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width//2, self.y - self.sin * self.height//2)

    def turn_right(self):
        self.angle -= 5
        self.rotate_surface = pygame.transform.rotate(self.sprite, self.angle)
        self.rotate_rect = self.rotate_surface.get_rect()
        self.rotate_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width//2, self.y - self.sin * self.height//2)

    def move_forwards(self):
        self.x += self.cos * 6
        self.y -= self.sin * 6
        self.rotate_surface = pygame.transform.rotate(self.sprite, self.angle)
        self.rotate_rect = self.rotate_surface.get_rect()
        self.rotate_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width//2, self.y - self.sin * self.height//2)     

    def move_backwards(self):
        self.x -= self.cos * 6
        self.y += self.sin * 6
        self.rotate_surface = pygame.transform.rotate(self.sprite, self.angle)
        self.rotate_rect = self.rotate_surface.get_rect()
        self.rotate_rect.center = (self.x, self.y)
        self.cos = math.cos(math.radians(self.angle + 90))
        self.sin = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cos * self.width//2, self.y - self.sin * self.height//2)      

    def player_input(self):
        global score
        global lives
        global game_over
        #a timer to stop the bullets from all going out at once super fast if the key is held
        global cooldown_tracker
        cooldown_tracker += clock.get_time()
        if cooldown_tracker > 300 and keys[pygame.K_SPACE] and game_over == False:
            cooldown_tracker = 0

        #player inputs
        if keys[pygame.K_UP] and game_over == False:
            player.move_forwards()
        if keys[pygame.K_LEFT] and game_over == False:
            player.turn_left()
        if keys[pygame.K_RIGHT] and game_over == False:
            player.turn_right()
        if keys[pygame.K_DOWN] and game_over == False:
            player.move_backwards()
        if keys[pygame.K_SPACE] and cooldown_tracker == 0 and game_over == False:
            bullets.append(Bullet())
            shoot_sound.play()
        if keys[pygame.K_RETURN] and game_over == True:
            game_over = False
            lives = 3
            asteroids.clear()
            score = 0

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

    #function to make the player wrap around the screen
    def wrap(self):
        if self.x < 0:
            self.x = scr_width
        elif self.x >scr_width:
            self.x = 0
        elif self.y <0:
            self.y = scr_height
        elif self.y > scr_height:
            self.y = 0
            

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.width = 3
        self.height = 3

        #matching direction of bullet with direction of ship
        self.cosB = player.cos
        self.sinB = player.sin
        self.x_vel = self.cosB * 10
        self.y_vel = self.sinB * 10

    def bullet_move(self):
        self.x += self.x_vel
        self.y -= self.y_vel

    def draw(self,window):
        pygame.draw.rect(window, (51,255,255), [self.x, self.y, self.width, self.height])


class Asteroid(object):
    def __init__(self, size):
        #setting the apropriate size to the sprite
        self.size = size
        if size == 1:
            self.sprite = asteroid_small
        if size == 2:
            self.sprite = asteroid_medium    
        if size == 3:
            self.sprite = asteroid_large
        
        #setting asteroid size
        self.width = 50 * size
        self.height = 50 * size

        #way of randomizing asteroid spawns outside of screen I found on the internet
        self.spawn = random.choice([(random.randrange(0,scr_width - self.width), random.choice([-1*self.height - 5, scr_height+5])), (random.choice([-1*self.width -5, scr_width + 5]), random.randrange(0, scr_height - self.height))])
        self.x, self.y = self.spawn
        
        #determining direction of asteroid when spawned 
        if self.x < 0:
            self.xdirection = 1
        else:
            self.xdirection = -1
        if self.y < 0:
            self.ydirection = 1
        else:
            self.ydirection = -1
        self.xvel = self.xdirection * random.randrange(1,3)
        self.yvel = self.ydirection * random.randrange(1,3)

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))


scr_width = 500
scr_height = 500
player = Player()
bullets = []
asteroids = []
clock = pygame.time.Clock()
window = pygame.display.set_mode((scr_width,scr_height))
cooldown_tracker = 0
asteroid_timer = 0
highscore = open("highscore.txt","r")
hs = int(highscore.read())
# game_over = False

def load_hs():
    global hs
    if game_over == True:
        if score > hs:
            f = open("highscore.txt","w")
            f.write(str(score))
            hs = score
    


def redrawGameWindow():
    global lives
    global score
    window.blit(background,(0,0))
    font = pygame.font.SysFont("arial", 20)
    text_lives = font.render("LIVES: " + str(lives), 0, (255,255,255))
    text_score = font.render("SCORE: " + str(score), 0, (255,255,255))
    text_retry = font.render("PRESS ENTER TO RETRY OR ESC TO EXIT", 0, (255,255,255))
    text_hs = font.render("HI SCORE: " + str(hs), 0, (255,255,255))
    player.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    for asteroid in asteroids:
        asteroid.draw(window)

        #detecting collisions between player and asteroid
        if(player.x >= asteroid.x and player.x <= asteroid.x + asteroid.width) or (player.x + player.width >= asteroid.x and player.x + player.width <= asteroid.x + asteroid.width):
            if(player.y >= asteroid.y and player.y <= asteroid.y + asteroid.height) or (player.y + player.height >= asteroid.y and player.y + player.height <= asteroid.y + asteroid.height):  
                
                lives -= 1
                asteroids.pop(asteroids.index(asteroid))
                damage_sound.play()
                break

        #detecting collisions between bullets and asteroids
        for bullet in bullets:
            if bullet.x < 0 or bullet.x > scr_width or bullet.y < 0 or bullet.y > scr_height:
                bullets.pop(bullets.index(bullet))
            if (bullet.x >= asteroid.x and bullet.x <= asteroid.width + asteroid.x) or (bullet.x + bullet.width >= asteroid.x and bullet.x + bullet.width <= asteroid.width + asteroid.x):
                if (bullet.y >= asteroid.y and bullet.y <= asteroid.height + asteroid.y) or (bullet.y +bullet.height >= asteroid.y and bullet.y +bullet.height <= asteroid.height + asteroid.y):
                    asteroids.pop(asteroids.index(asteroid))
                    bullets.pop(bullets.index(bullet))

                    #creating new and smaller asteroids that break off when a bigger one is destroyed
                    if asteroid.size == 3:
                        big_hit_sound.play()
                        score += 250
                        new_asteroid1 = Asteroid(2)
                        new_asteroid2 = Asteroid(2)

                        new_asteroid1.x = asteroid.x
                        new_asteroid2.x = asteroid.x
                        new_asteroid1.y = asteroid.y
                        new_asteroid2.y = asteroid.y

                        asteroids.append(new_asteroid1)
                        asteroids.append(new_asteroid2)
                    
                    elif asteroid.size == 2:
                        big_hit_sound.play()
                        score += 500
                        new_asteroid1 = Asteroid(1)
                        new_asteroid2 = Asteroid(1)

                        new_asteroid1.x = asteroid.x
                        new_asteroid2.x = asteroid.x
                        new_asteroid1.y = asteroid.y
                        new_asteroid2.y = asteroid.y

                        asteroids.append(new_asteroid1)
                        asteroids.append(new_asteroid2)
                    
                    elif asteroid.size == 1:
                        score += 1000
                        light_hit_sound.play()

    if game_over == True:
        window.blit(text_retry, (scr_width//2 - text_retry.get_width()//2, scr_height//2 - text_retry.get_height()))
            

    window.blit(text_lives, (25, 25))
    window.blit(text_score, (scr_width - text_score.get_width() - 25, 25))
    window.blit(text_hs, (scr_width//2 - text_hs.get_width()//2, 25)) 
              

    pygame.display.update()


#MAIN LOOP   
while running == True:
    pygame.time.delay(15)
    clock.tick(60)


    if lives > 0:
        game_over == False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    if game_over == False:
        #timing asteroid spawns and varying the randomness of different sizes when spawned
        asteroid_timer += clock.get_time()
        if asteroid_timer % 50 == 0:
            rand = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(rand))

        player.wrap()
        # keys = pygame.key.get_pressed()
        # player.player_input()
        

        for bullet in bullets:
            bullet.bullet_move()

        for asteroid in asteroids:
            asteroid.x += asteroid.xvel
            asteroid.y += asteroid.yvel

    keys = pygame.key.get_pressed()
    player.player_input()
    print(hs)
    
    redrawGameWindow()
    load_hs()


    if lives <= 0:
        game_over = True


    

#quits program once loop is broken
pygame.quit()


