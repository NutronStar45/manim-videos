from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from numpy import sin, cos, sqrt, array, arctan2 as atan2


# abbreviations
# abs = absolute
# ang = angle
# bg = background
# dest = destination
# eq = equation
# hl = highlight
# len = length
# rect = rectangle
# sq = squared
# tri = triangle
# uv = unit vector
# vt = value tracker


# the script
script = [
    # [0]
    "Let's consider a triangle with side lengths A and B, with an angle of gamma between them.",
    "The height of the triangle is part of <bookmark mark='triangle'/>this right triangle with hypotenuse B and is opposite of gamma, <bookmark mark='length'/>so its length is B sine gamma.",
    "This line is part of the same right triangle and is adjacent to gamma, <bookmark mark='length'/>so its length is B cosine gamma.",
    "This line together with B cosine gamma is equal to A, <bookmark mark='length'/>so its length is A minus B cosine gamma.",
    "This line is <bookmark mark='hl'/>the third side of the triangle, <bookmark mark='length'/>so its length is C.",
    # [5]
    "We can calculate C using the Pythagorean theorem, and by simplifying it, we find C to be A squared plus B squared minus 2 A B cosine gamma.",
    "In fact, this formula works for every triangle, you can pause the video and verify it yourself."
]


# the unit vector of an angle
def uv(angle):
    return array([cos(angle), sin(angle), 0])


