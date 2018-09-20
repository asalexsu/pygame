"""
Author:Alex Su

Date:2017.5.15

Description: Thunder game Sprites
"""

import pygame


class Bullet(pygame.sprite.Sprite):
    '''This class contains bullet with speed of 10.'''
    def __init__(self, bullet_img, init_pos):
        """initial method """        
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.__speed = 10

    def update(self):
        """This method will be called automatically to change 
        the current position of the bullet."""        
        self.rect.top -= self.__speed
        

class Player(pygame.sprite.Sprite):
    '''This class contains player plane.'''
    def __init__(self, plane_img, player_rect, init_pos,screen):
        """initial method """    
        pygame.sprite.Sprite.__init__(self)
        self.__screen=screen
        # List for player sprite images
        self.images = []                                 
        for i in range(len(player_rect)):
            self.images.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.index=0
        self.image= self.images[self.index]
        #initialize the image
        self.rect = player_rect[0]                      
        self.rect.topleft = init_pos                    
        #initialize the speed of the plane
        self.speed = 8 
        #sprite for all the bullets         
        self.img_index = 0 
        self.frame=0
        self.finish=0
        # If player is hit        
        self.is_hit = False                             
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        """moves down """  
        if self.rect.top >= self.__screen.get_height() - self.rect.height:
            self.rect.top = self.__screen.get_height() - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        """moves left """  
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        """moves right """  
        if self.rect.left >= self.__screen.get_width() - self.rect.width:
            self.rect.left = self.__screen.get_width() - self.rect.width
        else:
            self.rect.left += self.speed
    def update(self):
        """This method will be called automatically to change 
                the current position of the plane."""                
        self.frame+=1
        if self.frame%5==0:
            if not self.is_hit:
                self.index +=1
                if self.index > 1:
                    self.index=0
                self.image=self.images[self.index]
            else:
                self.index += 1
                if self.index < len(self.images):
                    self.image=self.images[self.index]
                else:
                    self.is_hit=0
                    self.finish=1
class Enemy(pygame.sprite.Sprite):
    '''This class contains enemy plane.'''
    def __init__(self, init_pos):
        """initial method """    
        pygame.sprite.Sprite.__init__(self)
        self.images = []                                 # List for player sprite images
        for i in range(6):
            self.images.append(pygame.image.load('resources/image/bad'+str(i)+'.png'))
        self.index=0
        self.image= self.images[self.index]        
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.down_finish = 0
        self.down=0
        self.frame=0
    def enemy_down(self):
        self.down=1
    def update(self):
        """This method will be called automatically to change 
                        the current position of the plane."""             
        self.rect.top += self.speed
        self.frame+=1
        if self.frame%4==0:        
            if self.down:
                self.index += 1
                if self.index < len(self.images):
                    self.image = self.images[self.index]
                else:
                    self.down_finish=1
class Shield(pygame.sprite.Sprite):
    '''This class contains shield.'''
    def __init__(self, init_pos):
        """initial method """    
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/image/shield_gold.png')     
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.init_pos=init_pos
        self.speed = 3
        self.hit=0
    def reset(self):
        """reset to top """ 
        self.rect.topleft = self.init_pos
    def update(self):
        """This method will be called automatically to change 
                        the current position of the shield."""             
        self.rect.top += self.speed
        if self.hit==1:
            self.rect.topleft = [500,500]
            self.hit=0
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self,screen):
        '''This initializer loads the system font "Spaceage", and
        sets the starting score to 0, life to 3'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.__screen=screen
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("spaceage.ttf", 30)
        self.__player_score = 0
        self.__player_life = 3
        
    def player_scored(self, points):
        '''This method adds points to the score for the player'''
        self.__player_score += points
    def get_score(self) :
        return int(self.__player_score)
    def deduct_life(self):
        '''This method deducts one life for the player'''
        self.__player_life -= 1
    def add_life(self):
        '''This method adds one life for the player'''
        self.__player_life += 1        
    def dead(self):
        '''If the player is dead, it will return 1, else will return 0'''
        if self.__player_life == 0:
            return 1
        else:
            return 0
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        message = "Score: %d Live(s): %d" %\
                (self.__player_score, self.__player_life)
        self.image = self.__font.render(message, 1, (128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = (self.__screen.get_width()/2, 10)
        