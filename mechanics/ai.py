import math
import pygame

class Seer(pygame.Rect):
    def __init__(self, x, y, w, h, colour, mob_t, sarr):
        pygame.Rect.__init__(self, pygame.Rect((x,y,w,h)))
        self.fov = pygame.Rect((0,0,200,200))
        sarr.append(self)
        self.sarr = sarr
        self.target = None
        self.t_last = None # last target position
        self.moving = False
        self.colour = colour
        self.mob_t = mob_t
        
    def update(self):
        self.fov.x = self.center[0] - (self.fov.w / 2)
        self.fov.y = self.center[1] - (self.fov.h / 2)
        
        for s in self.sarr:
            if s is not self:
                if self.fov.colliderect(s) and self.target == None:
                    print("you see a Seer")
                    self.target = s
                    self.t_last = s.copy()
        
        if self.target and self.mob_t != "player":
            if self.target.moving:
                d1 = distance(self, self.t_last)
                d2 = distance(self, self.target)
                
                print(d1,d2)
                if d2 < d1:
                    print("target is approaching you")
                    # x i(n) (r)ange
                    xnr = self.target.center[0] in range(self.center[0]-3, self.center[0]+3)
                    ynr = self.target.center[1] in range(self.center[1]-3, self.center[1]+3)
                    # self.x > self.target.x
                    sxgtx = self.center[0] > self.target.center[0]
                    sygty = self.center[1] > self.target.center[1]
                    
                    if not xnr:
                        if sxgtx:
                            self.move_ip(1,0)
                            print("moving east")
                        else:
                            self.move_ip(-1,0)
                            print("moving west")
                    if not ynr:
                        if sygty:
                            self.move_ip(0,1)
                            print("moving south")
                        else:
                            self.move_ip(0,-1)
                            print("moving north")
                else:
                    print("target is moving away from you")
                    if self.fov.colliderect(s):
                        self.target = None

def distance(r1, r2):
    a = abs(r1.center[0] - r2.center[0])
    b = abs(r1.center[1] - r2.center[1])
    return int(math.sqrt(a**2 + b**2))

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    sarr = []

    s1 = Seer(10,10,10,10, (0,0xff,0), "player", sarr) # green
    s2 = Seer(300,60,10,10, (0,0,0xff), "mob", sarr)

    running = True
    while running:
        clock.tick(60)
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] == 1:
            running = False
        if keys[pygame.K_RIGHT] == 1:
            s1.move_ip(1,0)
            s1.moving = True
        elif keys[pygame.K_LEFT] == 1:
            s1.move_ip(-1,0)
            s1.moving = True
        if keys[pygame.K_DOWN] == 1:
            s1.move_ip(0,1)
            s1.moving = True
        elif keys[pygame.K_UP] == 1:
            s1.move_ip(0,-1)
            s1.moving = True
                
        s1.update()
        s2.update()
        
        for s in sarr:
            pygame.draw.rect(display, s.colour, s)
            pygame.draw.rect(display, (0xff,0,0), s.fov, 1)
            
        pygame.display.flip()
        display.fill((0,0,0))
        s1.moving = False
