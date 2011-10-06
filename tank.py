import rabbyt

from pyglet import clock
from math import cos, sin, radians
from bullet import Bullet

class TankBase(rabbyt.Sprite):

    def __init__(self, name):
        
        rabbyt.Sprite.__init__(self, 'images/'+name+'.png')
        self.front_coll = False
        self.back_coll = False

    def render(self):
        
        self.front_coll = False
        self.back_coll = False
        rabbyt.Sprite.render(self)


class TankTurret(rabbyt.Sprite):
    
    def __init__(self, name):
        
        rabbyt.Sprite.__init__(self, 'images/'+name+'.png', (-10, 29, 10, -10))
        self.front_coll = False
        self.back_coll = False

    def render(self):

        self.front_coll = False
        self.back_coll = False
        rabbyt.Sprite.render(self)


class Tank(object):
     
    def __init__(self, turret, base, x, y):
       
        self.world = None
        self.t = TankTurret(turret)
        self.t.xy = (x, y)

        self.b = TankBase(base)
        self.b.xy = (x, y)
        
        self.velocity = [0,0]

        self.bullet_list = []

        self.reload = False

        self.top = self.b.top
        self.left = self.b.left
        self.right = self.b.right
        self.bottom = self.b.bottom
        self.x = self.b.x
        self.y = self.b.y
        
        self.top = float(self.top)

    
    def render(self):
        """
        Render this sprite
        """
         
        self.b.render()
        self.t.render()

        for b in self.bullet_list:
            b.render()

    
    def action(self, action, direction, dt):
        """
        Determine what movements the tank needs to make.
        """
        if action == 'move':
             self.move(direction, dt)

        elif action == 'rotate':
            self.rotate(direction, dt)

        elif action == 'turret':
            self.turretRotate(direction, dt)

        elif action == 'fire':
            self.fire(dt)
    
    
    def fire(self, dt):
        """
        fire a bullet
        """
        if not self.reload:
            angle_radians = radians(self.t.rot)

            bullet_x = self.t.x + sin(angle_radians)
            bullet_y = self.t.y + cos(angle_radians)

            bullet = Bullet('bullet', bullet_x, bullet_y, self)
            bullet.rot = self.t.rot
            self.bullet_list.append(bullet)
            self.reload = True
            clock.schedule_once(self.reloadComplete, 1.5)


    def reloadComplete(self, dt):
        """
        Allow them to fire again
        """
        self.reload = False


    def turretRotate(self, direction, dt):
        """
        Turret rotation is based on the left and right keys
        """
        top = self.t
        directions = {
            'left' : 2,
            'right' : -2,
        }
        rotation = directions[direction]
        top.rot += rotation


    def move(self, direction, dt):
        """
        Move the tank object.
        """
        bot = self.b
        top = self.t
        map_collisions = rabbyt.collisions.aabb_collide_groups([self.b], self.world.map_objects)
        for group in map_collisions:
            for obj in group:
                if direction == 'up':
                    obj.front_coll = True
                else:
                    obj.back_coll = True

        directions = {
            'up' : (1, 1),
            'down' : (1, -2),
        }
        dx, dy = directions[direction]

        a = [0.0,0.0]

        if direction == 'up':
            if not bot.front_coll:
                a[0] += cos(radians(bot.rot+90))*.9
                a[1] += sin(radians(bot.rot+90))*.9

                ff = .5 # Friction Factor

                self.velocity[0] *= ff
                self.velocity[1] *= ff

                self.velocity[0] += a[0]
                self.velocity[1] += a[1]

                bot.x += self.velocity[0]
                bot.y += self.velocity[1]
                top.x += self.velocity[0]
                top.y += self.velocity[1]
                self.x += self.velocity[0]
                self.y += self.velocity[1]

        elif direction == 'down':
            
            a[0] += cos(radians(bot.rot+90))*.9
            a[1] += sin(radians(bot.rot+90))*.9

            ff = .5 # Friction Factor

            self.velocity[0] *= ff
            self.velocity[1] *= ff

            self.velocity[0] += a[0]
            self.velocity[1] += a[1]

            bot.x -= self.velocity[0]
            bot.y -= self.velocity[1]
            top.x -= self.velocity[0]
            top.y -= self.velocity[1]
            self.x -= self.velocity[0]
            self.y -= self.velocity[1]
        self.top = self.b.top
        self.left = self.b.left
        self.right = self.b.right
        self.bottom = self.b.bottom
            

    def rotate(self, direction, dt):
        """
        Rotate the tank base left or right
        """

        bot = self.b
        directions = {
            'left' : 2,
            'right' : -2,
        }
        rotation = directions[direction]
        bot.rot += rotation

