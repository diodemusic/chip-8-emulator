import pyglet


class Chip(pyglet.window.Window):
    def __init__(self) -> None:
        self.clear()
        self.key_inputs = self._init_list(num=16)
        self.display_buffer = self._init_list(num=32 * 64)
        self.memory = self._init_list(num=4096)
        self.gpio = self._init_list(16)
        self.sound_timer = 0
        self.delay_timer = 0
        self.index = 0
        self.pc = 0
        self.stack = []
        self.fonts = []

    def initialize(self) -> None:
        self.clear()
        self.memory = self._init_list(num=4096)
        self.gpio = self._init_list(16)
        self.display_buffer = self._init_list(num=32 * 64)
        self.stack = []
        self.key_inputs = self._init_list(num=16)
        self.opcode = 0
        self.index = 0
        self.sound_timer = 0
        self.delay_timer = 0
        self.should_draw = False
        self.pc = 0x200

        i = 0

        while i < 80:
            self.memory[i] = self.fonts[i]
            i += 1

    def _init_list(self, num: int) -> list[int]:
        return [0] * num

    def load_rom(self, rom_file_name: str) -> None:
        rom_path: str = f"../roms/{rom_file_name}"
        print(f"Loading... {rom_path}")
        binary: bytes = open(rom_path, "rb").read()
        print(binary)

        offset: int = 0x200
        i: int = 0

        while i < len(binary):
            self.memory[i + offset] = binary[i]
            i += 1

    def cycle(self) -> None:
        self.opcode = self.memory[self.pc]
        self.vx = (self.opcode & 0x0F00) >> 8
        self.vy = (self.opcode & 0x00F0) >> 4
        self.pc += 2
        extracted_op = self.opcode & 0xF00

        try:
            self.funcmap[extracted_op]()
        except Exception as e:
            print(f"Unknown instructions: {self.opcode}: {e}")

        if not self.delay_timer > 0:
            return

        self.delay_timer -= 1

        if not self.sound_timer > 0:
            return

        self.sound_timer -= 1

        if not self.sound_timer == 0:
            return

        # TODO: play sound

    def _0ZZZ(self):
        extracted_op = self.opcode & 0xF0FF

        try:
            self.funcmap[extracted_op]()
        except Exception as e:
            print(f"Unkown instruction: {self.opcode}: {e}")
