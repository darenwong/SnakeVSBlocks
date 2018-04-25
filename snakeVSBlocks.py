import pygame
import random
import numpy as np
 
# --- Globals ---
# Colors
BLUE = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set the width and height of screen
display_height = 300
display_width = 300


# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create a screen
screen = pygame.display.set_mode([display_width, display_height])
 
# Set the title of the window
pygame.display.set_caption('Snake VS Blocks')

#Define Sprites and parameters
def stick(x,y, stick_width, stick_height):
    thickness = 0
    color= WHITE
    pygame.draw.rect(screen, color, (x,y,stick_width,stick_height), thickness)

def snake(x,y, snake_width, snake_height):
    thickness = 0
    color= YELLOW
    pygame.draw.rect(screen, color, (x,y,snake_width,snake_height), thickness)

def smallblock(x,y, smallblock_width, smallblock_height, point):
    thickness = 0
    color= YELLOW
    pygame.draw.rect(screen, color, (x,y,smallblock_width, smallblock_height), thickness)
    font = pygame.font.SysFont(None, 20)
    text = font.render(str(point), True, WHITE)
    textsize = text.get_rect()
    textsize.center = (smallblock_width/2+x, -smallblock_height/2+y)
    screen.blit(text,textsize)
    
def block(x,y, block_width, block_height, point):
    thickness = 0
    color= (point*5, 255-point*5, 0)
    pygame.draw.rect(screen, color, (x,y,block_width, block_height), thickness)
    font = pygame.font.SysFont(None, 50)
    text = font.render(str(point), True, BLACK)
    textsize = text.get_rect()
    textsize.center = (block_width/2+x, block_height/2+y)
    screen.blit(text,textsize)
    
def layer(xs, yb, negpoints, luck, luck2):
    block_width = 60
    block_height = 60
    if luck == 1:
        for n, i in enumerate(xs):
            if n == luck2:
                continue
            else:
                block(n*block_width ,yb[n], block_width, block_height, negpoints[n])
    else:           
        for n, i in enumerate(xs):
            block(n*block_width ,yb[n], block_width, block_height, negpoints[n])
    
def totalscore(count):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: "+ str(count), True, WHITE)
    screen.blit(text,(0,0))
    
def score(count, x, y, snake_width, snake_height):
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(count), True, BLACK)
    textsize = text.get_rect()
    textsize.center = (snake_width/2+x, snake_height/2+y)
    screen.blit(text,textsize)

def stickpara(block_width):
    stick_width = 6
    stick_height = random.randrange(150,200)
    sx = random.randrange(1,5)*block_width - stick_width/2
    luck3 = 0
    if random.randrange(0,2) == 1:
        luck3 = 1
    return stick_width, stick_height, sx, luck3
    
def layerpara(totalscor):
    xs = [0,1,2,3,4]
    negpoints=[]
    luck = 0
    if random.randrange(0,2) == 1:
        luck = 1
    luck2 = random.randrange(0,4)
    uppercap = totalscor + 15
    lowercap = int(totalscor/2)+1
    if uppercap >= 50:
        uppercap = 50
    if lowercap >= 10:
        lowercap = 10
        
    for i in range(len(xs)):
        negpoints.append(random.randrange(lowercap, uppercap))
    negpoints[luck2] = (random.randrange(1, 4))
            
    if luck == 1:
        negpoints[luck2] = 0
    return xs, negpoints, luck, luck2
    
clock = pygame.time.Clock()

#Start menu screen
def intro():
    fontsize = 30
    done = False
    
    while not done:
        
        screen.fill(BLACK)
        if fontsize > 50:
            fontsize = 30
        else: 
            fontsize += 1
        font = pygame.font.SysFont(None, fontsize)
        text = font.render("Snake VS Blocks", True, (64,255,64))
        textsize = text.get_rect()
        textsize.center = (display_width/2, display_height/3)
        screen.blit(text,textsize)
        
        font1 = pygame.font.SysFont(None, 30)
        text1 = font1.render("Press Spacebar to play", True, (255,255,0))
        textsize1 = text1.get_rect()
        textsize1.center = (display_width/2, 2*display_height/3)
        screen.blit(text1,textsize1)
        
        # Flip screen
        pygame.display.flip()
        
        # Pause
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done= True
                    game_loop()
                    
                if event.key == pygame.K_ESCAPE:
                    done = True
        
        
    
    
#Game Over screen
def gameover():
    over = False
    while not over:
                
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, (255,0,0))
        textsize = text.get_rect()
        textsize.center = (display_width/2, display_height/4)
        screen.blit(text,textsize)
        
        font1 = pygame.font.SysFont(None, 30)
        text1 = font1.render("Press Spacebar to play again", True, (255,140,0))
        textsize1 = text1.get_rect()
        textsize1.center = (display_width/2, display_height/2)
        screen.blit(text1,textsize1)
        
        # Flip screen
        pygame.display.flip()
        
        # Pause
        clock.tick(30)
        
        for event in pygame.event.get():
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    over = True
                    game_loop()
                    
                if event.key == pygame.K_ESCAPE:
                    over = True
                    intro()           
        
        


