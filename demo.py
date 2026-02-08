from manim import *

import numpy as np

np.random.seed(42)


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

        n_dots_now = 0
        n_dots_in_circle = 0
        approx_pi = 0

        point_number.add_updater(lambda m: m.set_value(n_dots_now))
        in_number.add_updater(lambda m: m.set_value(n_dots_in_circle))
        pi_number.add_updater(lambda m: m.set_value(approx_pi))

        n_dots_per_groups = [
            *[1] * 10,
            *[100] * 10,
            *[1000] * 20,
        ]

        # creating positions in memory
        n_dots_total = sum(n_dots_per_groups)
        print(f"Creating {n_dots_total} dots")
        xs = -6 + np.random.random(n_dots_total) * 4
        ys = -2 + np.random.random(n_dots_total) * 4
        zs = np.zeros(n_dots_total)
        pos = np.vstack([xs, ys, zs])
        is_in_circle = (xs + 4) ** 2 + ys**2 < 4

        # create n groups
        # drawing dots
        for n_dots_per_group in n_dots_per_groups:
            print(f"Drawing {n_dots_per_group} dots")
            dots_group = VGroup()
            # create m dots per group
            for _ in range(n_dots_per_group):
                dot_idx = n_dots_now
                if is_in_circle[dot_idx]:
                    color = RED
                    n_dots_in_circle += 1
                else:
                    color = GREEN

                dot = Dot(color=color, radius=0.04)
                dot.move_to(pos[:, dot_idx])
                dots_group.add(dot)
                n_dots_now += 1

            # update counters
            approx_pi = n_dots_in_circle / n_dots_now * 4

            # draw group of dots in run_time second
            # matching this with fps can speed up rendering by a lot
            # cuz if additional screens have to be copied
            sec_per_animation = 0.5
            self.play(Create(dots_group, run_time=sec_per_animation))

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
