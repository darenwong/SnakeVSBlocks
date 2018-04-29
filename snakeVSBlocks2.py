import pygame
import random
import numpy as np
 
# --- Globals ---
# Colors
BLUE = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (200,200,0)


# Set the width and height of screen
display_height = 480
display_width = 300


# Call this function so the Pygame library can initialize itself
pygame.init()

#Make mouse invisible
pygame.mouse.set_visible(True)

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
    if point < 16:
        color = (0, 255, 255-point*16)
    elif 16 <= point < 32:
        color = ((point-16)*16, 255, 0)
    elif point >= 32:
        color= (255, 255-(point-32)*15, 0)
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

def layer2(xs, yb, negpoints, lucknum):
    block_width = 60
    block_height = 60
    
    for n in range(5):
        if n in lucknum:
            continue
        else:
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
    stick_height = random.randrange(1,5)*block_width
    sx = random.randrange(1,5)*block_width - stick_width/2
    luck3 = 1
    if random.randrange(0,3) >= 1:
        luck3 = 1
    return stick_width, stick_height, sx, luck3 

def stickcoll(sx, sy, stick_height, sx1, sy1, stick_height1, sx2, sy2, stick_height2, sx3, sy3, stick_height3):
    if sx == sx1 or sx == sx2 or sx == sx3 :
        a = [57, 117, 177, 237]
        a.remove(sx1)
        if sx2 in a:
            a.remove(sx2)
        if sx3 in a:
            a.remove(sx3)
        sx = random.choice(a)
    return sx
   
def smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2):
    if xb == xb1 and ybb == ybb1:
         a = [30,90,150,210,270]
         a.remove(xb1)
         if xb2 in a:
             a.remove(xb2)
         xb = random.choice(a)

    if xb == xb2 and ybb == ybb2:
         a = [30,90,150,210,270]
         a.remove(xb1)
         if xb2 in a:
             a.remove(xb2)
         xb = random.choice(a)

    return xb
    
def layerpara2(totalscor, layertype):
    xs = [0,1,2,3,4]
    negpoints=[]
    lucknum = []
    uppercap = totalscor + 15
    lowercap = int(totalscor/2)+1
    if uppercap >= 50:
        uppercap = 50
    if lowercap >= 10:
        lowercap = 10
        
    for i in range(len(xs)):
        if random.randrange(0, 10) >= 7:
            negpoints.append(random.randrange(lowercap, uppercap))
        else:
            negpoints.append(random.randrange(1, 5))
            
    if layertype ==1:
        for i in range(len(xs)):
            luck = random.randrange(0,5)
            lucknum.append(luck)
            negpoints[luck] = 0
    
    elif layertype == 0 and random.randrange(0,2) == 0:
        luck = random.randrange(0,5)
        lucknum.append(luck)
        negpoints[luck] = 0
            
    return xs, negpoints, lucknum

def move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed,step, multiplier):
    yb -= step + multiplier*gamespeed
    yb1 -= step + multiplier*gamespeed
    yb2 -= step + multiplier*gamespeed 
    yb3 -= step + multiplier*gamespeed 
    yb4 -= step + multiplier*gamespeed
    yb5 -= step + multiplier*gamespeed
    ybb -= step + multiplier*gamespeed
    ybb1 -= step + multiplier*gamespeed
    ybb2 -= step + multiplier*gamespeed
    sy -= step + multiplier*gamespeed
    sy1 -= step + multiplier*gamespeed
    sy2 -= step + multiplier*gamespeed
    sy3 -= step + multiplier*gamespeed
    return yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3
    
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(None, 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    

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
        
        button_width = 150
        button_height = 50
            
        msg,x,y,w,h,ic,ac,action = "Play",(display_width-button_width)/2,(display_height*2/3-button_height/2),button_width,button_height,BRIGHT_YELLOW,YELLOW,game_loop
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
    
            if click[0] == 1 and action != None:
                action()
                done = True
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))
       
        smallText = pygame.font.SysFont(None, 30)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)
            
        # Flip screen
        pygame.display.flip()
        
        # Pause
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done= True
                    game_loop()
                    
                if event.key == (pygame.K_ESCAPE):
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
        
        button_width = 150
        button_height = 50
            
        msg,x,y,w,h,ic,ac,action = "Play Again",(display_width-button_width)/2,(0.5*display_height-button_height/2),button_width,button_height,(200,200,0),(255,255,0),game_loop
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
    
            if click[0] == 1 and action != None:
                action()
                over = True
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))
    
        smallText = pygame.font.SysFont(None, 30)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)
        
        if over == True:
            break
        
        # Flip screen
        pygame.display.flip()
        
        # Pause
        clock.tick(30)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                over = True
                intro()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    over = True
                    game_loop()
                    
                if event.key == (pygame.K_ESCAPE) :
                    over = True
                    intro()


