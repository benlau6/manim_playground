from manim import *

import numpy as np
import random as ran


class MonteCarlo(Scene):
    def construct(self):

        offset = (-4, 0, 0)

        circle = Circle(radius=2, color=RED)
        circle.move_to(offset)

        square = Rectangle(width=4, height=4)
        square.move_to(offset)

        self.add(circle)
        self.add(square)
        self.wait(1)

        point_text, point_number = point_label = VGroup(
            Text("All dot : "),
            DecimalNumber(0, show_ellipsis=False, num_decimal_places=0),
        )

        in_text, in_number = in_label = VGroup(
            Text("Dot in a circle : "),
            DecimalNumber(0, show_ellipsis=False, num_decimal_places=0),
        )

        pi_text, pi_number = pi_label = VGroup(
            Text("PI : "), DecimalNumber(0, show_ellipsis=True, num_decimal_places=4)
        )
        point_label.arrange(RIGHT)
        in_label.arrange(RIGHT)
        pi_label.arrange(RIGHT)

        point_label.move_to((2, -1, 0))
        in_label.move_to((2, 0, 0))
        pi_label.move_to((2, 1, 0))

        self.add(point_label, in_label, pi_label)

        n_dots_all = 0
        n_dots_in_circle = 0
        approx_pi = 0

        point_number.add_updater(lambda m: m.set_value(n_dots_all))
        in_number.add_updater(lambda m: m.set_value(n_dots_in_circle))
        pi_number.add_updater(lambda m: m.set_value(approx_pi))

        ran.seed(1)

        # create n groups
        n_groups = 50
        n_dots_per_group = 50
        n_dots_to_create = n_groups * n_dots_per_group
        print(f"Creating {n_dots_to_create} dots")
        for _ in range(n_groups):
            dots_group = VGroup()
            # create m dots per group
            for _ in range(n_dots_per_group + 1):
                pos = (-6 + ran.random() * 4, -2 + ran.random() * 4, 0)
                if (pos[0] + 4) ** 2 + pos[1] ** 2 < 4:
                    dot = Dot(color=RED, radius=0.04)
                    n_dots_in_circle += 1
                else:
                    dot = Dot(color=GREEN, radius=0.04)
                dot.move_to(pos)
                dots_group.add(dot)

                # update counters
                n_dots_all += 1
                approx_pi = n_dots_in_circle / n_dots_all * 4

            # create group of dots in run_time second
            sec_to_update = 0.5
            self.play(Create(dots_group, run_time=sec_to_update))

        self.wait(2)


class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.add(line, dot, dot2, b1, b2, b1text, b2text)


class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2, 2, 0], buff=0)
        numberplane = NumberPlane()
        origin_text = Text("(0, 0)").next_to(dot, DOWN)
        tip_text = Text("(2, 2)").next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)
