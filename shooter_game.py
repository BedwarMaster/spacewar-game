#import stuff
from pygame import *
from random import *
import math
from random import choice

#create windows
WIDTH, HEIGHT = 800,640
window = display.set_mode((WIDTH,HEIGHT))
clock = time.Clock()
font.init()
#createclasses
class  ImageSprite(sprite.Sprite):
    def __init__(self, filename, pos, size):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image,size)
        self.rect = Rect(pos, size)
        self.initial_pos = pos
    def draw(self, surface):
        surface.blit(self.image,self.rect.topleft)
    def reset(self):
        self.rect.topleft = self.initial_pos

class PlayerSprite(ImageSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= 8
        if keys[K_d]:
            self.rect.x += 8   
        
            

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        b = BulletSprite(filename='asteroid.png', pos=(0,0), size=(7,12))
        b.rect.center = self.rect.midtop#place the bullet
        ammos.add(b)            
    #def is_colliding_with(self, other_sprite):
        #col = sprite.collide_rect(self, other_sprite)
        #return col

class EnemySprite(ImageSprite):
    def __init__(self, filename, pos, size,speed):
        super().__init__(filename,pos,size)
        self.speed = Vector2(speed)
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)

class BulletSprite(ImageSprite):
    def update(self): 
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()
       
class TextSprite():
    def __init__(self, text, color, pos, font_size):
        self.font = font.SysFont(None, font_size)
        self.pos = pos
        self.color = color
        self.set_new_text(text)
    def set_new_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image,self.pos)

score = 0
points_counter = TextSprite(
    text="Du hast: " +str(score), 
    color=(174, 214, 241), 
    pos=(50,50), 
    font_size=30)

mixer.init()
win_music = mixer.Sound('fire.ogg')
lose_music = mixer.Sound('fire.ogg')
soundeffects = []
soundeffect = mixer.Sound('Death.wav')
soundeffects.append(soundeffect)




win_label = ImageSprite(filename='lose.jpg', pos=(0,0), size=(WIDTH,HEIGHT))
lose_label = ImageSprite(filename='lose.jpg', pos=(0,0), size=(WIDTH,HEIGHT))
bg = ImageSprite(filename='galaxy.jpg', pos=(0,0), size=(WIDTH,HEIGHT))
p1 = PlayerSprite(filename='rocket.png', pos=(350,540), size=(100,100))


monsters = sprite.Group()
ammos = sprite.Group()

def create_enemy():
    x = randint(0,WIDTH-50)
    y = -40
    speedy = randint(4,8)
    e1 = EnemySprite(filename='ufo.png', pos=(x,y), size=(50,50), speed=(0,speedy))
    monsters.add(e1)

for _ in range(90):
    create_enemy()



#for a in range(1,6):
    #monster = EnemySprite(filename='ufo.png', pos=(randint(0,600), 0), size=(50,50))
    #monsters.append(monster)

game_over = False
state = "START"

while not event.peek(QUIT):
    if not game_over:
        #region Game

        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    p1.shoot()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    p1.shoot()
        bg.draw(window)
        p1.update()
        p1.draw(window)
        monsters.update()
        monsters.draw(window)
        ammos.update()
        ammos.draw(window)
        points_counter.draw(window )
        players_hits = sprite.spritecollide(p1,monsters, True)
        for hit in players_hits:
            create_enemy()
            score -= 10
            points_counter.set_new_text("Du hast: " +  str(score))

        enemies_hits = sprite.groupcollide(ammos,monsters, True,True)
        for hit in enemies_hits:
            create_enemy()
            score += 50
            points_counter.set_new_text("Du hast: " +str(score))
            choice(soundeffects).play()
        
        #endregion Game
        
        #region Game Over
        if score < -1500:
            
            game_over = True
            state = "L"
            
            
        elif score > 1500:
            
            game_over = True
            state = "Glory"
            
    else:
        
        if state == 'L':
            lose_label.draw(window)
            # lose_music.play()
        elif state == "Glory":
            win_label.draw(window)
            # win_music.play()
        
       
        #endregion Game Over

    
    display.update()
    clock.tick(60)
    #opengameart.org
  