def game_loop():
    #Initialise game scoring settings
    gamespeed = 0
    scor = 10
    totalscor = 0
    point = random.randrange(1, 4)
    point1 = random.randrange(1, 4)
    point2 = random.randrange(1, 4)
    
    #Initialise snake parameters
    snake_width = 25
    snake_height = 25
    x = 0.5*display_width
    y = 0.7*display_height
    
    
    #Initialise Bigblocks parameters
    block_width = 60
    block_height = 60
    stickupperlim = 4*block_height
    xs, negpoints, lucknum = layerpara2(totalscor, 0)
    yb = -stickupperlim + np.zeros(len(xs)).astype('float64')
    xs1, negpoints1, lucknum1 = layerpara2(totalscor,1)
    yb1 = -stickupperlim + np.zeros(len(xs1)).astype('float64') - display_height/4
    xs2, negpoints2, lucknum2 = layerpara2(totalscor,1)
    yb2 = -stickupperlim + np.zeros(len(xs2)).astype('float64') - display_height*2/4
    xs3, negpoints3, lucknum3 = layerpara2(totalscor, 0)
    yb3 = -stickupperlim + np.zeros(len(xs3)).astype('float64') - display_height*3/4
    xs4, negpoints4, lucknum4 = layerpara2(totalscor, 1)
    yb4 = -stickupperlim + np.zeros(len(xs4)).astype('float64') - display_height
    xs5, negpoints5, lucknum5 = layerpara2(totalscor, 1)
    yb5 = -stickupperlim + np.zeros(len(xs5)).astype('float64') - display_height*5/4

    
    #Initialise Smallblock parameters
    smallblock_width = 15
    smallblock_height = 15
    xb = random.randrange(0, 5)*block_width + block_width/2
    ybb = max(yb) - block_height/2
    xb1 = random.randrange(0, 5)*block_width + block_width/2
    ybb1 = max(yb1) - block_height/2
    xb2 = random.randrange(0, 5)*block_width + block_width/2
    ybb2 = max(yb1) - block_height/2
    xb = smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2)
    xb1 = smallblockcoll(xb1, ybb1, xb, ybb, xb2, ybb2)
    xb2 = smallblockcoll(xb2, ybb2, xb, ybb, xb1, ybb1)
    
    
    #Initialise stick parameters
    stick_width, stick_height, sx, luck3 = stickpara(block_width)
    stick_width1, stick_height1, sx1, luck31 = stickpara(block_width)
    stick_width2, stick_height2, sx2, luck32 = stickpara(block_width)
    stick_width3, stick_height3, sx3, luck33 = stickpara(block_width)
    sy =  -stick_height - random.randrange(0,3)*block_height 
    sy1 = -stick_height1 - random.randrange(0,3)*block_height  
    sy2 = -stick_height2 - random.randrange(0,3)*block_height - display_height/2
    sy3 = -stick_height3 - random.randrange(0,3)*block_height - display_height
    
    gameExit = False
    while not gameExit:
#        print(xb1, xb2)
#        print(sx, sx1, sx2, sx3, sy, sy1, sy2, sy3, stick_height, stick_height1, stick_height2, stick_height3)
        xt = pygame.mouse.get_pos()[0]
        #Set up Screen boundary limits    
        if xt > (display_width - snake_width):
            xt = (display_width - snake_width)
        if xt < 0:
            xt = 0

            
        if max(yb) > y - block_height:            
            for n, i in enumerate(xs):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints[n] > 0:        
                        negpoints[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints[n] == 0:
                        yb[n] = -display_height
                        lucknum.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb) + block_height) - 2 > y and (y+snake_height > max(yb)):
                        if n-1 not in lucknum and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb) > display_height:
                xs, negpoints, lucknum = layerpara2(totalscor, 0)
                yb.fill(-stickupperlim)
