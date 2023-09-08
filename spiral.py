from dataclasses import dataclass
from functools import partial
import turtle
from typing import List, Optional

UNIT = 15


@dataclass
class IntPoint2d:
    x: int
    y: int

    @classmethod
    def manhattan_displacements(cls, r: int = 1):
        return [
            cls(dy, dx)
            for dy in range(-r, r + 1)
            for dx in range(-r, r + 1)
            if dy != 0 or dx != 0
        ]

    def manhattan_distance(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def manhattan_neighbours(self, other, r=1):
        return self.manhattan_distance(other) <= r

    def squared_abs(self) -> int:
        return self.x ** 2 + self.y ** 2

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"P({self.x}, {self.y})"

    def __mul__(self, other: int):
        return self.__class__(self.x * other, self.y * other)


def key_to_angle(key: str) -> int:
    if key.startswith("KP_"):
        key = key[3:]

    DIGIT_TO_ANGLE = {
        '6': 0,
        '9': 45,
        '8': 90,
        '7': 135,
        '4': 180,
        '1': 225,
        '2': 270,
        '3': 325,
    }

    return DIGIT_TO_ANGLE[key]


def key_to_displacement(key: str):
    DIGIT_TO_DISPLACEMENT = {
        '6': (1, 0),
        '9': (1, 1),
        '8': (0, 1),
        '7': (-1, 1),
        '4': (-1, 0),
        '1': (-1, -1),
        '2': (0, -1),
        '3': (1, -1),
    }
    DIGIT_TO_DISPLACEMENT['l'] = DIGIT_TO_DISPLACEMENT['d'] = DIGIT_TO_DISPLACEMENT['6']
    DIGIT_TO_DISPLACEMENT['u'] = DIGIT_TO_DISPLACEMENT['e'] = DIGIT_TO_DISPLACEMENT['9']
    DIGIT_TO_DISPLACEMENT['k'] = DIGIT_TO_DISPLACEMENT['w'] = DIGIT_TO_DISPLACEMENT['8']
    DIGIT_TO_DISPLACEMENT['y'] = DIGIT_TO_DISPLACEMENT['q'] = DIGIT_TO_DISPLACEMENT['7']
    DIGIT_TO_DISPLACEMENT['h'] = DIGIT_TO_DISPLACEMENT['a'] = DIGIT_TO_DISPLACEMENT['4']
    DIGIT_TO_DISPLACEMENT['b'] = DIGIT_TO_DISPLACEMENT['z'] = DIGIT_TO_DISPLACEMENT['1']
    DIGIT_TO_DISPLACEMENT['j'] = DIGIT_TO_DISPLACEMENT['x'] = DIGIT_TO_DISPLACEMENT['2']
    DIGIT_TO_DISPLACEMENT['n'] = DIGIT_TO_DISPLACEMENT['c'] = DIGIT_TO_DISPLACEMENT['3']

    return IntPoint2d(*DIGIT_TO_DISPLACEMENT[key])


visited_points = [IntPoint2d(0, 0)]


def canvas_to_logical(canvas_coords):
    return IntPoint2d(int(canvas_coords[0] // UNIT), int(canvas_coords[1] // UNIT))


def step_by_d(d: IntPoint2d):
    p = turtle.position()
    new_canvas_coords = (p[0] + d.x * UNIT, p[1] + d.y * UNIT)
    turtle.goto(new_canvas_coords)
    visited_points.append(canvas_to_logical(new_canvas_coords))
    print(visited_points)


def step_by_key(key: str):
    print(key)
    d = key_to_displacement(key)
    step_by_d(d)


def undo_step():
    if len(visited_points) > 1:
        visited_points.pop()
        turtle.undo()
        print(visited_points)


def next_step_score(visited: List[IntPoint2d], step_d: IntPoint2d) -> int:
    last_point = visited[-1]
    next_point = last_point + step_d

    previous_step_d = visited[-1] - visited[-2]

    old_radius_squared = last_point.squared_abs()
    radius_squared = next_point.squared_abs()

    # We want step_d vector to be clockwise from radius vector
    cross_product = (last_point.x * step_d.y - last_point.y * step_d.x)

    clockwise = cross_product >= 0
    strictly_clockwise = cross_product > 0
    returning = old_radius_squared > radius_squared
    strictly_returning = (abs(next_point.x) <= abs(last_point.x)) and (abs(next_point.y) <= abs(last_point.y))
    right_angle_with_previous = (step_d.x * previous_step_d.x + step_d.y * previous_step_d.y) == 0
    print(f"{step_d=} {previous_step_d=} {right_angle_with_previous=} {int(right_angle_with_previous) * 4=}")

    already_visited_neighbours = [p for p in visited if next_point.manhattan_neighbours(p)]
    # a = radius_squared \
    #     - len(already_visited_neighbours) \
    #     - int(clockwise) * 3 \
    #     - int(strictly_clockwise) * 5 \
    #     - int(returning) if clockwise or returning else radius_squared * 2
    # b = radius_squared \
    #     - len(already_visited_neighbours) \
    #     - int(clockwise) * 3 \
    #     - int(strictly_clockwise) * 5 \
    #     - int(returning) if clockwise or returning else radius_squared * 2 \
    #     + int(right_angle_with_previous) * 5
    # print(f"{a=} {b=}")
    return \
        radius_squared \
        - len(already_visited_neighbours) \
        - int(clockwise) * 4 \
        - int(strictly_clockwise) * 6 \
        - int(returning) * 2 \
        - int(strictly_returning) * 5 \
        + (0 if clockwise or strictly_returning else radius_squared) \
        - (old_radius_squared - radius_squared if returning else 0) \
        + int(right_angle_with_previous)


def auto_step() -> None:
    if len(visited_points) == 1:
        step_by_key("9")  # or maybe a random one
    else:
        step_by_d(generate_auto_step())


def auto_draw() -> None:
    old_speed = turtle.speed()
    old_tracer = turtle.tracer()

    turtle.speed('fastest')
    # turtle.tracer(0, 0)

    for _ in range(10000):
        auto_step()

    turtle.update()
    turtle.tracer(old_tracer)
    turtle.speed(old_speed)
        
        
def generate_auto_step() -> Optional[IntPoint2d]:
    last_point = visited_points[-1]
    previous_d = visited_points[-1] - visited_points[-2]
    best_d = IntPoint2d(0, 0)
    best_score = 100000
    for d in IntPoint2d.manhattan_displacements(1):
        if d != previous_d:
            next_point = last_point + d
            if next_point not in visited_points:
                score = next_step_score(visited_points, d)
                print(f"{d=}; {score=}")
                if score < best_score:
                    best_d = d
                    best_score = score
    else:
        if best_d != IntPoint2d(0, 0):
            return best_d
        else:
            return None


def main():
    for i in "adqwezzxchjklyubn":
        h = partial(step_by_key, i)
        turtle.onkey(h, i)

    turtle.onkey(auto_step, "5")
    turtle.onkey(auto_draw, "0")
    turtle.onkey(undo_step, "BackSpace")

    turtle.color('red')
    turtle.listen()
    turtle.mainloop()


if __name__ == "__main__":
    main()

