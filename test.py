# Exercise:

# Write a Python function decode_opcode(opcode: int) -> tuple[int, int, int, int] that, given a 16-bit CHIP‑8 opcode (0x0000 to 0xFFFF),
# returns the four 4-bit “nibbles” as integers in order: (first_nibble, second_nibble, third_nibble, fourth_nibble).

# E.g., if opcode = 0xA2F0, then decode_opcode(opcode) should return (0xA, 0x2, 0xF, 0x0), i.e., (10, 2, 15, 0).

# Briefly explain in a sentence or two how you extract each nibble (e.g., which bitwise ops you use).

# Write a few simple unit tests (just examples) for edge cases: e.g., lowest value (0x0000), highest (0xFFFF), and a random mid-range opcode.

# >> shift & bitwise and

import random


def decode_opcode(opcode: int) -> tuple[int, int, int, int]:
    print(f"opcode: {opcode}")

    first_nibble = (opcode >> 12) & 0xF0
    second_nibble = (opcode >> 8) & 0xF0
    third_nibble = (opcode >> 4) & 0xF0
    fourth_nibble = (opcode) & 0xF0

    return (first_nibble, second_nibble, third_nibble, fourth_nibble)


def decode_24_bit_opcode(opcode: int) -> tuple[int, int, int]:
    print(f"opcode: {opcode}")

    first_nibble = (opcode >> 16) & 0xFF
    second_nibble = (opcode >> 8) & 0xFF
    third_nibble = opcode & 0xFF

    return (first_nibble, second_nibble, third_nibble)


nums = []

for i in range(100):
    nums.append(random.randint(0, 2**16 - 1))

for i in nums:
    decoded_opcode = decode_opcode(i)
    print(f"decoded opcode: {decoded_opcode}\n{'-' * 5}")

nums = []

for i in range(100):
    nums.append(random.randint(0, 2**24 - 1))

for i in nums:
    decoded_opcode = decode_24_bit_opcode(i)
    print(f"decoded opcode: {decoded_opcode}\n{'-' * 5}")
