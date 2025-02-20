import re
import pygame
from . import settings, colors


class LevelManager:
    def __init__(self, save_file) -> None:
        self.load_save_file(save_file)

    def load_save_file(self, save_file):
        with open(save_file, "r") as file:
            data = file.read().split(",")
            self.level = data[0]

    def load_tilemap(self, level, init_pos_player=[0, 0]):
        print(f"loading level {level}")
        with open(f"tilemaps/{level}.csv", "r") as file:
            tilemap = file.readlines()
            # print(tilemap)

        clean_tilemap = []
        for i in tilemap:
            clean_tilemap.append(i.strip().split(","))

        sep_tilemap = {}
        # init_pos_player = (0, 0)
        tilemap_height = len(clean_tilemap)
        tilemap_width = len(clean_tilemap[0])
        for y, x_pos in enumerate(clean_tilemap):
            for x, tile_type in enumerate(x_pos):
                # if clean_tilemap[y][x] != "0" and clean_tilemap[y][x] not in ["-1", "-2"]:
                if clean_tilemap[y][x] == "1":
                    sep_tilemap[f"{x};{y}"] = {"type": "wall",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "color":colors["white"],
                                               "collidable": True
                                               }
                if clean_tilemap[y][x] == "2":
                    sep_tilemap[f"{x};{y}"] = {"type": "wall",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "color":colors["red"],
                                               "collidable": True
                                               }
                if clean_tilemap[y][x] == "3":
                    sep_tilemap[f"{x};{y}"] = {"type": "wall",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "color":colors["green"],
                                               "collidable": True
                                               }
                if clean_tilemap[y][x] == "4":
                    sep_tilemap[f"{x};{y}"] = {"type": "wall",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "color":colors["blue"],
                                               "collidable": True
                                               }

                if clean_tilemap[y][x] == "0":
                    sep_tilemap[f"{x};{y}"] = {"type": "teleport_tile",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "collidable": False,
                                               "active": True
                                               }

                if clean_tilemap[y][x] == "0-0":
                    sep_tilemap[f"{x};{y}"] = {"type": "teleport_tile",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "collidable": False,
                                               "active": False
                                               }
                if clean_tilemap[y][x] == "-1":
                    sep_tilemap[f"{x};{y}"] = {"type": "ground",
                                               "rect": pygame.Rect(
                                                   x*settings.tilesize, y*settings.tilesize, settings.tilesize, settings.tilesize),
                                               "pixel_coor": (x*settings.tilesize, y*settings.tilesize),
                                               "collidable": False
                                               }
                elif tile_type == "-2":
                    init_pos_player = [x * settings.tilesize,
                                       y * settings.tilesize]

        sep_tilemap["height"] = tilemap_height
        sep_tilemap["width"] = tilemap_width

        return sep_tilemap, tuple(init_pos_player)
