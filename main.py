import pygame
import os
from settings import*
from tiles import Tile
import buttons
import time



#initialiser le module pygame
pygame.init()
#taille de l'écran
screen_width = 1540
screen_height = 800


#définir l'écran
screen = pygame.display.set_mode((screen_width, screen_height))
#le titre de l'écran
pygame.display.set_caption('Falling fight')

#définir le nombre d'images par secondes
clock = pygame.time.Clock()
FPS = 60

#definir les variables du jeu
GRAVITY = 0.75
TILE_SIZE = 24

start_game = False

moving_left = False
moving_right = False
moving_left1 = False
moving_right1 = False
shoot = False
shoot1 = False
balle = False
ball_thrown = False
balle1 = False
ball_thrown1 = False
construction = False
construction1 = False
wall_constructed = False
wall_constructed1 = False


#charger les images

#button images
start_img = pygame.image.load('Buttons/start_btn.png').convert_alpha()
exit_img = pygame.image.load('Buttons/exit_btn.png').convert_alpha()
player_win = pygame.image.load('Buttons/player_win.png').convert_alpha()
enemy_win = pygame.image.load('Buttons/enemy_win.png').convert_alpha()


#bullet
flake_img = pygame.image.load('Character/icons/flake.png').convert_alpha()
#balle
ball_img = pygame.image.load('Character/icons/balle.png').convert_alpha()
#special_balle
special_ball_img = pygame.image.load('Character/icons/golden_balle.png').convert_alpha()
#hearts
heart_img = pygame.image.load('Character/icons/heart.png').convert_alpha()
#fire
fire_img = pygame.image.load('Character/icons/fire.png').convert_alpha()
#stick
brick_img = pygame.image.load('Character/icons/stick.png').convert_alpha()

#image des boîtes
flake_box_img = pygame.image.load('Character/icons/flake_box.png').convert_alpha()
fire_box_img = pygame.image.load('Character/icons/fire_box.png').convert_alpha()
power_box_img = pygame.image.load('Character/icons/golden_balle_box.png').convert_alpha()
#création d'un dictionnaire d'images
item_boxes = {
    'Fire' : fire_box_img,
    'Flake' : flake_box_img,
    'Power' : power_box_img
}

#définir la couleur de l'arrière plan
BG = ('grey')

#définir la couleur verte
GREEN = (0,140,140)
#définir la couleur rouge
RED = ('red')

#définir la couleur blanche
WHITE = (255,255,255)

#définir la typographie
font = pygame.font.SysFont('Arial', 20)


def draw_text(text, font, text_color, x, y):
    #créer une fonction qui permettra d'écrire du texte sur l'écran
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))


def draw_background():
    #créer une fonction qui permettra de dessiner l'arrière-plan
    screen.fill(BG)

def reset():
    #créer une fonction qui permettra de relancer le jeu quand les joueurs perdent une vie
    for stick in brick_group:
        stick.kill()
    for balls in ball_group:
        balls.kill()
    player.flakes = 5
    player.walls = 100
    player.balls = 1000000
    player.fires = 2
    enemy.fires = 2
    enemy.flakes = 5
    enemy.walls = 100
    enemy.balls = 1000000
    item_box = Itembox('Fire', 1000, 748)
    item_box_group.add(item_box)
    item_box = Itembox('Flake', 530, 748)
    item_box_group.add(item_box)
    item_box = Itembox('Power', 770, 315)
    item_box_group.add(item_box)
    item_box_group.update()
    item_box_group.draw(screen)


def stop():
    #créer une fonction qui permet de réinitialiser les valeurs à 0 quand le jeu se termine pour que l'on ne puisse plus jouer
    enemy.speed = 0
    enemy.fires = 0
    enemy.flakes = 0
    enemy.balls = 0
    player.speed = 0
    player.fires = 0
    player.flakes = 0
    player.balls = 0
    player.walls = 0
    enemy.walls = 0

