from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender, Growth

from math import pi

import os.path

from pyglet import image



class Explosion(object):

    def __init__(self, x, y):

        spark_tex = image.load(os.path.join(os.path.dirname(__file__), 'images/flare3.png')).get_texture()

        sparks = ParticleGroup(
            controllers=[
                Lifetime(2),
                Movement(damping=0.93),
                Fader(fade_out_start=0, fade_out_end=1.8),
            ],

            renderer=BillboardRenderer(SpriteTexturizer(spark_tex.id)))

        spark_emitter = StaticEmitter(
            template=Particle(
                position=(x,y),
                color=(1,1,1)),
            deviation=Particle(
                position=(1,1,0),
                velocity=(300,300,0),
                age=1.5),
            size=[(1,1,0), (2,2,0), (2,2,0), (2,2,0), (3,3,0), (4,4,0)])
        spark_emitter.emit(50, sparks)

        fire_tex = image.load(os.path.join(os.path.dirname(__file__), 'images/puff.png')).get_texture()

        fire = ParticleGroup(
            controllers=[
            Lifetime(4),
            Movement(damping=0.95),
            Growth(10),
            Fader(fade_in_start=0, start_alpha=0, fade_in_end=0.5, max_alpha=0.4,
                fade_out_start=1.0, fade_out_end=1.0)
            ],
            renderer=BillboardRenderer(SpriteTexturizer(fire_tex.id)))

        fire_emitter = StaticEmitter(
            template=Particle(
                position=(x, y),
                size=(10,10,0)),
            deviation=Particle(
                position=(2,2,0),
                velocity=(70,70,0),
                size=(5,5,0),
                up=(0,0,pi*2),
                rotation=(0,0,pi*0.06),
                age=.3,),
            color=[(0.5,0,0), (0.5,0.5,0.5), (0.4,0.1,0.1), (0.85,0.3,0)],
        )
        fire_emitter.emit(200, fire)

