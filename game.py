from player import Player
from lepton import default_system
from world import World

import rabbyt
import os
from pyglet import clock, image, app, resource
from pyglet.gl import *
import zmq
import sys

global sub_socket

#---------------------------------------
#OPEN GL STUFF THAT HARDLY MAKES SENSE
#---------------------------------------
glEnable(GL_BLEND)
glShadeModel(GL_SMOOTH)
glBlendFunc(GL_SRC_ALPHA,GL_ONE)
glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
glDisable(GL_DEPTH_TEST)

#----------------------------------
# CREATE THE PLAYER THEN THE WORLD
#----------------------------------
tank = Player('PhantomXC', 'tanktop', 'tankbot', 100, 100)
world = World()
world.connectServer()
world.selectLevel('city1')

world.addPlayer(tank, main=True)

#---------------------------------------------------
# RABBYT THAT NEEDS TO HAPPEN AFTER WORLD GENERATION
#---------------------------------------------------
rabbyt.set_default_attribs()
rabbyt.data_directory = os.path.dirname(__file__)


#------
# CRAP that needs to move
#------
fps_display = clock.ClockDisplay()

#---------------------------------
# WINDOW EVENTS. MOSTLY MOUSE
#---------------------------------
@world.window.event
def on_draw():
    world.window.clear()

    #render your bg here if you want to see the shapes
    #world.bgimage.blit(0,0)
    
    for obj in world.map_objects:
        obj.render()
    
    world.bgimage.blit(0,0)
    
    for obj in world.player_objects:
        obj.render()

    world.displayScore()

    glLoadIdentity()
    default_system.draw()
    fps_display.draw()

if __name__=='__main__':
    clock.schedule(world.gameUpdate)
    app.run()


