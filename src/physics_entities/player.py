from math import sqrt
import pygame

from src.ui import UIState
from . import settings, colors
from enum import Enum


class Sprite:
    def __init__(self, tilemap, init_pos) -> None:
        self.tilemap = tilemap

        self.rect = pygame.Rect(init_pos[0], init_pos[1], settings.tilesize, settings.tilesize)
        self.init_pos = self.rect.copy()

        self.movement = [0.0, 0.0]

        self.img = pygame.image.load("assets/basky_32x32.png")
        self.angle = 0

        self.state = State.NORMAL

    def handle_input(self, event):
        
        keys = pygame.key.get_pressed()
        self.movement[0] = (keys[pygame.K_d] - keys[pygame.K_a])
        self.movement[1] = (keys[pygame.K_s] - keys[pygame.K_w])

        self.normalize_movement()


    def update(self, delta: float, surface):
        # self.rect += self.vel * delta
        position_tilemap = [int((self.rect.x + settings.tilesize//2) // settings.tilesize),
                            int((self.rect.y + settings.tilesize//2) // settings.tilesize)]

        # pygame.draw.rect(surface, colors["red"], pygame.Rect(
        #     position_tilemap[0] * settings.tilesize, position_tilemap[1] * settings.tilesize, settings.tilesize, settings.tilesize))

        self.rect.left += int(self.movement[0] * settings.player_speed * delta)
        self.rect.top += int(self.movement[1] * settings.player_speed * delta)

        movement_prohibited_x, movement_prohibited_y = self.get_tilemap_collision(
            surface, position_tilemap)

        # if self.movement[0] not in movement_prohibited_x:
        #     self.rect.left += int(self.movement[0] * settings.player_speed * delta)
        # else:
        #     print(f"cant move x: {self.movement[0]}")
        #
        # if self.movement[1] not in movement_prohibited_y:
        #     self.rect.top += int(self.movement[1] * settings.player_speed * delta)
        # else:
        #     print(f"cant move y: {self.movement[1]}")
        


        change_state = False
        new_state = None
        
        return (change_state, new_state)


    def reset(self):
        self.state = State.NORMAL
        self.rect = self.init_pos.copy()
        self.health = 3
        self.vel = pygame.Vector2(0, 0)


    # this functions checks for collision around the player
    # and returns the collision data that has the shortest normal
    def get_tilemap_collision(self, surface, position_tilemap) -> tuple[list[int], list[int]]:
        position_around = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        
        movement_prohibited_x = []
        movement_prohibited_y = []

        for pos in position_around:
            tile = self.tilemap.get(f"{position_tilemap[0] + pos[0]};{position_tilemap[1] + pos[1]}")
            if tile and tile["collidable"] and self.rect.colliderect(tile["rect"]):
                if pos[0] == 1:
                    self.rect.right = tile["rect"].left
                if pos[0] == -1:
                    self.rect.left = tile["rect"].right

                if pos[1] == 1:
                    self.rect.bottom = tile["rect"].top
                
                if pos[1] == -1:
                    self.rect.top = tile["rect"].bottom

                movement_prohibited_x.append(pos[0])
                movement_prohibited_y.append(pos[1])

        return movement_prohibited_x, movement_prohibited_y

    # returns collision data between a pygame.Rect object and player

    def clamp(self, start, value, end) -> int:
        if value < start:
            return start
        if value > end:
            return end

        return value

    def normalize_movement(self):
        length = sqrt(self.movement[0]**2 + self.movement[1]**2)

        if length != 0:
            self.movement[0] /= length
            self.movement[1] /= length

class State(Enum):
    NORMAL = 0
    INPUT = 1


class CollisionData:
    def __init__(self, collision_detected:bool, collision_point:list[int] | None, collision_with: str | None, collision_dir) -> None:
        self.collision_status = collision_detected
        self.collision_point = collision_point
        self.collision_with = collision_with
        self.collision_dir = collision_dir

    def update_all(self, collision_info: "CollisionData"):
        self.update_collision_point(collision_info.collision_point)
        self.update_collision_dir(collision_info.collision_dir)
        self.update_collision_status(collision_info.collision_status)
        self.update_collision_with(collision_info.collision_with)

    def update_collision_dir(self, new_dir):
        self.collision_dir = new_dir

    def update_collision_point(self, new_collision_point):
        self.collision_point = new_collision_point

    def update_collision_status(self, new_collision_status):
        self.collision_status = new_collision_status

    def update_collision_with(self, new_collision_with):
        self.collision_with = new_collision_with
