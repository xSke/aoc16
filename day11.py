# This one takes a long time - run with PyPy for best results

import collections
import fileinput

import re

State = collections.namedtuple("State", ["floors", "elevator_pos"])


def is_valid(state):
    for i, floor in enumerate(state.floors):
        has_generator = has_bare_chip = False

        # A bare chip is a chip without its accompanying generator
        for object in floor:
            if object.endswith(" chip"):
                if object.split(" ")[0] + " generator" not in floor:
                    has_bare_chip = True
            else:
                has_generator = True

        # A bare chip cannot survive if there are any generators on the floor
        if has_bare_chip and has_generator:
            return False

    return True


def is_solution(state):
    # It's a solution if all floors except the top one is empty
    return len(state.floors[0]) + len(state.floors[1]) + len(state.floors[2]) == 0


def to_prunable(state):
    # Convert to an abstract string representation where equivalent states are identical
    # Sort the individual items on the floors so they're in a determinstic order
    string_form = "\n".join([",".join(sorted(f)) for f in state.floors])

    # Then replace all elements with a number based on their index in the entire floor system
    # So [Co chip, Co gen] [Ru Chip] [Ru Gen]
    # ... and [Ru chip, Ru gen] [Co Chip] [Co Gen]
    # both evaluate to [0 chip, 0 gen] [1 chip] [1 gen]

    map = {}
    id = 0
    for f in state.floors:
        for obj in sorted(f):
            type = obj.split(" ")[0]

            if type not in map:
                map[type] = id
                id += 1

    for type, id in map.items():
        string_form = string_form.replace(type, str(id))

    return string_form, state.elevator_pos


def next_states(state):
    # A helper function to move one object from one floor to another
    def move_object(floors, object, from_floor, to_floor):
        if to_floor < 0 or to_floor >= 4:
            return floors

        new_floors = list(floors)
        new_floors[from_floor] = list(new_floors[from_floor])
        new_floors[from_floor].remove(object)

        new_floors[to_floor] = list(new_floors[to_floor])
        new_floors[to_floor].append(object)
        return new_floors

    elevator_floor = state.floors[state.elevator_pos]

    if state.elevator_pos < 3:
        could_move_two_up = False

        # Move two things up
        for object1 in elevator_floor:
            for object2 in elevator_floor:
                if object1 == object2:
                    continue

                new_floors = move_object(state.floors, object1, state.elevator_pos, state.elevator_pos + 1)
                new_floors = move_object(new_floors, object2, state.elevator_pos, state.elevator_pos + 1)
                new_state = state._replace(floors=new_floors, elevator_pos=state.elevator_pos + 1)
                if is_valid(new_state):
                    could_move_two_up = True
                    yield new_state

        # If we could move two items up, no need to try to move a single one up
        if not could_move_two_up:
            # Move one thing up
            for object in elevator_floor:
                new_floors = move_object(state.floors, object, state.elevator_pos, state.elevator_pos + 1)
                yield state._replace(floors=new_floors, elevator_pos=state.elevator_pos + 1)

    all_floors_below_empty = True
    for floor in state.floors[0:state.elevator_pos]:
        if len(floor) > 0:
            all_floors_below_empty = False

    # If all floors below us are empty, no point in moving anything down there
    if state.elevator_pos > 0 and not all_floors_below_empty:
        could_move_one_down = False

        # Move one thing down
        for object in elevator_floor:
            new_floors = move_object(state.floors, object, state.elevator_pos, state.elevator_pos - 1)
            new_state = state._replace(floors=new_floors, elevator_pos=state.elevator_pos - 1)
            if is_valid(new_state):
                could_move_one_down = True
                yield new_state

        # If we could move one item down, no need to try to move two down
        if not could_move_one_down:
            # Move two things down
            for object1 in elevator_floor:
                for object2 in elevator_floor:
                    if object1 == object2:
                        continue

                    new_floors = move_object(state.floors, object1, state.elevator_pos, state.elevator_pos - 1)
                    new_floors = move_object(new_floors, object2, state.elevator_pos, state.elevator_pos - 1)
                    yield state._replace(floors=new_floors, elevator_pos=state.elevator_pos - 1)


def run(initial):
    states_queue = [(0, initial)]
    last_step = 0

    # Keep a list of already-encountered values so we don't recalculate it constantly
    seen = set()

    while True:
        if len(states_queue) == 0:
            print("Empty search space")
            break

        step, state = states_queue.pop(0)

        if step > last_step:
            last_step = step

        if is_solution(state):
            break

        for new_state in next_states(state):
            prunable = to_prunable(new_state)
            if prunable not in seen and is_valid(new_state):
                seen.add(prunable)
                states_queue.append((step + 1, new_state))

    return last_step


object_re = re.compile(r"(\w+ generator|\w+\-compatible microchip)")


def parse_input():
    print("Input lines from puzzle input...")

    for i, line in enumerate(fileinput.input()):
        floor = []
        for match in object_re.findall(line):
            floor.append(match.replace("-compatible microchip", " chip"))

        yield floor

        if i >= 3:
            break


floors = list(parse_input())

print("Working... (may take a while)")
initial = State(floors=floors, elevator_pos=0)
print(" - The minimum amount of steps necessary is {} -".format(run(initial)))

initial.floors[0] += ["elerium generator", "elerium chip", "dilithium generator", "dilithium chip"]
print(" - The minimum amount of steps necessary (with extra parts) is {} -".format(run(initial)))