class LawOfCos(VoiceoverScene):
    def construct(self):
        # set the speech service for the voiceover
        self.set_speech_service(AzureService(
            voice="en-US-JennyNeural",
            style="newscast"
        ))

        # colors
        C_HL = YELLOW  # highlight

        with self.voiceover(script[0]):
            # the triangle
            tri = Polygon([-2, -1, 0], [2, -1, 0], [1, 1, 0], color=WHITE)
            self.play(Create(tri))

            # the brace & length of a
            # the brace & length of b
            # the mark & angle of gamma
            a_brace = BraceBetweenPoints([-2, -1, 0], [2, -1, 0], DOWN)
            a_len = MathTex(r"a").next_to(a_brace, DOWN)
            b_brace = BraceBetweenPoints([1, 1, 0], [-2, -1, 0],
                                         uv(atan2(3, -2)))
            b_len = MathTex(r"b").shift(LEFT*.95+UP*.675)
            gamma_mark = Angle(Line(LEFT*2+DOWN, RIGHT*2+DOWN),
                               Line(LEFT*2+DOWN, RIGHT+UP),
                               -atan2(2, 3)/4+.96)
            gamma_ang = MathTex(r"\gamma").shift(LEFT*.9+DOWN*.7)
            self.play(AnimationGroup(
                      Write(a_brace), Write(a_len),
                      Write(b_brace), Write(b_len),
                      Create(gamma_mark), Write(gamma_ang),
                      lag_ratio=.1))

        with self.voiceover(script[1]):
            # the brace of bsin
            # the right angle of the right triangle with hypotenuse b
            bsin = DashedLine(RIGHT+UP, RIGHT+DOWN)
            bsin_brace = BraceBetweenPoints([2, 1, 0], [2, -1, 0], RIGHT)
            right_ang = Angle(bsin, Line(RIGHT+DOWN, LEFT*2+DOWN),
                              .4, (-1, 1), elbow=True)
            self.play(Create(bsin), Write(bsin_brace), Create(right_ang))

            self.wait_until_bookmark("triangle")
            # highlight the right triangle with hypotenuse b
            b_tri_hl = Polygon([-2, -1, 0], [1, -1, 0], [1, 1, 0],
                               stroke_width=6, color=C_HL)
            self.play(FadeIn(b_tri_hl))

            self.wait_until_bookmark("length")
            # the length of bsin
            self.play(FadeOut(b_tri_hl))
            bsin_len = MathTex(r"b\sin\gamma").next_to(bsin_brace, RIGHT)
            self.play(Write(bsin_len))

        with self.voiceover(script[2]):
            # move the brace & length of a down
            # the brace of bcos
            bcos_brace = BraceBetweenPoints([-2, -1, 0], [1, -1, 0], DOWN)
            self.play(VGroup(a_brace, a_len).animate.shift(DOWN),
                      Write(bcos_brace))

            self.wait_until_bookmark("length")
            # the length of bcos
            bcos_len = MathTex(r"b\cos\gamma").next_to(bcos_brace, DOWN)
            self.play(Write(bcos_len))

        with self.voiceover(script[3]):
            # the brace of a-bcos
            a_bcos_brace = BraceBetweenPoints([1, -1, 0], [2, -1, 0], DOWN)
            self.play(Write(a_bcos_brace))

            self.wait_until_bookmark("length")
            # the length of a-bcos
            a_bcos_len = (MathTex(r"a - b\cos\gamma")
                          .next_to(a_bcos_brace, DOWN)
                          .shift(RIGHT*.5))
            self.play(Write(a_bcos_len))

        # duplicate the right triangle with hypotenuse c
        c2 = Line(RIGHT+UP, RIGHT*2+DOWN)
        bsin2 = bsin.copy()
        bsin_brace2 = bsin_brace.copy()
        bsin_len2 = bsin_len.copy()
        a_bcos2 = Line(RIGHT+DOWN, RIGHT*2+DOWN)
        a_bcos_brace2 = a_bcos_brace.copy()
        a_bcos_len2 = a_bcos_len.copy()
        c_tri_copy = VGroup(c2, bsin2,
                            a_bcos2, a_bcos_brace2, a_bcos_len2)
        self.add(c_tri_copy)

        # shift c_tri_copy to the top-right corner
        # move the brace of bsin to left
        bsin_brace2_dest = BraceBetweenPoints(LEFT*5+UP*3, LEFT*5+UP, LEFT)
        bsin_len2_dest = (MathTex(r"b\sin\gamma")
                          .next_to(bsin_brace2_dest, LEFT))
        self.play(c_tri_copy.animate.shift(LEFT*6+UP*2),
                  Transform(bsin_brace2, bsin_brace2_dest),
                  Transform(bsin_len2, bsin_len2_dest))

        with self.voiceover(script[4]):
            # the brace of c
            c_brace2 = Brace(c2, uv(atan2(1, 2)))
            self.play(Write(c_brace2))

            self.wait_until_bookmark("hl")
            # highlight c
            c_hl = Line(RIGHT+UP, RIGHT*2+DOWN, stroke_width=6, color=C_HL)
            self.play(FadeIn(c_hl), rate_func=there_and_back)
            self.remove(c_hl)

            self.wait_until_bookmark("length")
            # the length of c
            c_len2 = MathTex(r"c").shift(LEFT*3.8+UP*2.35)
            self.play(Write(c_len2))

        with self.voiceover(script[5]):
            # the first part of finding c^2
            eq_c_sq = MathTex(r"c^2").shift(LEFT*2.5+UP*3)
            eq_c_sq_part1 = (MathTex(r"{{= (b\sin\gamma)^2 +}} ({{a - b\cos\gamma}}){{^2}}")
                             .shift(RIGHT*.78+UP*2.95))
            eq_c_sq_part2 = (MathTex(r"= b^2\sin^2\gamma + a^2 - "
                                     r"2ab\cos\gamma + b^2\cos^2\gamma")
                             .shift(RIGHT*1.95+UP*1.95))
            eq_c_sq_part3 = (MathTex(r"= a^2 + b^2 - 2ab\cos\gamma")
                             .shift(RIGHT*.14+UP*.95))
            bg_rect_eq = BackgroundRectangle(
                VGroup(eq_c_sq, eq_c_sq_part1, eq_c_sq_part2, eq_c_sq_part3),
                buff=.2)
            self.play(FadeIn(bg_rect_eq), Write(eq_c_sq), Write(eq_c_sq_part1),
                      run_time=1.2)

            # the second part of finding c^2
            self.play(Write(eq_c_sq_part2), run_time=1.5)

            # the third part of finding c^2
            self.play(Write(eq_c_sq_part3), run_time=1.2)

        with self.voiceover(script[6]):
            # make braces below the triangle more compact
            # move a-bcos down
            # transform bcos and a-bcos into their absolute values
            bcos_len_abs = (MathTex(r"| {{b\cos\gamma}} |")
                            .next_to(bcos_brace, DOWN, .1))
            a_brace_dest = a_brace.copy().shift(UP*.1)
            a_bcos_brace_dest = a_bcos_brace.copy().shift(DOWN*1.6)
            a_bcos_len_abs = (MathTex(r"| {{a - b\cos\gamma}} |")
                              .next_to(a_bcos_brace_dest, DOWN, .1))
            a_bcos_len2_abs = (MathTex(r"| {{a - b\cos\gamma}} |")
                               .next_to(a_bcos_brace2, DOWN)
                               .shift(RIGHT*.5))
            eq_c_sq_part1_dest = (
                MathTex(r"{{= (b\sin\gamma)^2 +}} |{{a - b\cos\gamma}}|{{^2}}")
                   .shift(RIGHT*.73+UP*2.95))
            self.play(TransformMatchingTex(bcos_len, bcos_len_abs),
                      Transform(a_brace, a_brace_dest),
                      a_len.animate.next_to(a_brace_dest, DOWN, .1),
                      Transform(a_bcos_brace, a_bcos_brace_dest),
                      TransformMatchingTex(a_bcos_len, a_bcos_len_abs),
                      TransformMatchingTex(a_bcos_len2, a_bcos_len2_abs),
                      TransformMatchingTex(eq_c_sq_part1, eq_c_sq_part1_dest))

            # move the tip of the triangle to the left
            vt = ValueTracker(1)
            bcos = DashedLine(RIGHT*2+DOWN, RIGHT+DOWN, dash_length=.05)
            a_bcos2_dashed = DashedLine(UP*5, UP*6)
            self.add(bcos, a_bcos2_dashed)
            tri.add_updater(lambda m: m.become(
                Polygon([-2, -1, 0], [2, -1, 0], [vt.get_value(), 1, 0],
                        color=WHITE)))
            b_brace.add_updater(lambda m: m.become(
                BraceBetweenPoints([vt.get_value(), 1, 0],
                                   [-2, -1, 0],
                                   uv(atan2(vt.get_value()+2, -2)))))
            b_len.add_updater(lambda m: m.move_to(
                RIGHT * (vt.get_value()-2)/2
                + RIGHT * 9*sqrt(13)/40 * cos(atan2(vt.get_value()+2, -2))
                + UP * 9*sqrt(13)/40 * sin(atan2(vt.get_value()+2, -2))))
            gamma_mark.add_updater(lambda m: m.become(
                Angle(Line(LEFT*2+DOWN, RIGHT*2+DOWN),
                      Line(LEFT*2+DOWN, RIGHT*vt.get_value()+UP),
                      -atan2(2, vt.get_value()+2)/4+.96)))
            right_ang.add_updater(lambda m: m.become(
                Angle(bsin, Line(RIGHT*vt.get_value()+DOWN,
                                 RIGHT*vt.get_value()+LEFT*.6+DOWN),
                      .4, (-1, 1), elbow=True)))
            bsin.add_updater(lambda m: m.put_start_and_end_on(
                [vt.get_value(), 1, 0], [vt.get_value(), -1, 0]))
            bcos.add_updater(lambda m: m.become(
                DashedLine(RIGHT*2+DOWN,
                           RIGHT*vt.get_value()
                           +(LEFT*.6 if vt.get_value() < 2 else ORIGIN)
                           +DOWN,
                dash_length=.05)))
            bcos_brace.add_updater(lambda m: m.become(
                BraceBetweenPoints([-2, -1, 0], [vt.get_value(), -1, 0], DOWN)))
            bcos_len_abs.add_updater(lambda m: m.next_to(bcos_brace, DOWN, .1))
            c2.add_updater(lambda m: m.put_start_and_end_on(
                [-6 + min(vt.get_value(), 2), 3, 0],
                [min(-2-vt.get_value(), -4), 1, 0]))
            c_brace2.add_updater(lambda m: m.become(
                Brace(c2, uv(
                    (0 if vt.get_value() < 2 else TAU/2)
                    + atan2(2-vt.get_value(), 2)
                ))))
            c_len2.add_updater(lambda m: m.move_to(
                LEFT*(5-vt.get_value()/2
                      if vt.get_value() < 2 else
                      3+vt.get_value()/2) + UP*2
                + RIGHT
                    * 7/4/sqrt(5)
                    * cos(
                        (0 if vt.get_value() < 2 else TAU/2)
                        + atan2(2-vt.get_value(), 2))
                + UP
                    * 7/4/sqrt(5)
                    * sin(
                        (0 if vt.get_value() < 2 else TAU/2)
                        + atan2(2-vt.get_value(), 2))
            ))
            a_bcos_brace.add_updater(lambda m: m.become(
                BraceBetweenPoints([vt.get_value(), -2.6, 0],
                                   [2, -2.6, 0], DOWN)))
            a_bcos_len_abs.add_updater(lambda m:
                m.next_to(a_bcos_brace, DOWN, .1))
            a_bcos2.add_updater(lambda m:
                m.put_start_and_end_on([-6+vt.get_value(), 1, 0], [-4, 1, 0])
                if vt.get_value() < 2 else
                m.put_start_and_end_on([0, 5, 0], [0, 6, 0]))
            a_bcos2_dashed.add_updater(lambda m:
                m.put_start_and_end_on([-2-vt.get_value(), 1, 0], [-4, 1, 0])
                if vt.get_value() > 2 else
                m.put_start_and_end_on([0, 5, 0], [0, 6, 0]))
            a_bcos_brace2.add_updater(lambda m:
                m.become(
                    BraceBetweenPoints(LEFT*6+RIGHT*vt.get_value()+UP,
                                       LEFT*4+UP, DOWN)
                    if vt.get_value() < 2 else
                    BraceBetweenPoints(LEFT*2+LEFT*vt.get_value()+UP,
                                       LEFT*4+UP, DOWN)
                    if vt.get_value() > 2 else
                    BraceBetweenPoints(LEFT*4+UP, LEFT*4+UP, DOWN)))
            a_bcos_len2_abs.add_updater(lambda m:
                m.next_to(a_bcos_brace2, DOWN).shift(RIGHT*.5))
            bsin2.add_updater(lambda m: m.put_start_and_end_on(
                [-6+min(vt.get_value(), 2), 3, 0],
                [-6+min(vt.get_value(), 2), 1, 0]))
            bsin_brace2.add_updater(lambda m:
                m.become(Brace(bsin2, LEFT))
                if vt.get_value() < 2 else
                m.become(Brace(bsin2, RIGHT)))
            bsin_len2.add_updater(lambda m:
                m.next_to(bsin_brace2, LEFT if vt.get_value() < 2 else RIGHT))
            bsin_brace.add_updater(lambda m: m.become(
                BraceBetweenPoints(RIGHT*max(vt.get_value(), 2)+UP,
                                   RIGHT*max(vt.get_value(), 2)+DOWN,
                                   RIGHT)))
            bsin_len.add_updater(lambda m: m.next_to(bsin_brace, RIGHT))
            self.play(vt.animate.set_value(3),
                      gamma_ang.animate.shift(RIGHT*.3+DOWN*.05), run_time=1.5)

            # move the tip of the triangle to the right
            self.play(vt.animate.set_value(-3),
                      gamma_ang.animate.shift(LEFT*.9+UP*.3), run_time=2)

            # move the tip of the triangle to its original position
            self.play(vt.animate.set_value(1),
                      gamma_ang.animate.shift(RIGHT*.6+DOWN*.25), run_time=1.5)

        tri.clear_updaters()
        b_brace.clear_updaters()
        b_len.clear_updaters()
        gamma_mark.clear_updaters()
        right_ang.clear_updaters()
        bsin.clear_updaters()
        bcos.clear_updaters()
        bcos_brace.clear_updaters()
        bcos_len_abs.clear_updaters()
        c2.clear_updaters()
        c_brace2.clear_updaters()
        c_len2.clear_updaters()
        a_bcos_brace.clear_updaters()
        a_bcos_len_abs.clear_updaters()
        a_bcos2.clear_updaters()
        a_bcos2_dashed.clear_updaters()
        a_bcos_brace2.clear_updaters()
        a_bcos_len2_abs.clear_updaters()
        bsin2.clear_updaters()
        bsin_brace2.clear_updaters()
        bsin_len2.clear_updaters()
        bsin_brace.clear_updaters()
        bsin_len.clear_updaters()
        # fade out everything
        self.play(FadeOut(tri, a_brace, a_len, b_brace, b_len,
                          gamma_mark, gamma_ang, bsin,
                          bsin_brace, right_ang, bsin_len,
                          bcos_brace, bcos_len_abs,
                          a_bcos_brace, a_bcos_len_abs,
                          bsin2, bsin_brace2, bsin_len2, c2,
                          a_bcos2, a_bcos_brace2, a_bcos_len2_abs,
                          c_brace2, c_len2 ,bg_rect_eq, eq_c_sq,
                          eq_c_sq_part1_dest,
                          eq_c_sq_part2, eq_c_sq_part3,
                          bcos, a_bcos2_dashed))