class player1(pygame.sprite.Sprite):
    #création de la classe joueur ainsi que ses paramètres
    def __init__(self, char_type, x , y , scale , speed, flakes, balls, lifes, fires, power):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.initial_speed = speed
        self.flakes = flakes
        self.start_ammo = flakes
        self.shoot_cooldown = 0
        self.balls = balls
        self.fires = fires
        self.lifes = lifes
        self.walls = 100
        self.health = 100
        self.power = power
        self.max_power = power
        #lorsque power est au max : lance une balle géante jaune
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.on_ground = False
        self.flake_hit = False
        self.inflamed = False
        self.flip = False
        self.ball_collide = False
        self.shooter = False
        self.special = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #charger toutes les images pour les joueurs
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Shooting']
        for animation in animation_types:
            #réinitialiser temporairement la liste des images
            temp_list = []
            #compter le nombres d'images dans le fichier
            nb_of_frames = len(os.listdir(f'Character/{self.char_type}/{animation}'))
            for i in range(nb_of_frames):
                img = pygame.image.load(f'Character/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()


    def update(self):
        #la fonction update est une fonction qui actualise les fonctions qui sont crées dedans et le code qui y est écrit lorsqu'on lance le jeu
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0 :
            self.shoot_cooldown -=1

    def construct(self):
        #création d'une fonction qui permet de créer un mur pour le joueur
        if self.walls >0 :
            wall = Wall(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.centery,
                        player.direction)
            brick_group.add(wall)
            self.walls -= 1

    def construct1(self):
        # création d'une fonction qui permet de créer un mur pour l'ennemi
        if self.walls >0 :
            wall = Wall(enemy.rect.centerx + (0.5 * enemy.rect.size[0] * enemy.direction), enemy.rect.centery,
                        enemy.direction)
            brick_group.add(wall)
            self.walls -= 1



    def move(self, moving_left, moving_right):
        #création d'une fonction qui permet au joueur de bouger
        dx = 0
        dy = 0

        if moving_left :
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #sauter
        if self.jump == True and self.in_air == False:
            self.vel_y = -13
            self.jump = False
            self.in_air = True
        #gravité
        self.vel_y += GRAVITY
        dy += self.vel_y

        #collisions avec les éléments du décor

        for tile in level.tiles:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                elif self.vel_y >= 0 :
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.rect.top - self.rect.bottom

        for walls in brick_group:
            if walls.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if walls.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = walls.rect.bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = walls.rect.top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def move1(self, moving_left1, moving_right1):
        # création d'une fonction qui permet a l'ennemi du joueur de bouger
        dx = 0
        dy = 0

        if moving_left1 :
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right1:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #sauter
        if self.jump == True and self.in_air == False:
            self.vel_y = -13
            self.jump = False
            self.in_air = True
        #gravité
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #Les collisions avec le niveau
        for tile in level.tiles:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                elif self.vel_y >= 0 :
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.rect.top - self.rect.bottom
        #Les collisions avec les murs de brique
        for walls in brick_group:
            if walls.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if walls.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = walls.rect.bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = walls.rect.top - self.rect.bottom



        self.rect.x += dx
        self.rect.y += dy




    def shoot(self):
        #création d'une fonction qui permet de tirer des flocons pour le joueur
        if self.shoot_cooldown == 0 and self.flakes > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (1.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.flakes -= 1

    def shoot1(self):
        #création d'une fonction qui permet de tirer des flocons pour les ennemis
        if self.shoot_cooldown == 0 and self.flakes > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (1.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.flakes -= 1




    def update_animation(self):
        #création d'une fonction qui permettra d'actualiser les animations en fonctions des actions des joueurs
        ANIMATION_COOLDOWN = 150
        self.image = self.animation_list[self.action][self.frame_index]
        #Regarder si il y a eu assez de temps qui s'est écoulé depuis la dernière update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN :
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Si le nombre d'animation est dépassé, revenir au début
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0



    def update_action(self, new_action):
        #Regarder si la nouvelle action est différente de la précédente
        if new_action != self.action:
            self.action = new_action
            #actualiser les paramètres d'animations
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        #création d'une fonction pour déterminer ou non si le joueur ou l'ennemi est en vie
        if self.rect.bottom - 50 > screen_height :
            self.lifes -= 1
            time.sleep(1)
            player.rect.x = 460
            player.rect.y = 200
            enemy.rect.x = 1090
            enemy.rect.y = 200
            reset()
        if self.lifes <= 0:
            self.health = 0
            self.speed = 0 #modifier ca quand fini pour que le joueur tombe
            self.alive = False


    def draw(self):
        #création d'une fonction pour afficher à l'écran
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



class Itembox(pygame.sprite.Sprite):
    #création de la classe box et ses attributs
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))



    def update(self):
        #collisions avec les joueurs
        if pygame.sprite.collide_rect(self, player):
            #regarder quel type de box est-ce
            if self.item_type == 'Fire':
                player.fires = 2
            elif self.item_type == 'Flake':
                player.flakes = 5
            elif self.item_type == 'Power':
                player.power = 10
            self.kill()
        #collisions avec les ennemis
        if pygame.sprite.collide_rect(self, enemy):
            #regarder quel type de box est-ce
            if self.item_type == 'Fire':
               enemy.fires = 2
            elif self.item_type == 'Leaf':
                enemy.flakes = 5
            elif self.item_type == 'Power':
                enemy.power = 10
            self.kill()




class Ball(pygame.sprite.Sprite):
    #création de la classe balle et ses attributs
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = -17
        self.speed = 18
        self.image = ball_img
        self.special_image = special_ball_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.nb_rebound = 40


    def update(self):
        #la trajectoire
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        #regarder les collisions horizontales avec les joueurs
        for sprite in ball_group.sprites(): #on parcourt les éléments dans le groupe "ball_group"
            if sprite.rect.colliderect(player.rect):# Si un élément rentre en collision avec le rectangle du joueur
                player.ball_collide = True
                if player.rect.x > ball.rect.x: # S'il y a une collision à droite
                    player.rect.left = sprite.rect.right
                player.flake_hit = False
                player.speed = 5
                if player.rect.x < ball.rect.x : # S'il y a une collision à gauche
                    player.ball_collide = True
                    player.rect.right = sprite.rect.left
                player.flake_hit = False
                player.speed = 5

        #regarder les collisions horizontales avec les ennemis
        for sprite in ball_group.sprites():#on parcourt les éléments dans le groupe "ball_group"
            if sprite.rect.colliderect(enemy.rect):# Si un élément rentre en collision avec l'ennemi
                if enemy.rect.x > ball.rect.x: # S'il y a une collision à droite
                    enemy.ball_collide = True
                    enemy.rect.left = sprite.rect.right
                enemy.flake_hit = False
                enemy.speed = 5
                if enemy.rect.x < ball.rect.x :# S'il y a une collision à gauche
                    enemy.ball_collide = True
                    enemy.rect.right = sprite.rect.left
                enemy.flake_hit = False
                enemy.speed = 5


        #les collisions verticales avec les joueurs
        for sprite in ball_group.sprites(): #on parcourt les éléments dans le groupe "ball_group"
            if sprite.rect.colliderect(player.rect) : # Si un élément rentre en collision avec le joueur
                if player.rect.y > ball.rect.y: # S'il y a une collision en dessous du joueur
                    player.rect.top = sprite.rect.bottom
                if player.rect.y < ball.rect.y : # S'il y a une collision au dessus du joueur
                    player.rect.bottom = sprite.rect.top

        #les collisions verticales avec les ennemis
        for sprite in ball_group.sprites():#on parcourt les éléments dans le groupe "ball_group"
            if sprite.rect.colliderect(enemy.rect): # Si un élément rentre en collision avec l'ennemi
                if enemy.rect.y > ball.rect.y: # S'il y a une collision en dessous de l'ennemi
                    enemy.rect.top = sprite.rect.bottom
                if enemy.rect.y < ball.rect.y : # S'il y a une collision au dessus de l'ennemi
                    enemy.rect.bottom = sprite.rect.top



        #les collisions avec les éléments du décor
        for tile in level.tiles:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                self.speed -= 2
            if tile.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y += self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = tile.rect.bottom - self.rect.top
                    #gestion des rebonds
                    self.nb_rebound -= 1
                    if self.nb_rebound == 0:
                        self.kill()
                elif self.vel_y >= 0:
                    self.vel_y -= self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = tile.rect.top - self.rect.bottom
                    # gestion des rebonds
                    self.nb_rebound -= 1
                    if self.nb_rebound == 0:
                        self.kill()

        #les collisions avec les limites de l'écran de jeu
        if self.rect.left + dx < 0 or self.rect.left + dx > screen_width:
            self.direction *= -1

        #les collisions avec les murs de brique créés par les joueurs
        for sticks in brick_group:
            if sticks.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                self.speed -= 2
                sticks.kill()
            if sticks.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y += self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = sticks.rect.bottom - self.rect.top
                    sticks.kill()
                elif self.vel_y >= 0:
                    self.vel_y -= self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = sticks.rect.top - self.rect.bottom
                    sticks.kill()

        #actualiser les positions de la balle

        self.rect.x += dx
        self.rect.y += dy

class GoldenBall(pygame.sprite.Sprite):
    #création de la classe GoldenBall qui est une transformation de la petite balle en balle géante
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = -4
        self.speed = 30
        image = special_ball_img
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.nb_rebound = 40

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction *self.speed
        dy = self.vel_y -5



        #regarder les collisions avec les joueurs
        for sprite in ball_group.sprites():# On parcourt les éléments du groupe "ball_group"
            if sprite.rect.colliderect(player.rect):# Si un élément rentre en collision avec le joueur
                player.ball_collide = True
                if player.rect.x > special_ball.rect.x: # S'il y a une collision à droite
                    player.rect.left = sprite.rect.right
                player.flake_hit = False
                player.speed = 5
                if player.rect.x < special_ball.rect.x : # S'il y a une collision à gauche
                    player.ball_collide = True
                    player.rect.right = sprite.rect.left
                player.flake_hit = False
                player.speed = 5

        #regarder les collisions avec les ennemis
        for sprite in ball_group.sprites():# On parcourt les éléments du groupe "ball_group"
            if sprite.rect.colliderect(enemy.rect):# Si un élément rentre en collision avec l'ennemi'
                if enemy.rect.x > special_ball.rect.x: # S'il y a une collision à droite
                    enemy.ball_collide = True
                    enemy.rect.left = sprite.rect.right
                enemy.flake_hit = False
                enemy.speed = 5
                if enemy.rect.x < special_ball.rect.x :# S'il y a une collision à gauche
                    enemy.ball_collide = True
                    enemy.rect.right = sprite.rect.left
                enemy.flake_hit = False
                enemy.speed = 5


        #les collisions verticales avec le joueur
        for sprite in ball_group.sprites():# On parcourt les éléments du groupe "ball_group"
            if sprite.rect.colliderect(player.rect) : # Si un élément rentre en collision avec le joueur
                if player.rect.y > ball.rect.y: # S'il y a une collision en dessous du joueur
                    player.rect.top = sprite.rect.bottom
                if player.rect.y < ball.rect.y : # S'il y a une collision au dessus du joueur
                    player.rect.bottom = sprite.rect.top

        #les collisions verticales avec l'ennemi
        for sprite in ball_group.sprites():# On parcourt les éléments du groupe "ball_group"
            if sprite.rect.colliderect(enemy.rect): # Si un élément rentre en collision avec l'ennemi
                if enemy.rect.y > ball.rect.y: # S'il y a une collision en dessous de l'ennemi
                    enemy.rect.top = sprite.rect.bottom
                if enemy.rect.y < ball.rect.y : # S'il y a une collision au dessus de l'ennemi
                    enemy.rect.bottom = sprite.rect.top



        #regarder les collisions avec le décor
        for tile in level.tiles:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                self.speed -= 2
            if tile.rect.colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y += self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = tile.rect.bottom - self.rect.top
                    self.nb_rebound -= 1
                    if self.nb_rebound == 0:
                        self.kill()
                elif self.vel_y >= 0:
                    self.vel_y -= self.speed
                    self.speed = self.speed / 2
                    self.vel_y = self.vel_y / 1.2
                    dy = tile.rect.top - self.rect.bottom
                    self.nb_rebound -= 1
                    if self.nb_rebound == 0:
                        self.kill()


        #les collisions avec les bordures du jeu
        if self.rect.left + dx < 0 or self.rect.left + dx > screen_width:
            self.direction *= -1

        #les collisions avec les murs de brique créés par les joueurs
        for bricks in brick_group:
            if self.rect.colliderect(bricks.rect):
                bricks.kill()


        #actualiser les positions de la balle
        self.rect.x += dx
        self.rect.y += dy

class Bullet(pygame.sprite.Sprite):
    #création de la classe Bullet qui est le flocon
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = flake_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction




    def update(self):
        #faire bouger le flocon
        self.rect.x += (self.direction * self.speed)
        #regarder si le flocon a dépassé l'écran, et si oui le faire disparaître
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        #regarder les collisions avec les joueurs
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.flake_hit = True
                if player.flake_hit == True:
                    player.speed = 0
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.flake_hit = True
                if enemy.flake_hit == True :
                    enemy.speed = 0
                self.kill()

        for tile in level.tiles:
            if tile.rect.colliderect(self.rect):
                self.kill()


class Wall(pygame.sprite.Sprite):
    #création de la classe Wall qui est le mur créé par les joueurs
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = brick_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #les collisions avec le décor
        for tile in level.tiles:
            if tile.rect.colliderect(self.rect):
                if tile.rect.y < self.rect.y :
                    self.rect.bottom = tile.rect.top
                if tile.rect.y > self.rect.y :
                    self.rect.top = tile.rect.bottom
                if tile.rect.x > self.rect.x :
                    self.rect.right = tile.rect.left
                if tile.rect.x < self.rect.x :
                    self.rect.left = tile.rect.right



class Level:
    #création de la classe Level qui est utilisée pour faire la carte et poser les plateformes
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

    def run(self):
        #dessiner les plateformes
        self.tiles.update(0)
        self.tiles.draw(self.display_surface)

    def setup_level(self, layout):
        #lien entre la carte du "settings.py" et le main
        self.tiles = pygame.sprite.Group()


        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    #Ajouter un rectangle à chaque X dans la liste
                    tile = Tile((x,y),TILE_SIZE)
                    self.tiles.add(tile)






#création des boutons de jeu
start_button = buttons.Button(screen_width // 2 , screen_height // 2 -100, start_img, 1)
exit_button = buttons.Button(screen_width // 2 , screen_height // 2 +150, exit_img, 1)
player_win_button = buttons.Button(screen_width // 2, screen_height // 2, player_win , 1)
enemy_win_button = buttons.Button(screen_width // 2, screen_height // 2, enemy_win , 1)


#on créée les groupes de sprites qui sont les éléments du jeu
bullet_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()



#on créée les box
item_box = Itembox('Fire', 1000, 748)
item_box_group.add(item_box)
item_box = Itembox('Flake', 530,748)
item_box_group.add(item_box)
item_box = Itembox('Power', 770, 315)
item_box_group.add(item_box)


#création des instances des joueurs
player = player1('player', 467, 200, 1, 5, 5, 1000000, 3, 2, 0)
enemy = player1('enemy', 1100, 200, 1, 5, 5, 1000000, 3, 2, 0)

#la carte
level = Level(level_map,screen)


#boucle qui permet de vérifier si le jeu est lancé ou non
run = True
while run:

    clock.tick(FPS)
    if start_game == False :
        #dessiner le menu
        screen.fill(BG)
        #y ajouter les boutons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else :
        current_time = pygame.time.get_ticks()
        draw_background()
        #dessiner les attributs du joueur en haut a gauche et en haut a droite
        draw_text(f'Player', font, GREEN, 40, 5)

        draw_text(f'Flocons restants : ', font, GREEN, 39, 25)

        for x in range (player.flakes):
            screen.blit(flake_img, (30 + (x * 20), 45))
        draw_text(f'Enemy', font, 'red', 1455, 5)

        draw_text(f'Flocons restants : ', font, 'red', 1380, 25)
        for x in range (enemy.flakes):
            screen.blit(flake_img, (1400 + (x * 20), 45))

        draw_text(f'Feux restants : ', font, GREEN, 39, 120)
        for x in range (player.fires):
            screen.blit(fire_img, (33 + (x*20), 135))

        draw_text(f'Feux restants : ', font, 'red', 1399, 118)
        for x in range (enemy.fires):
            screen.blit(fire_img, (1460 + (x * 20), 134))

        draw_text(f'Vies :', font, GREEN, 38, 70)
        for x in range (player.lifes):
            screen.blit(heart_img, (-15 +(x * 31), 43))

        draw_text(f'Vies :', font, 'RED', 1467, 70)
        for x in range (enemy.lifes):
            screen.blit(heart_img, (1365 +(x * 31), 43))

        #on appelle les fonctions update qui vont actualiser les fonctions présentes dans le Player
        player.update()
        player.draw()

        enemy.update()
        enemy.draw()

        level.run()



        #on actualise les groupes et on les dessine à l'écran
        bullet_group.update()
        bullet_group.draw(screen)

        ball_group.update()
        ball_group.draw(screen)

        brick_group.update()
        brick_group.draw(screen)

        item_box_group.update()
        item_box_group.draw(screen)
         #Actualiser les actions du joueur
        if player.alive:
            #tirer les flocons
            if shoot:
                player.shoot()
            if shoot1:
                enemy.shoot1()
            #construire les murs de brique
            if construction and wall_constructed == False:
                player.construct()
                wall_constructed = True
            if construction1 and wall_constructed1 == False:
                enemy.construct1()
                wall_constructed1 = True

            #lancer les balles (projectiles pour le joueur)
            elif balle and ball_thrown == False and player.balls >0:
                if player.power == 10:

                    special_ball = GoldenBall(player.rect.centerx + (3 * player.rect.size[0] * player.direction), \
                                player.rect.top - 30, player.direction)
                    ball_group.add(special_ball)
                    ball_thrown = True
                    player.balls -= 1
                    player.power = 0
                else:
                    ball = Ball(player.rect.centerx + (1 * player.rect.size[0] * player.direction), \
                                player.rect.top , player.direction)
                    ball_group.add(ball)
                    #reduire le nombre de balles
                    ball_thrown = True
                    player.balls -= 1
            if player.in_air:
                player.update_action(2)#2 --> action sauter
            elif moving_left or moving_right:
                player.update_action(1)#1 --> action courir
            elif balle:
                player.update_action(4)
            else :
                player.update_action(0)
                balle = False
        else:
            #si le jeu se termine on appelle la fonction stop
            stop()
            if enemy_win_button.draw(screen):
                run = False


        if enemy.alive:
            #actions de l'ennemi
            if balle1 and ball_thrown1 == False and enemy.balls >0:
                if enemy.power == 10:
                    special_ball = GoldenBall(enemy.rect.centerx + (3 * enemy.rect.size[0] * enemy.direction), \
                                enemy.rect.top, enemy.direction)
                    ball_group.add(special_ball)
                    ball_thrown = True
                    enemy.balls -= 1
                    enemy.power = 0
                else :
                    ball = Ball(enemy.rect.centerx + (1 * enemy.rect.size[0] * enemy.direction), \
                                enemy.rect.top, enemy.direction)
                    ball_group.add(ball)
                    #reduire le nombre de balles
                    ball_thrown1 = True
                    enemy.balls -= 1
            if enemy.in_air:
                enemy.update_action(2)#2 --> action sauter
            elif moving_left1 or moving_right1:
                enemy.update_action(1)#1 --> action courir
            else :
                enemy.update_action(0)

        else:
            stop()
            if player_win_button.draw(screen):
                run = False
    #appeller les fonctions pour bouger
    player.move(moving_left, moving_right)
    enemy.move1(moving_left1, moving_right1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            #récupérer les actions sur le clavier lorsqu'on appuie dessus
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_q:
                moving_left1 = True
            if event.key == pygame.K_d:
                moving_right1 = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and player.flake_hit == True:
                shoot = False
                player.inflamed = True
                player.fires -= 1
                player.speed = 5
                player.flake_hit = False
            elif event.key == pygame.K_SPACE and player.flake_hit == False:
                shoot = True
            if event.key == pygame.K_s and enemy.flake_hit == True:
                shoot = False
                enemy.inflamed = True
                enemy.fires -= 1
                enemy.speed = 5
                enemy.flake_hit = False
            elif event.key == pygame.K_s:
                shoot1 = True
            if event.key == pygame.K_t:
                balle = True
                player.shooter = True
            if event.key == pygame.K_z:
                balle1 = True
                enemy.shooter = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_a and enemy.alive:
                enemy.jump = True
            if event.key == pygame.K_j and player.alive and player.in_air == False and player.rect.y > 50:
                construction = True
            if event.key == pygame.K_x and enemy.alive and enemy.in_air == False and enemy.rect.y > 50:
                construction1 = True
            if event.key == pygame.K_ESCAPE:
                run = False


        if event.type == pygame.KEYUP:
            # récupérer les actions sur le clavier lorsqu'on lache la touche
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_q:
                moving_left1 = False
            if event.key == pygame.K_d:
                moving_right1 = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_s:
                shoot1 = False
            if event.key == pygame.K_t:
                balle = False
                ball_thrown = False
            if event.key == pygame.K_z:
                balle1 = False
                ball_thrown1 = False
            if event.key == pygame.K_j and player.alive:
                construction = False
                wall_constructed = False
            if event.key == pygame.K_x and enemy.alive:
                construction1 = False
                wall_constructed1 = False


     #actualiser l'écran
    pygame.display.update()
pygame.quit()