#                
        if max(yb1) > y - block_height:            
            for n, i in enumerate(xs1):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb1[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints1[n] > 0:        
                        negpoints1[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints1[n] == 0:
                        yb1[n] = -display_height
                        lucknum1.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb1) + block_height) - 2 > y and (y+snake_height > max(yb1)):
                        if n-1 not in lucknum1 and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum1 and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb1) > display_height:
                xs1, negpoints1, lucknum1 = layerpara2(totalscor, 1)
                yb1.fill(-stickupperlim)
        
        if max(yb2) > y - block_height:            
            for n, i in enumerate(xs2):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb2[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints2[n] > 0:        
                        negpoints2[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints2[n] == 0:
                        yb2[n] = -display_height
                        lucknum2.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb2) + block_height) - 2 > y and (y+snake_height > max(yb2)):
                        if n-1 not in lucknum2 and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum2 and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb2) > display_height:
                xs2, negpoints2, lucknum2 = layerpara2(totalscor, 1)
                yb2.fill(-stickupperlim)

        if max(yb3) > y - block_height:            
            for n, i in enumerate(xs3):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb3[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints3[n] > 0:        
                        negpoints3[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints3[n] == 0:
                        yb3[n] = -display_height
                        lucknum3.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb3) + block_height) - 2 > y and (y+snake_height > max(yb3)):
                        if n-1 not in lucknum3 and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum3 and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb3) > display_height:
                xs3, negpoints3, lucknum3 = layerpara2(totalscor, 0)
                yb3.fill(-stickupperlim)

        if max(yb4) > y - block_height:            
            for n, i in enumerate(xs4):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb4[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints4[n] > 0:        
                        negpoints4[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints4[n] == 0:
                        yb4[n] = -display_height
                        lucknum4.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb4) + block_height) - 2 > y and (y+snake_height > max(yb4)):
                        if n-1 not in lucknum4 and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum4 and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb4) > display_height:
                xs4, negpoints4, lucknum4 = layerpara2(totalscor, 1)
                yb4.fill(-stickupperlim)
        
        if max(yb5) > y - block_height:            
            for n, i in enumerate(xs5):
                #Make sure newly spawned bigblocks doesn't overlap with smallblocks
                if (4 >= (yb5[n] + block_height) - y >= 0) and ((i*block_width - snake_width < x) and (x <= (i+1)*block_width)):
                    if negpoints5[n] > 0:        
                        negpoints5[n] -= 1
                        totalscor += 1
                        scor -= 1
                        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 6, 0.003)
                    elif negpoints5[n] == 0:
                        yb5[n] = -display_height
                        lucknum5.append(n)
                        
                if i*block_width <= x < (i+1)*block_width:
                    if (max(yb5) + block_height) - 2 > y and (y+snake_height > max(yb5)):
                        if n-1 not in lucknum5 and xt < (i*block_width):
                            xt = (i*block_width)
                        if n+1 not in lucknum5 and xt > ((i+1)*block_width - snake_width):                         
                            xt = ((i+1)*block_width - snake_width)
        
            if max(yb5) > display_height:
                xs5, negpoints5, lucknum5 = layerpara2(totalscor, 1)
                yb5.fill(-stickupperlim)
        

        toplayer = min(max(yb),max(yb1),max(yb2),max(yb3),max(yb4),max(yb5))
        
        #Adding boundary limits to sticks
        if (sy + stick_height) > y and (y+snake_height > sy) and luck3 ==1:
            if x <= (sx - snake_width) and (xt > (sx - snake_width)):
                xt = (sx - snake_width)
            if x >= (sx + stick_width) and (xt < (sx + stick_width)):
                xt = (sx + stick_width)
        if 4 >= (sy + stick_height) - y >= 0 and luck3 ==1:
            if -stick_width/2 - snake_width - 1< x - sx < 3 + stick_width/2:
                yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 2, 0.001)
        if sy > display_height:
            stick_width, stick_height, sx, luck3 = stickpara(block_width)       
            sy = -stick_height + random.randrange(0,3)*block_height + toplayer
            sx = stickcoll(sx, sy, stick_height, sx1, sy1, stick_height1, sx2, sy2, stick_height2, sx3, sy3, stick_height3)
           
    
        if (sy1 + stick_height1) > y and (y+snake_height > sy1) and luck31 ==1:
            if x <= (sx1 - snake_width) and (xt > (sx1 - snake_width)):
                xt = (sx1 - snake_width)
            if x >= (sx1 + stick_width1) and (xt < (sx1 + stick_width1)):
                xt = (sx1 + stick_width1)
        if 4 >= (sy1 + stick_height1) - y >= 0 and luck31 ==1:
            if -stick_width1/2 - snake_width - 1< x - sx1 < 3 + stick_width1/2:
                yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 2, 0.001)
        if sy1 > display_height:
            stick_width1, stick_height1, sx1, luck31 = stickpara(block_width)       
            sy1 = -stick_height1 + random.randrange(0,3)*block_height + toplayer
            sx1 = stickcoll(sx1, sy1, stick_height1, sx, sy, stick_height, sx2, sy2, stick_height2, sx3, sy3, stick_height3)
              
    
        if (sy2 + stick_height2) > y and (y+snake_height > sy2) and luck32 ==1:
            if x <= (sx2 - snake_width) and (xt > (sx2 - snake_width)):
                xt = (sx2 - snake_width)
            if x >= (sx2 + stick_width2) and (xt < (sx2 + stick_width2)):
                xt = (sx2 + stick_width2)
        if 4 >= (sy2 + stick_height2) - y >= 0 and luck32 ==1:
            if -stick_width2/2 - snake_width - 1< x - sx2 < 3 + stick_width2/2:
                yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 2, 0.001)
        if sy2 > display_height:
            stick_width2, stick_height2, sx2, luck32 = stickpara(block_width)       
            sy2 = -stick_height2 + random.randrange(0,3)*block_height + toplayer
            sx2 = stickcoll(sx2, sy2, stick_height2, sx1, sy1, stick_height1, sx, sy, stick_height, sx3, sy3, stick_height3)
         
       
        if (sy3 + stick_height3) > y and (y+snake_height > sy3) and luck33 ==1:
            if x <= (sx3 - snake_width) and (xt > (sx3 - snake_width)):
                xt = (sx3 - snake_width)
            if x >= (sx3 + stick_width3) and (xt < (sx3 + stick_width3)):
                xt = (sx3 + stick_width3)
        if 4 >= (sy3 + stick_height3) - y >= 0 and luck33 ==1:
            if -stick_width3/2 - snake_width - 1< x - sx3 < 3 + stick_width3/2:
                yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, 2, 0.001)
        if sy3 > display_height:
            stick_width3, stick_height3, sx3, luck33 = stickpara(block_width)       
            sy3 = -stick_height3 + random.randrange(0,3)*block_height + toplayer
            sx3 = stickcoll(sx3, sy3, stick_height3, sx1, sy1, stick_height1, sx2, sy2, stick_height2, sx, sy, stick_height)
             
        
            
        #Make sure newly spawned smallblock doesn't overlap with bigblocks
        point_freq = -1
        if ybb > y - block_height:
            if (smallblock_height >= (ybb + smallblock_height) - y >= 0) and ((xb-snake_width <= x) and (x <= xb+smallblock_width)):
                scor += point
                xb = random.randrange(0, 5)*block_width + block_width/2
                ybb = toplayer + point_freq*block_height/2
                xb = smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2)
                point = random.randrange(1, 4)
                    
            if (ybb + smallblock_height) > y and (y+snake_height > ybb):
                if ( smallblock_width > x - (xb - snake_width) > 0):
                    scor += point
                    xb = random.randrange(0, 5)*block_width + block_width/2
                    ybb = toplayer + point_freq*block_height/2
                    xb = smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2)
                if (-smallblock_width < x - (xb + smallblock_width) < 0):
                    scor += point
                    xb = random.randrange(0, 5)*block_width + block_width/2
                    ybb = toplayer + point_freq*block_height/2
                    xb = smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2)
            if ybb > display_height:
                xb = random.randrange(0, 5)*block_width + block_width/2
                ybb = toplayer + point_freq*block_height/2
                xb = smallblockcoll(xb, ybb, xb1, ybb1, xb2, ybb2)
            
        if ybb1 > y - block_height:
            if (smallblock_height >= (ybb1 + smallblock_height) - y >= 0) and ((xb1-snake_width <= x) and (x <= xb1+smallblock_width)):
                scor += point1
                xb1 = random.randrange(0, 5)*block_width + block_width/2
                ybb1 = toplayer + point_freq*block_height/2
                xb1 = smallblockcoll(xb1, ybb1, xb, ybb, xb2, ybb2)
                point1 = random.randrange(1, 4)
                
            if (ybb1 + smallblock_height) > y and (y+snake_height > ybb1):
                if ( smallblock_width > x - (xb1 - snake_width) > 0):
                    scor += point1
                    xb1 = random.randrange(0, 5)*block_width + block_width/2
                    ybb1 = toplayer + point_freq*block_height/2
                    xb1 = smallblockcoll(xb1, ybb1, xb, ybb, xb2, ybb2)
                if (-smallblock_width < x - (xb1 + smallblock_width) < 0):
                    scor += point1
                    xb1 = random.randrange(0, 5)*block_width + block_width/2
                    ybb1 = toplayer + point_freq*block_height/2
                    xb1 = smallblockcoll(xb1, ybb1, xb, ybb, xb2, ybb2)
            if ybb1 > display_height:
                xb1 = random.randrange(0, 5)*block_width + block_width/2
                ybb1 = toplayer + point_freq*block_height/2
                xb1 = smallblockcoll(xb1, ybb1, xb, ybb, xb2, ybb2)
                            
        if ybb2 > y - block_height:
            if (smallblock_height >= (ybb2 + smallblock_height) - y >= 0) and ((xb2-snake_width <= x) and (x <= xb2+smallblock_width)):
                scor += point2
                xb2 = random.randrange(0, 5)*block_width + block_width/2
                ybb2 = toplayer + point_freq*block_height/2
                xb2 = smallblockcoll(xb2, ybb2, xb, ybb, xb1, ybb1)
                point2 = random.randrange(1, 4)
                
            if (ybb2 + smallblock_height) > y and (y+snake_height > ybb2):
                if ( smallblock_width > x - (xb2 - snake_width) > 0):
                    scor += point2
                    xb2 = random.randrange(0, 5)*block_width + block_width/2
                    ybb2 = toplayer + point_freq*block_height/2
                    xb2 = smallblockcoll(xb2, ybb2, xb, ybb, xb1, ybb1)
                if (-smallblock_width < x - (xb2 + smallblock_width) < 0):
                    scor += point2
                    xb2 = random.randrange(0, 5)*block_width + block_width/2
                    ybb2 = toplayer + point_freq*block_height/2
                    xb2 = smallblockcoll(xb2, ybb2, xb, ybb, xb1, ybb1)
            if ybb2 > display_height:
                xb2 = random.randrange(0, 5)*block_width + block_width/2
                ybb2 = toplayer + point_freq*block_height/2
                xb2 = smallblockcoll(xb2, ybb2, xb, ybb, xb1, ybb1)
    
        if xt > x:
            x += 0.2*abs(x - xt)
        if xt < x:
            x -= 0.2*abs(x - xt)
   
        gamespeed += 0.5
        if gamespeed > 2000:
            gamespeed = 2000
        
        yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3 = move(yb, yb1, yb2, yb3, yb4, yb5, ybb, ybb1, ybb2, sy, sy1, sy2, sy3, gamespeed, -2, -0.001)
                    
                    
        print('fps = ' + str(clock.get_fps()))
        screen.fill(BLACK)
        snake(x,y, snake_width, snake_height)
        layer2(xs,list(yb), negpoints, lucknum)
        layer2(xs1,list(yb1), negpoints1, lucknum1)
        layer2(xs2,list(yb2), negpoints2, lucknum2)
        layer2(xs3,list(yb3), negpoints3, lucknum3)
        layer2(xs4,list(yb4), negpoints4, lucknum4)
        layer2(xs5,list(yb5), negpoints5, lucknum5)
        if scor >= 0:    
            score(scor, x, y, snake_width, snake_height)
        else:
            score(0, x, y, snake_width, snake_height)
        smallblock(xb,ybb,smallblock_width,smallblock_height, point)
        smallblock(xb1,ybb1,smallblock_width,smallblock_height, point1)
        smallblock(xb2,ybb2,smallblock_width,smallblock_height, point2)
        totalscore(totalscor)
        if luck3 == 1:
            stick(sx, sy, stick_width, stick_height)
        if luck31 == 1:
            stick(sx1, sy1, stick_width1, stick_height1)
        if luck32 == 1:
            stick(sx2, sy2, stick_width2, stick_height2)
        if luck33 == 1:
            stick(sx3, sy3, stick_width3, stick_height3)
     
        
#        Go to gameover loop when score < 0
        if scor < 0:
            gameExit = True
            gameover()
        
        # Flip screen
        pygame.display.update(0,0,display_width, display_height)
        
        clock.tick(60)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                    intro()
            
        
#Start entire program by calling intro loop
intro()
pygame.quit()
