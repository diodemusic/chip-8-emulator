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
        self.fonts = [
            0xF0,
            0x90,
            0x90,
            0x90,
            0xF0,  # 0
            0x20,
            0x60,
            0x20,
            0x20,
            0x70,  # 1
            0xF0,
            0x10,
            0xF0,
            0x80,
            0xF0,  # 2
            0xF0,
            0x10,
            0xF0,
            0x10,
            0xF0,  # 3
            0x90,
            0x90,
            0xF0,
            0x10,
            0x10,  # 4
            0xF0,
            0x80,
            0xF0,
            0x10,
            0xF0,  # 5
            0xF0,
            0x80,
            0xF0,
            0x90,
            0xF0,  # 6
            0xF0,
            0x10,
            0x20,
            0x40,
            0x40,  # 7
            0xF0,
            0x90,
            0xF0,
            0x90,
            0xF0,  # 8
            0xF0,
            0x90,
            0xF0,
            0x10,
            0xF0,  # 9
            0xF0,
            0x90,
            0xF0,
            0x90,
            0x90,  # A
            0xE0,
            0x90,
            0xE0,
            0x90,
            0xE0,  # B
            0xF0,
            0x80,
            0x80,
            0x80,
            0xF0,  # C
            0xE0,
            0x90,
            0x90,
            0x90,
            0xE0,  # D
            0xF0,
            0x80,
            0xF0,
            0x80,
            0xF0,  # E
            0xF0,
            0x80,
            0xF0,
            0x80,
            0x80,  # F
        ]
        self.funcmap = {
            0x0000: self._0ZZZ,  # Extract nibbles
            0x00E0: self._0ZZ0,  # Clear screen
            0x00EE: self._0ZZE,  # Return from a subroutine
            0x1000: self._1ZZZ,  # Jump to address
            0x4000: self._4ZZZ,  # Skip next instruction if VX != NN
            0x5000: self._5ZZZ,  # Skip next instruction if VX == VY
            0x8004: self._8ZZ4,  # Adds VY to VX, VF is set to 1 when there's a carry, 0 otherwise
            0x8005: self._8ZZ5,  # VY is subtracted from VX, VF is set to 0 when there's a borrow, 1 otherwise
        }
        self.vx = 0
        self.vy = 0

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

    def _0ZZZ(self) -> None:
        extracted_op = self.opcode & 0xF0FF

        try:
            self.funcmap[extracted_op]()
        except Exception as e:
            print(f"Unkown instruction: {self.opcode}: {e}")

    def _0ZZ0(self) -> None:
        print("Clears the screen")
        self.display_buffer = self._init_list(num=64 * 32)
        self.should_draw = True

    def _0ZZE(self) -> int:
        print("Returns from the subroutine")
        self.pc = self.stack.pop()

    def _1ZZZ(self):
        print("Jumps to address NNN")
        self.pc = self.opcode & 0x0FFF

    def _4ZZZ(self):
        print("Skips the next instruction if VX doesn't equal NN")
        if self.gpio[self.vx] != (self.opcode & 0x00FF):
            self.pc += 2

    def _5ZZZ(self):
        print("Skips the next instruction if VX equals VY")
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _8ZZ4(self):
        print(
            "Adds vy to vx. vf is set to 1 when there's a carry, and to 0 when there isn't"
        )

        if self.gpio[self.vx] + self.gpio[self.vy] > 0xFF:
            self.gpio[0xF] = 1
        else:
            self.gpio[0xF] = 0

        self.gpio[self.vx] += self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ5(self):
        print(
            "vy is subtracted from vx. vf is set to 0 when there's a borrow, and 1 when there isnt"
        )

        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xF] = 0
        else:
            self.gpio[0xF] = 1

        self.gpio[0xF] = self.gpio[self.vx] - self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _DZZZ(self):
        print("Draw a sprite")
        self.gpio[0xF] = 0
        x = self.gpio[self.vx] & 0xFF
        y = self.gpio[self.vy] & 0xFF
        height = self.opcode & 0x000F
        row = 0

        while row < height:
            curr_row = self.memory[row + self.index]
            pixel_offset = 0

            while pixel_offset < 8:
                loc = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1

                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    continue

                mask = 1 << 8 - pixel_offset
                curr_pixel = (curr_row & mask) >> (8 - pixel_offset)
                self.display_buffer[loc] ^= curr_pixel

                if self.display_buffer[loc] == 0:
                    self.gpio[0xF] = 1
                else:
                    self.gpio[0xF] = 0

        row += 1
        self.should_draw = True

    def draw(self):
        if self.should_draw:
            self.clear()
            # line_counter = 0

            i = 0

            while i < 2048:
                if self.display_buffer[i] == 1:
                    self.pixel.blit((i % 64) * 10, 310 - ((i / 64) * 10))

                i += 1

            self.flip()
            self.should_draw = False

    def main(self):
        self.initialize()
        self.load_rom("test.rom")

        while not self.has_exit:
            self.dispatch_events()
            self.cycle()
            self.draw()
