from pygame import *
from random import *

FPS = 60
Game = True
clock = time.Clock()
back = 'galaxy.jpg'
rocket = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

score = 0
lost = 0
max_lost = 3
goal = 10

finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_im, player_x, player_y, sixe_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_im), (sixe_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(back), (win_width, win_height))

monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

rocket = Player(rocket, 5, win_height - 100, 80, 100, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_in_the_hole = mixer.Sound('fire.ogg')

while Game:
    for e in event.get():
        if e.type == QUIT:
            Game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_in_the_hole.play()
                rocket.fire()
    
    if not finish:
        window.blit(background,(0, 0))
        rocket.update()
        monsters.update()
        bullets.update()

        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(rocket, monsters, False,) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    time.delay(50)

display.update()
clock.tick(FPS)