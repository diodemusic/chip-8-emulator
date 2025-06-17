import pyglet


class Chip(pyglet.window.Window):
    def __init__(self) -> None:
        self.key_inputs = self.init_list(num=16)
        self.display_buffer = self.init_list(num=32 * 64)
        self.memory = self.init_list(num=4096)
        self.gpio = self.init_list(16)
        self.sound_timer = 0
        self.delay_time = 0
        self.index = 0
        self.pc = 0
        self.stack = []

    def init_list(self, num: int) -> list[int]:
        return [0] * num
