"""
Author:Alex Su

Date:2017.5.15

Description: Thunder game, use WASD or up down left right arrow to control the
plane. It will get harder as your score goes higher. Each plane shot down will
give you 1000 points, each plane hit or missed you will lose one life. There are
shields dropped randomly on the screen which will gives you one extra life.
"""
# I - IMPORT AND INITIALIZE
import pygame, pySprites, time, random
pygame.init()
pygame.mixer.init()

def main():
    '''This function defines the 'mainline logic' for our pyPong game.'''
    # DISPLAY
    pygame.display.set_caption("Thunder")
    screen = pygame.display.set_mode((480, 800))
    
    # ENTITIES
    # Background initialization
    background = pygame.image.load('resources/image/background.png').convert()
    screen.blit(background, (0, 0))
    #Images loading
    game_over = pygame.image.load('resources/image/gameover.png').convert()
    plane_img =pygame.image.load('resources/image/shoot.png')    
    # Config rect for bullets
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img.subsurface(bullet_rect)
    # Player Config
    player_rect = []
    # Player Sprite area
    player_rect.append(pygame.Rect(0, 99, 102, 126))  
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    # Player explosion sprite area
    player_rect.append(pygame.Rect(165, 234, 102, 126))
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    # Sprite for player plane
    player = pySprites.Player(plane_img, player_rect, player_pos,screen)    
    # Config Rect for enemy plane
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    # Sprite for enemy plane
    enemies1 = pygame.sprite.Group()
    shield_pos = [random.randint(0, background.get_width() - enemy1_rect.width), 0]
    shield = pySprites.Shield(shield_pos)
    # Save down plane for explosion
    enemies_down = pygame.sprite.Group()
    #bullets sprites
    bullets = pygame.sprite.Group()
    # Sprite for score keeper
    score_keeper = pySprites.ScoreKeeper(screen)
    allSprites = pygame.sprite.OrderedUpdates(enemies1,enemies_down,shield,score_keeper,bullets,player)
    
    #initialize setting
    shoot_frequency = 25
    enemy_frequency = 50
    #keep track of frame and current score
    frame=0
    score = 0    
    
    # Background Music and Sound Effects
    bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
    enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
    game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
    bullet_sound.set_volume(0.3)
    enemy1_down_sound.set_volume(0.3)
    game_over_sound.set_volume(0.3)
    pygame.mixer.music.load('resources/sound/game_music.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)

    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
 
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
     
        # TIME, 60 FPS for smoother play
        clock.tick(60)
     
        # EVENT HANDLING: Player uses keyboard, left arrow/A for left, right 
        #arrow/D for right, up/W for up, down/S for down

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        if not player.is_hit:
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
                player.moveUp()
            if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
                player.moveDown()
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                player.moveLeft()
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                player.moveRight()                    
        
        frame += 1
        score=score_keeper.get_score()            
        # Fire bullets 
        if frame % shoot_frequency == 0:
            bullet_sound.play()
            bullet = pySprites.Bullet(bullet_img,player.rect.midtop)
            bullets.add(bullet)            
        
        #if score if more than 10000 increase the speed
        #more than 20000 increase speed again and increase shoot frequency,
        #more than 30000 increase spped again and increase shoot frequency again
        if score >10000:
            enemy_frequency=40
            shoot_frequency=20
        if score >20000:
            enemy_frequency=25
            shoot_frequency=15
        if score >30000:
            enemy_frequency=20
            shoot_frequency=13 
        #generate shield   
        if frame % 1000 == 0:
            shield.reset()
        #generate enemy plane
        if frame % enemy_frequency == 0:
            enemy1_pos = [random.randint(0, background.get_width() - enemy1_rect.width), 0]
            enemy1 = pySprites.Enemy(enemy1_pos)
            enemies1.add(enemy1)
                    
        #detect if bullet is out of screen, if it is, remove the bullet
        for bullet in bullets:
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
        
        for enemy in enemies1:
            #detect if the player is hit or out of screen, if it is, deduct one life and removes the plane
            if pygame.sprite.collide_circle(enemy, player) or enemy.rect.top > background.get_height():
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                score_keeper.deduct_life()
                player.is_hit=1
        if score_keeper.dead():
            player.is_hit=1
            pygame.mixer.music.fadeout(2000)
            if player.finish==1:
                keepGoing=False

        if shield.rect.colliderect(player):
            score_keeper.add_life() 
            shield.hit=1
        # detect if bullet hits the plane, if so then plus 1000 score and removes the plane
        enemies1_down = pygame.sprite.groupcollide(enemies1, bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)
            score_keeper.player_scored(1000)            

        for enemy_down in enemies_down:
            if enemy_down.index == 0:
                enemy1_down_sound.play()
                enemy_down.enemy_down()
            if enemy_down.index >= len(enemy_down.images):
                enemies_down.remove(enemy_down)
                continue
        allSprites = pygame.sprite.OrderedUpdates(enemies1,enemies_down,shield,score_keeper,bullets,player)
        # REFRESH SCREEN
        screen.blit(background, (0, 0))
        allSprites.clear(screen,background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
    
    # Display "Game Over" graphic and unhide the mouse pointer
    game_over_sound.play()
    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score_keeper.get_score()), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)    
    pygame.display.flip()
    pygame.mouse.set_visible(True)
    time.sleep(5)
    pygame.quit()
# Call the main function
main()