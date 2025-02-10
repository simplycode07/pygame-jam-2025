import pygame

from src import settings, colors
from src.ui import UIState
from .player import Sprite

class PhysicsEntities:
    def __init__(self, level_info) -> None:
        self.tilemap = level_info[0]
        player_info = level_info[1]
        hoop_info = level_info[2]

        self.player = Sprite(self.tilemap, player_info)
        # self.hoop = Hoop(hoop_info)

    def handle_input(self, event):
        self.player.handle_input(event)

    def update(self, delta, display):
        change_state, new_state = self.player.update(delta, display)

        # center = self.player.get_self_rect().center

        # this checks for collision with hoop, phsyics and score
        # if self.object_near_player(self.hoop):
        #     # this checks for physics collision with hoop
        #     for rect in self.hoop.collision_rects:
        #         collision_data = self.player.get_collision_with_rect(rect, pygame.Vector2(center), "(-1)")
        #         self.player.handle_collision(delta, collision_data, self.hoop.elasticity)
        #
        #     if self.hoop.check_for_win(self.player, pygame.Vector2(center)):
        #         change_state = True
        #         new_state = UIState.LEVEL_SELECTOR
        #         # print("You Win!")

        return (change_state, new_state)

    def reset(self):
        self.player.reset()

    # this checks if any passed object is near the player to do physics
    # the object should have the following attributes
    # 1) x, y -> current position
    # 2) collision range -> basically the area in which you wanna check for collision
    def object_near_player(self, entity) -> bool:
        if abs(self.player.pos[0] - entity.pos[0]) < entity.collision_range:
            if abs(self.player.pos[1] - entity.pos[1]) < entity.collision_range:
                return True

        return False
