from math import cos, radians, sin
from explosion import Explosion
import rabbyt



class Bullet(rabbyt.Sprite):
    
    def __init__(self, name, x, y, tank):
        
        #10 X 26
        rabbyt.Sprite.__init__(self, 'images/'+name+'.png', (-5, 13, 5, -13))
        self.x = x
        self.y = y
        self.dead = False
        self.speed = 16
        self.tank = tank
        self.world = tank.world

    def render(self):
        """
        Determines the animation for the bullet and does the collision detection
        """
        a = [0.0,0.0]
        
        a[0] += cos(radians(self.rot+90)) * self.speed
        a[1] += sin(radians(self.rot+90)) * self.speed

        self.x += a[0]
        self.y += a[1]
        
        map_collisions = rabbyt.collisions.aabb_collide_single(self, self.world.map_objects)
        player_collisions = rabbyt.collisions.aabb_collide_single(self, self.world.player_objects)
        
        
        if player_collisions:
            if self.tank not in player_collisions:
                Explosion(self.x, self.y)
                self.tank.score += 1
                self.tank.bullet_list.remove(self)
                del(self)
                return
        
        if map_collisions:
            Explosion(self.x, self.y)
            self.tank.bullet_list.remove(self)
            del(self)
            return
        
        if self.x < 0 or self.y < 0:
            self.tank.bullet_list.remove(self)
            del(self)

        elif self.y > self.world.window.height or self.x > self.world.window.width:
            self.tank.bullet_list.remove(self)
            del(self)

        else:
            rabbyt.Sprite.render(self)