def game_loop():
    #Initialise game scoring settings
    gamespeed = 1
    scor = 10
    totalscor = 0
    point = random.randrange(1, 5)
    
    #Initialise snake parameters
    snake_width = 25
    snake_height = 25
    x = 0.5*display_width
    y = 0.8*display_height
    left_change = 0
    right_change = 0
    
    #Initialise Bigblocks parameters
    block_width = 60
    block_height = 60
    xs, negpoints, luck, luck2 = layerpara(totalscor)
    yb = np.zeros(len(xs)).astype('float64')
    
    #Initialise Smallblock parameters
    smallblock_width = 15
    smallblock_height = 15
    xb = random.randrange(0, 5)*block_width + block_width/2
    ybb = -1*random.randrange(100, 400)
    
    #Initialise stick parameters
    stick_width, stick_height, sx, luck3 = stickpara(block_width)
    

    
    gameExit = False
    while not gameExit:

        #Set up Screen boundary limits    
        if x > (display_width - snake_width):
            right_change = 0
        if x < 0:
            left_change = 0
        
        #Make sure newly spawned smallblock doesn't overlap with bigblocks   
        if (4 >= (ybb + smallblock_height) - y >= 0) and ((xb-snake_width <= x) and (x <= xb+smallblock_width)):
            scor += point
            xb = random.randrange(0, 5)*block_width + block_width/2
            ybb = -100
            point = random.randrange(1, 5)
            if block_height >= ybb - max(yb) >= -smallblock_height :
                ybb -= 100
                
        if (ybb + smallblock_height) > y and (y+snake_height > ybb):
            if ( smallblock_width > x - (xb - snake_width) > 0):
                scor += point
                xb = random.randrange(0, 5)*block_width + block_width/2
                ybb = -1*random.randrange(100, 400)
                point = random.randrange(1, 5)
                if block_height >= ybb - max(yb) >= -smallblock_height :
                    ybb -= 100
                  
            if (-smallblock_width < x - (xb + smallblock_width) < 0):
                scor += point
                xb = random.randrange(0, 5)*block_width + block_width/2
                ybb = -1*random.randrange(100, 400)
                point = random.randrange(1, 5)
                if block_height >= ybb - max(yb) >= -smallblock_height :
                    ybb -= 100
        
        
        for n, i in enumerate(xs):
            #Make sure newly spawned bigblocks doesn't overlap with smallblocks
            if (4 >= (yb[n] + block_height) - y >= 0) and ((i*block_width - snake_width + 4 <= x) and (x <= i*block_width+block_width-4)):
                if negpoints[n] > 0:        
                    negpoints[n] -= 1
                    totalscor += 1
                    scor -= 1
                    yb -= 6 +0.001*gamespeed 
                    ybb -= 6 +0.001*gamespeed 
                elif negpoints[n] == 0:
                    yb[n] = -300

            #Add boundary limits on bigblocks
            if (yb[n] + block_height) > y and (y+snake_height > yb[n]):
                if ( block_width > x - (i*block_width - snake_width) > 0):
                    right_change = 0
                if (-block_width < x - (i*block_width + block_width) < 0):
                    left_change = 0
        
        #Make sure newly spawned bigblocks doesn't overlap with smallblocks
        if max(yb) > display_height:
            xs, negpoints, luck, luck2 = layerpara(totalscor)
            stick_width, stick_height, sx, luck3 = stickpara(block_width)
            yb.fill(-100)
            if block_height >= ybb - max(yb) >= -smallblock_height :
                yb -= 100
            
        #Make sure newly spawned smallblocks doesn't overlap with bigblocks    
        if ybb > display_height:
            xb = random.randrange(0, 5)*block_width + block_width/2
            ybb = -1*random.randrange(100, 400)
            point = random.randrange(1, 5)
            if block_height >= ybb - max(yb) >= -smallblock_height :
                ybb -= 100
                
        #Adding boundary limits to sticks
        if (max(yb) + stick_height) > y and (y+snake_height > max(yb)) and luck3 ==1:
            if ( stick_width > x - (sx - snake_width) > 0):
                right_change = 0
            if (-stick_width < x - (sx + stick_width) < 0):
                left_change = 0
        if 4 >= (max(yb) + stick_height) - y >= 0 and luck3 ==1:
            if -stick_width/2 - snake_width - 3< x - sx < 3 + stick_width/2:
                yb -= 2 +0.001*gamespeed 
                ybb -= 2 +0.001*gamespeed 
            
        
        #Update sprite positions
        x += left_change + right_change
        yb += 2 +0.001*gamespeed 
        ybb += 2 +0.001*gamespeed 
        
        #Set Upper gamespeed limit
        if gamespeed < 2000:
            gamespeed += 0.5
        
        #Draw sprites and background
        screen.fill(BLACK)
        snake(x,y, snake_width, snake_height)
        score(scor, x, y, snake_width, snake_height)         
        layer(xs,list(yb), negpoints, luck, luck2)
        smallblock(xb,ybb,smallblock_width,smallblock_height, point)
        totalscore(totalscor)
        
        #Update stick parameters
        if luck3 == 1:
            stick(sx, max(yb), stick_width, stick_height)
        
        # Flip screen
        pygame.display.flip()
        
        # Pause
        clock.tick(90)
        
        #Go to gameover loop when score < 0
        if scor <= 0:
            gameExit = True
            gameover()
        
        for event in pygame.event.get():
     
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_change = -0.02*display_width
                    
                if event.key == pygame.K_RIGHT:
                    right_change = 0.02*display_width
                
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                    intro()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_change = 0
                    
                if event.key == pygame.K_RIGHT:
                    right_change = 0

        

#Start entire program by calling intro loop
intro()
pygame.quit()