import fileinput
import re


def swap_pos(s, a, b):
    a, b = (min(int(a), int(b)), max(int(a), int(b)))
    return s[:a] + s[b] + s[a + 1:b] + s[a] + s[b + 1:]


def swap_letter(s, a, b):
    return swap_pos(s, s.index(a), s.index(b))


def rotate_basic(s, dir, count):
    count = int(count)
    if dir == "left":
        return s[count:] + s[:count]
    else:
        return s[-count:] + s[:-count]


def rotate_basic_alt(s, dir, count):
    return rotate_basic(s, "left" if dir == "right" else "right", count)


def rotate_letter(s, letter):
    i = s.index(letter)
    s = rotate_basic(s, "right", i + 1)
    if i >= 4:
        s = rotate_basic(s, "right", 1)
    return s


def rotate_letter_alt(s, letter):
    for i in range(len(s) + 2):
        ss = rotate_basic(s, "left", i)
        if rotate_letter(ss, letter) == s:
            return ss


def reverse(s, a, b):
    a, b = (int(a), int(b))
    return s[:a] + s[b:a:-1] + s[a] + s[b + 1:]


def move_pos(s, a, b):
    l = list(s)
    l.insert(int(b), l.pop(int(a)))
    return "".join(l)


def move_pos_alt(s, a, b):
    return move_pos(s, b, a)


instructions = [
    ("swap position (\d+) with position (\d+)", swap_pos, swap_pos),
    ("swap letter (\w) with letter (\w)", swap_letter, swap_letter),
    ("rotate (left|right) (\d+) step", rotate_basic, rotate_basic_alt),
    ("rotate based on position of letter (\w)", rotate_letter, rotate_letter_alt),
    ("reverse positions (\d+) through (\d+)", reverse, reverse),
    ("move position (\d+) to position (\d+)", move_pos, move_pos_alt)
]

lines = list(fileinput.input())

inp = "abcdefgh"
for line in lines:
    for ins, func, func_alt in instructions:
        match = re.match(ins, line)
        if match:
            inp = func(inp, *match.groups())

print(" - The scrambled version of 'abcdefgh' is {} -".format(inp))

inp = "fbgdceah"
for line in lines[::-1]:
    for ins, func, func_alt in instructions:
        match = re.match(ins, line)
        if match:
            inp = func_alt(inp, *match.groups())

print(" - The unscrambled version of 'bgfacdeh' is {} -".format(inp))
