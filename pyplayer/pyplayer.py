import pygame
from pyomxplayer import OMXPlayer
from time import time, sleep

def setup():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastChangeTime, state, startTime

    omx = OMXPlayer('./data/vids/MVI_0702.mov')
    #omx.toggle_pause()

    pygame.init()
    screen = pygame.display.set_mode((0, 0), (pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE))
    pygame.display.set_caption('LaSonora')
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    font = pygame.font.Font("./data/arial.ttf", 800)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    mSurface = font.render("La Sonora Telematica ", 1, (200,200,200), (0,0,0))
    mSurfaceRect = mSurface.get_rect()
    scale = min(float(background.get_width())/mSurfaceRect.width, float(mSurfaceRect.width)/background.get_width())
    mSurface = pygame.transform.scale(mSurface,(int(scale*mSurfaceRect.width),int(scale*mSurfaceRect.height)))
    mSurfaceRect = mSurface.get_rect(centerx=background.get_width()/2,
                                     centery=background.get_height()/2)

    lastChangeTime = time()
    state = 0
    startTime = time()

def loop():
    global omx
    global background, screen, font, mSurface, mSurfaceRect
    global lastChangeTime, state, startTime

    if(time() - lastChangeTime > 2):
        lastChangeTime = time()
        background.fill((0,0,0))
        if(state is 0):
            state = 1
            background.blit(mSurface, mSurfaceRect)
        else:
            state = 0

        screen.blit(background, (0,0))
        pygame.display.flip()
    if((time() - startTime > 10) and omx and (omx.paused)):
        omx.toggle_pause()
    if((time() - startTime > 30) and (not omx is None)):
        omx.stop()
        omx = None

if __name__=="__main__":
    setup()
    try:
        while(True):
            loopStart = time()
            loop()
            loopTime = time()-loopStart
            if (loopTime < 0.016):
                sleep(0.016 - loopTime)
        exit(0)
    except KeyboardInterrupt:
        omx.stop()
        exit(0)
