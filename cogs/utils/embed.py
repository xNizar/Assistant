import discord
import colorsys
import random


class EmbedUtils:
    @staticmethod
    def random_color():
        values = [int(i * 255) for i in colorsys.hsv_to_rgb(random.random(), 1, 1)]
        color = discord.Color.from_rgb(*values)

        return color
