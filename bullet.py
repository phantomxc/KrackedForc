from math import cos, radians, sin
from explosion import Explosion
import rabbyt



class Bullet(rabbyt.Sprite):
    
    def __init__(self, name, x, y, tank, left, top, right, bottom):
        
        #10 X 26
        rabbyt.Sprite.__init__(self, 'images/'+name+'.png', (left, top, right, bottom))
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
        
        if self.tank in player_collisions:
            player_collisions.remove(self.tank)

        if player_collisions:
            Explosion(self.x, self.y)
            player_hit = player_collisions[0]
            player_hit.health -= self.dmg
            if player_hit.health <= 0:
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




class BlueBullet(Bullet):
    
    def __init__(self, x, y, tank):
        """
        stuff
        """
        name = 'bluebullet'
        left = -5
        top = 13
        right = 5
        bottom = -13

        self.dmg = 50
        self.load_time = 1.5

        super(BlueBullet, self).__init__(name, x, y, tank, left, top, right, bottom)


class RedBullet(Bullet):
    
    def __init__(self, x, y, tank):
        """
        stuff
        """
        name = 'redbullet'
        left = -5
        top = 13
        right = 5
        bottom = -13

        self.dmg = 25
        self.load_time = .75

        super(RedBullet, self).__init__(name, x, y, tank, left, top, right, bottom)

