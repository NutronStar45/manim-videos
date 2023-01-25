from manim import *
import random


# abbreviations
# circ = circle
# rad = radius
# sq = square


class MonteCarloTau(Scene):
    def construct(self):
        # the circle and the square
        circ = Circle(3, color=WHITE).shift(RIGHT*28/9)
        sq = Square(6).shift(RIGHT*28/9)
        self.play(Create(sq), Create(circ))
        self.wait(.5)

        # the radius
        rad_brace = BraceBetweenPoints(RIGHT*1/9, RIGHT*1/9+DOWN*3, LEFT)
        rad = MathTex(r"1").next_to(rad_brace, LEFT)
        self.play(Write(rad_brace), Write(rad))
        self.wait(.5)

        # points
        points_count = 0
        text_points = Tex("Points: $0$").shift(LEFT*6+UP*3)
        text_points.shift(RIGHT * text_points.width / 2)

        # points in circle
        points_in_circle = 0
        text_points_in_circle = Tex("Points in circle: $0$").shift(LEFT*6+UP*2)
        text_points_in_circle.shift(RIGHT*text_points_in_circle.width/2)

        # ratio
        text_ratio = MathTex(r"0:0\approx\frac{\tau}{2}:4").shift(LEFT*6+UP)
        text_ratio.shift(RIGHT * text_ratio.width / 2)

        # approximate tau
        text_tau = MathTex(r"\tau\approx-").shift(LEFT*6)
        text_tau.shift(RIGHT * text_tau.width / 2)

        # write all texts
        self.play(Write(text_points), Write(text_points_in_circle),
                  Write(text_ratio), Write(text_tau))
        self.wait(.5)

        # integrate
        points = VGroup()
        for _ in range(500):
            for _ in range(20):
                point_x = random.random() * 2 - 1
                point_y = random.random() * 2 - 1
                point = Dot([point_x * 3 + 28/9, point_y * 3, 0])
                points_count += 1
                if point_x*point_x + point_y*point_y < 1:
                    points_in_circle += 1
                    point.set_color(GREEN)
                else:
                    point.set_color(RED)
                self.add(point)
                points += point
            text_points.become(
                Tex(f"Points: ${points_count}$").shift(LEFT*6+UP*3)
                    .shift(RIGHT * Tex(f"Points: ${points_count}$").width / 2)
            )
            text_points_in_circle.become(
                Tex(f"Points in circle: ${points_in_circle}$")
                    .shift(LEFT*6+UP*2)
                    .shift(RIGHT * Tex(
                        f"Points in circle: ${points_in_circle}$"
                    ).width / 2)
            )
            text_ratio.become(
                MathTex(
                    r"%d:%d\approx\frac{\tau}{2}:4" % (points_in_circle, points_count)
                ).shift(LEFT*6+UP)
                    .shift(RIGHT * MathTex(
                        r"%d:%d\approx\frac{\tau}{2}:4" % (points_in_circle, points_count)
                    ).width / 2)
            )
            text_tau.become(
                MathTex(r"\tau\approx%.6f" % (points_in_circle / points_count * 8))
                    .shift(LEFT*6)
                    .shift(RIGHT * MathTex(
                        r"\tau\approx%.6f" % (
                            points_in_circle / points_count * 8
                        )
                    ).width / 2)
            )
            self.wait(.1)
        self.wait(2)

        self.play(FadeOut(circ, sq, rad_brace, rad, text_points, text_points_in_circle, text_ratio, text_tau, points))


class MonteCarloTauTh(Scene):
    def construct(self):
        # the circle and the square
        circ = Circle(3, color=WHITE)
        sq = Square(6)
        self.add(sq, circ)

        # integrate
        points_count = 0
        points_in_circle = 0
        for _ in range(200):
            point_x = random.random() * 2 - 1
            point_y = random.random() * 2 - 1
            point = Dot([point_x * 3, point_y * 3, 0])
            points_count += 1
            if point_x*point_x + point_y*point_y < 1:
                points_in_circle += 1
                point.set_color(GREEN)
            else:
                point.set_color(RED)
            self.add(point)
