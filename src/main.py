# Complete your game here
import pygame
from random import randint


class GameObject:
        
    def __init__(self, image:str, x: int , y: int):
        self._x = x
        self._y = y
        self.__sprite = pygame.transform.scale(pygame.image.load(image), (pygame.image.load(image).get_width() / 2, pygame.image.load(image).get_height() / 2))

    def sprite(self):
        return self.__sprite

    def pos(self):
        return (self._x, self._y)

    def __eq__(self, __other: object):
        if (__other._x <= self._x + self.__sprite.get_width() and __other._x >= self._x) and (__other._y <= self._y + self.__sprite.get_height() and __other._y >= self._y):
            return True
        return False
    

class Player(GameObject):
    def __init__(self, image: str, x: int, y: int):
        super().__init__(image, x, y)
        self.__velocity = 2

    def move(self, up: bool, down: bool, left: bool, right: bool):
        if left and self._x - self.__velocity >= 50:
            self._x -= self.__velocity
        if right and self._x + self.sprite().get_width() <= 590:
            self._x += self.__velocity
        if up and self._y - self.__velocity >= 50:
            self._y -= self.__velocity
        if down and self._y + self.sprite().get_height() <= 430:
            self._y += self.__velocity

    def teleport(self, pos:tuple):
        self._x, self._y = pos


class Enemy(GameObject):
    def __init__(self, image: str, x: int, y: int):
        super().__init__(image, x, y)
        self.__velocity = 1

    def chase_player(self, player:Player):
        if self._x > player._x:
            self._x -= self.__velocity
        if self._x < player._x:
            self._x += self.__velocity
        if self._y < player._y:
            self._y += self.__velocity
        if self._y > player._y:
            self._y -= self.__velocity
    

class Coin(GameObject):
    def __init__(self, image: str, x: int, y: int):
        super().__init__(image, x, y)

    def move_random(self):
        self._x, self._y = randint(55, 580), randint(55, 425)
    

class Door(GameObject):
    def __init__(self, image: str, x: int, y: int):
        super().__init__(image, x, y)
    

class Sokoban:
    def __init__(self):
        pygame.init()

        self.load_objects()

        self.game_font = pygame.font.SysFont("Arial", 24)

        self.coins = 0
        self.gameover = False
        
        self.width = 540
        self.height = 380
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Coin Chaser")

        self.to_up, self.to_left, self.to_down, self.to_right = False, False, False, False
        self.main_loop()

    def coin_caught(self, player:Player, coin:Coin):
        if player == coin:
            return True
        return False

    def player_caught(self,player:Player, enemy:Enemy):
        if player == enemy:
            return True
        return False

    def portal_reached(self, doorOne:Door, doorTwo:Door, player:Player):
        if player == doorOne:
            return doorTwo.pos()
        elif player == doorTwo:
            return doorOne.pos()
        return None

    def load_objects(self):
        self.objects = [Player("robot.png", 100, 100), Coin("coin.png", 270, 190), Door("door.png", 150, 250), Door("door.png", 400, 100), Enemy("monster.png", 300, 200)]

    def draw_game_boundary(self):
        pygame.draw.rect(self.window, (0, 0, 0), [50, 50, self.width, self.height], 6)

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True

                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_up = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False
               
            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill((255, 255, 255))

        game_text = self.game_font.render("Coins: " + str(self.coins), True, (0, 0, 0))
        self.window.blit(game_text, (25, 20))

        game_text = self.game_font.render("Esc = exit game", True, (0, 0, 0))
        self.window.blit(game_text, (25, 450))
        
        self.draw_game_boundary()
        
        for object in self.objects:
            self.window.blit(object.sprite(), object.pos())
        
        self.objects[0].move(self.to_up, self.to_down, self.to_left, self.to_right)
        self.objects[4].chase_player(self.objects[0])

        if self.coin_caught(self.objects[0], self.objects[1]):
            self.objects[1].move_random()
            self.coins += 1

        if self.player_caught(self.objects[0], self.objects[4]):
            self.gameover = True

        if self.gameover:
           print(f"Unfortunately you got caught by the monster but you did get {self.coins} point")
           exit()

        portal_activate = self.portal_reached(self.objects[2], self.objects[3], self.objects[0])
        if portal_activate:
            self.objects[0].teleport(portal_activate)
        
        pygame.display.flip()
        
        self.clock.tick(60)
        
Sokoban()
