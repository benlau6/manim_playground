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
            # *[1000] * 20,
        ]

        # creating positions in memory
        n_dots_total = sum(n_dots_per_groups)
        print(f"Creating {n_dots_total} dots")
        xs = -2 + np.random.random(n_dots_total) * 4 + offset[0]
        ys = -2 + np.random.random(n_dots_total) * 4 + offset[1]
        zs = np.zeros(n_dots_total)
        pos = np.vstack([xs, ys, zs])
        is_in_circle = (xs - offset[0]) ** 2 + (ys - offset[1]) ** 2 < 4

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


class PiTimeSeries(Scene):
    def construct(self):
        # Generate Monte Carlo data
        n_samples = 3000
        xs = -2 + np.random.random(n_samples) * 4
        ys = -2 + np.random.random(n_samples) * 4
        is_in_circle = xs**2 + ys**2 < 4

        # Calculate running pi estimates
        pi_estimates = []
        for i in range(1, n_samples + 1):
            n_in = np.sum(is_in_circle[:i])
            pi_est = n_in / i * 4
            pi_estimates.append(pi_est)

        # Create axes
        x_step = n_samples // 5
        axes = Axes(
            x_range=[0, n_samples + x_step // 2, x_step],
            y_range=[2, 4.5, 0.5],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=6,
        ).add_coordinates()

        # Labels
        title = Text("Monte Carlo Pi Estimation Over Time").scale(0.5).to_edge(UP)
        x_label = Text("Sample Size").scale(0.4).next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"\hat{\pi}").scale(1).next_to(axes.y_axis, UP)

        # True pi line
        pi_line = axes.get_horizontal_line(axes.c2p(n_samples, PI), color=WHITE)
        # axes.add_coordinates(None, {np.pi: r"$\pi$"}, None)
        pi_label = (
            MathTex(r"\pi", color=WHITE).scale(0.9).next_to(pi_line.get_left(), LEFT)
        )

        # Create the time series line
        x_values = list(range(1, n_samples + 1))

        # Track current position
        current_idx = ValueTracker(0)

        # Create moving pi text that follows the line
        pi_text = DecimalNumber(0, num_decimal_places=4, color=WHITE).scale(0.6)
        pi_dot = Dot(color=WHITE, radius=0.05)
        pi_group = VGroup(pi_text, pi_dot)

        def update_pi_text(mob):
            idx = int(current_idx.get_value())
            idx = min(idx, n_samples - 1)
            current_pi = pi_estimates[idx]
            x_pos = x_values[idx]

            # Update the text value
            pi_text.set_value(current_pi)

            # Position at the current point on the graph
            graph_point = axes.c2p(x_pos, current_pi)
            pi_dot.move_to(graph_point)
            pi_text.next_to(pi_dot, RIGHT)

        # reposition and update the text at time t
        pi_group.add_updater(update_pi_text)

        def update_pi_graph(mob):
            idx = int(current_idx.get_value())
            idx = min(idx, n_samples)

            # if idx = 0, it is 1 point, but for a line to be a line, it has to be 2 points
            if idx >= 1:
                new_pi_graph = axes.plot_line_graph(
                    x_values=x_values[:idx],
                    y_values=pi_estimates[:idx],
                    line_color=BLUE,
                    add_vertex_dots=False,
                )
                mob.become(new_pi_graph)

        # create a empty graph at first
        pi_graph = VMobject()
        # recreate a line plot at time t
        pi_graph.add_updater(update_pi_graph)

        # Add everything
        self.add(
            axes,
            title,
            x_label,
            y_label,
            pi_line,
            pi_label,
            pi_group,
            pi_graph,
        )

        # Animate the graph appearing with moving text
        self.play(
            current_idx.animate.set_value(n_samples),
            run_time=10,
        )

        # Remove updater after animation
        pi_group.clear_updaters()
        pi_graph.clear_updaters()

        # Show error of final estimate
        final_pi = pi_estimates[-1]
        error_text = (
            Text(f"Error: {abs(final_pi - PI):.4f}").scale(0.3).next_to(pi_text, DOWN)
        )

        self.play(Write(error_text))
        self.wait(2)


# class BraceAnnotation(Scene):
#     def construct(self):
#         dot = Dot(np.array([-2, -1, 0]))
#         dot2 = Dot(np.array([2, 1, 0]))
#         line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
#         b1 = Brace(line)
#         b1text = b1.get_text("Horizontal distance")
#         b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
#         b2text = b2.get_tex("x-x_1")
#         self.add(line, dot, dot2, b1, b2, b1text, b2text)


# class VectorArrow(Scene):
#     def construct(self):
#         dot = Dot(ORIGIN)
#         arrow = Arrow(ORIGIN, np.array([2, 2, 0]), buff=0)
#         numberplane = NumberPlane()
#         origin_text = Text("(0, 0)").next_to(dot, DOWN)
#         tip_text = Text("(2, 2)").next_to(arrow.get_end(), RIGHT)
#         self.add(numberplane, dot, arrow, origin_text, tip_text)


if __name__ == "__main__":
    with tempconfig({"quality": "medium_quality", "disable_caching": True}):
        scene = PiTimeSeries()
        scene.render()