class LawOfCosTh(Scene):
    def construct(self):
        tri = Polygon([-2, -1, 0], [2, -1, 0], [1, 1, 0], color=WHITE)
        a_brace = BraceBetweenPoints([-2, -1, 0], [2, -1, 0], DOWN)
        a_len = MathTex(r"a").next_to(a_brace, DOWN)
        b_brace = BraceBetweenPoints([1, 1, 0], [-2, -1, 0],
                                     uv(atan2(3, -2)))
        b_len = MathTex(r"b").shift(LEFT*.95+UP*.675)
        c_brace = BraceBetweenPoints([2, -1, 0], [1, 1, 0],
                                     uv(atan2(1, 2)))
        c_len = MathTex(r"c").shift(RIGHT*(1.5+sqrt(1053/2000))
                                    + UP*(sqrt(1053/8000)))
        gamma_mark = Angle(Line(LEFT*2+DOWN, RIGHT*2+DOWN),
                           Line(LEFT*2+DOWN, RIGHT+UP),
                           -atan2(2, 3)/4+.96)
        gamma_ang = MathTex(r"\gamma").shift(LEFT*.9+DOWN*.7)
        tex = MathTex(r"c^2 = a^2 + b^2 - 2ab\cos\gamma").shift(UP*2.5)
        self.add(tri, a_brace, a_len, b_brace, b_len,
                 c_brace, c_len, gamma_mark, gamma_ang, tex)
