import sys, pygame
import RSVM
import random
import sys
pygame.init()


try:
   import psyco
   psyco.full()
   print "Psyco loaded."
except ImportError:
   print "Psyco not found."



size = width, height = 640, 480
bg = 0, 0, 0

d = ""
f = ""
xx = 0
yy = 0
angle = 0

f = sys.argv[1]
xx = float(sys.argv[2])
yy = float(sys.argv[3])
angle = float(sys.argv[4])

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
player = pygame.image.load("player.png")

code = RSVM.loadFCode(f)
R = RSVM.RSVM(code)
      
R.spawnThread(0, xx, yy, angle, None)
#R.spawnThread(0, xx + 10, yy, 0, 0)

pygame.time.set_timer(pygame.USEREVENT, 30)

px = width / 2
py = height - 20
mspeed = 5

showlines = False
kf1down = False

linecolor = pygame.Color(0, 200, 0)

while True:
    go = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.USEREVENT: go = True

    if go:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] == True:
            print len(R.threads)
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_UP] == True:
            py -= mspeed
        if keys[pygame.K_DOWN] == True:
            py += mspeed
        if keys[pygame.K_LEFT] == True:
            px -= mspeed
        if keys[pygame.K_RIGHT] == True:
            px += mspeed
        if keys[pygame.K_F1] == True:
            if not kf1down:
               showlines = not showlines
               kf1down = True
        else:
            kf1down = False
        
        R.setPlayerPosition(px, py)
        R.run()
        threads = R.getThreadIDs()
        
        screen.fill(bg)
        
        screen.blit(player, pygame.Rect(px-17, py-17, 0, 0))
        
        for x in threads:
           screen.blit(ball, pygame.Rect(R.getState(x, "__x")-4, R.getState(x,"__y")-4, 0, 0))
        
        if showlines:
           for x in threads:
              pid = R.getThreadParent(x)
              if pid != -1:
                 p1 = (R.getState(x, "__x"), R.getState(x, "__y"))
                 p2 = (R.getState(pid, "__x"), R.getState(pid, "__y"))
                 pygame.draw.line(screen, linecolor, p1, p2)
        
        pygame.display.flip()
        

