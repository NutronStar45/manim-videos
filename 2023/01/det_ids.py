from manim import *


# abbreviations
# alg = algebraic
# arr = arrow
# bg = background
# dest = destination
# det = determinant
# eq = equation
# expl = explanation
# par = parallelogram
# rect = rectangle
# vt = value tracker


def det_2d(a, b, c, d):
    """calculate |a b ; c d|"""
    return a*d - b*c


def det_2d_vt(a, b, c, d):
    """extract the values and calculate |a b ; c d|"""
    return det_2d(a.get_value(), b.get_value(),
                  c.get_value(), d.get_value())


def rrnz(x, precision):
    """round (remove negative zero)"""
    return 0 if round(x, precision) == 0 else round(x, precision)


class DetIds2D(Scene):
    def construct(self):
        # ------ #
        # Notice #
        # ------ #

        # fade in arrow
        # fade in text
        arr_notice = Arrow([5, 2, 0], [6, 3, 0])
        text_notice = Text(
            "Watch this if you're unfamiliar\nwith thinking of determinants as\nsigned areas/scaling factors"
        ).scale(.5).shift(RIGHT*2.3+UP*1.8)
        self.play(FadeIn(arr_notice), FadeIn(text_notice))
        self.wait(2)

        # fade out arrow
        # fade out text
        self.play(FadeOut(arr_notice), FadeOut(text_notice))


        # ------------------ #
        # All Zeros (Column) #
        # ------------------ #

        # a number plane
        # a number plane for reference
        plane = NumberPlane(y_range=(-64/9, 64/9, 1))
        plane_copy = NumberPlane(y_range=(-64/9, 64/9, 1),
                                 axis_config={"stroke_opacity": .5},
                                 background_line_style={
                                    "stroke_color": WHITE,
                                    "stroke_opacity": .1
                                })
        self.play(Create(plane), run_time=1.5)
        self.add(plane_copy)
        self.wait(.2)

        # two vectors
        v1_x = ValueTracker(1)
        v1_y = ValueTracker(2)
        v2_x = ValueTracker(-3)
        v2_y = ValueTracker(1)
        v1 = Vector([v1_x.get_value(), v1_y.get_value()])
        v2 = Vector([v2_x.get_value(), v2_y.get_value()])
        self.play(Create(v1), Create(v2))

        # the parallelogram formed by the vectors
        par = Polygon(
            [0, 0, 0],
            [v1_x.get_value(), v1_y.get_value(), 0],
            [
                v1_x.get_value()+v2_x.get_value(),
                v1_y.get_value()+v2_y.get_value(),
                0
            ],
            [v2_x.get_value(), v2_y.get_value(), 0],
            color=ORANGE)
        par.set_fill(ORANGE, .5)
        self.play(Create(par))

        # the signed area
        text_area = (Tex(
            f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
        ).shift(LEFT*6.5+UP*3.5))
        text_area.shift(RIGHT * text_area.width/2)
        bgrect_text_area = BackgroundRectangle(text_area, buff=.2)
        self.play(FadeIn(bgrect_text_area), Write(text_area))
        self.wait(.5)
        
        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&0\\A_{21}&0\end{vmatrix}=0"
        ).shift(RIGHT*5.5+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # move v2 to (0,0)
        v1.add_updater(lambda m: m.become(
            Vector([v1_x.get_value(), v1_y.get_value(), 0])
        ))
        v2.add_updater(lambda m: m.become(
            Vector([v2_x.get_value(), v2_y.get_value(), 0])
        ))
        par.add_updater(lambda m: m.become(
            Polygon(
                [0, 0, 0],
                [v1_x.get_value(), v1_y.get_value(), 0],
                [
                    v1_x.get_value()+v2_x.get_value(),
                    v1_y.get_value()+v2_y.get_value(),
                    0
                ],
                [v2_x.get_value(), v2_y.get_value(), 0],
            color=ORANGE).set_fill(ORANGE, .5)
        ))
        text_area.add_updater(lambda m: m.become(
            Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                .shift(
                    LEFT*6.5 + UP*3.5
                    + RIGHT * Tex(
                        f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                    ).width/2)
        ))
        bgrect_text_area.add_updater(lambda m: m.become(
            BackgroundRectangle(
                Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                    .shift(
                        LEFT*6.5 + UP*3.5
                        + RIGHT * Tex(
                            f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                        ).width/2),
                buff=.2)
        ))
        self.play(v2_x.animate.set_value(0), v2_y.animate.set_value(0))

        # explanation
        text_expl = (Text("If a column consists of only 0s,\nthe parallelogram formed by the columns collapses into a line,\nmaking the determinant 0.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # --------------- #
        # All Zeros (Row) #
        # --------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}0&0\\A_{21}&A_{22}\end{vmatrix}=0"
        ).shift(RIGHT*5+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # set the x-coordinates to 0
        self.play(v1_x.animate.set_value(0), v2_x.animate.set_value(0))

        # explanation
        text_expl = (Text("If a row consists of only 0s,\nthe parallelogram formed by the columns collapses into a line,\nmaking the determinant 0.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v2_x.animate.set_value(-3))


        # ---------------------------------------- #
        # A column is a multiple of another column #
        # ---------------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&rA_{11}\\A_{21}&rA_{21}\end{vmatrix}=0"
        ).shift(RIGHT*5+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # set v2 to v1
        self.play(v2_x.animate.set_value(1), v2_y.animate.set_value(2))

        # slide v2 along v1
        self.play(v2_x.animate.set_value(-1.5), v2_y.animate.set_value(-3))
        self.play(v2_x.animate.set_value(1.5), v2_y.animate.set_value(3))

        # explanation
        text_expl = (Text("If a column is a multiple of another column,\nthe parallelogram formed by the columns collapses into a line,\nmaking the determinant 0.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # ---------------------------------- #
        # A row is a multiple of another row #
        # ---------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&A_{12}\\rA_{11}&rA_{12}\end{vmatrix}=0"
        ).shift(RIGHT*5+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # set the y-coordinates to the x-coordinates
        self.play(v1_y.animate.set_value(1), v2_y.animate.set_value(-3))

        # change the slope
        self.play(v1_y.animate.set_value(-1), v2_y.animate.set_value(3))
        self.play(v1_y.animate.set_value(1/3), v2_y.animate.set_value(-1))

        # explanation
        text_expl = (Text("If a row is a multiple of another row,\nthe columns have the same slope, and the parallelogram\nformed by the columns collapses into a line,\nmaking the determinant 0.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_y.animate.set_value(2), v2_y.animate.set_value(1))

        
        # ------------------ #
        # Switch two columns #
        # ------------------ #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{12}&A_{11}\\A_{22}&A_{21}\end{vmatrix}=-\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).shift(RIGHT*4+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # switch the columns
        self.play(v1_x.animate.set_value(-3), v1_y.animate.set_value(1),
                  v2_x.animate.set_value(1), v2_y.animate.set_value(2))

        # explanation
        text_expl = (Text("Since the orientation is changed and the area isn't,\nthe determinant is multiplied by -1.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # --------------- #
        # Switch two rows #
        # --------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{21}&A_{22}\\A_{11}&A_{12}\end{vmatrix}=-\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).shift(RIGHT*4+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # switch the rows
        # switch the axes
        self.play(v1_x.animate.set_value(2), v1_y.animate.set_value(1),
                  v2_x.animate.set_value(1), v2_y.animate.set_value(-3),
                  plane.animate.apply_matrix([[0, 1], [1, 0]]))

        # explanation
        text_expl = (Text("The x- and y-coordinates are switched,\nso the orientation is changed and the area isn't,\nand the determinant is multiplied by -1.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        # switch the axes
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1),
                  plane.animate.apply_matrix([[0, 1], [1, 0]]))


        # ---------------------------------- #
        # Multiplying a column by a constant #
        # ---------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&rA_{12}\\A_{21}&rA_{22}\end{vmatrix}=r\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).shift(RIGHT*4+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # multiply the second column by -.5
        self.play(v2_x.animate.set_value(1.5), v2_y.animate.set_value(-.5))

        # explanation
        text_expl = (Text("If a column is multiplied by a constant,\nthe area of the parallelogram is multiplied by the same constant.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # ------------------------------- #
        # Multiplying a row by a constant #
        # ------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}rA_{11}&rA_{12}\\A_{21}&A_{22}\end{vmatrix}=r\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).shift(RIGHT*3.8+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # multiply the x-coordinates by 2
        # stretch the x-axis by 2
        self.play(v1_x.animate.set_value(2), v2_x.animate.set_value(-6),
                  plane.animate.apply_matrix([[2, 0], [0, 1]]))

        # explanation
        text_expl = (Text("Multiplying a row by a constant is equivalent to\nstretching the parallelogram by the same constant,\nand its area is multiplied by that constant.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        # stretch the axis by 1/2
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v2_x.animate.set_value(-3),
                  plane.animate.apply_matrix([[1/2, 0], [0, 1]]))

        
        # -------------------------------------------------------------- #
        # Adding determinants of matrices with only one different column #
        # -------------------------------------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}+\begin{vmatrix}A_{11}&B_{12}\\A_{21}&B_{22}\end{vmatrix}=\begin{vmatrix}A_{11}&A_{12}+B_{12}\\A_{21}&A_{22}+B_{22}\end{vmatrix}"
        ).scale(.6).shift(RIGHT*4+DOWN*3.4)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # two vectors
        v3_x = ValueTracker(1)
        v3_y = ValueTracker(2)
        v4_x = ValueTracker(-2)
        v4_y = ValueTracker(0)
        v3 = Vector([v3_x.get_value(), v3_y.get_value()])
        v4 = Vector([v4_x.get_value(), v4_y.get_value()])
        self.play(Create(v3), Create(v4))

        # the parallelogram formed by the vectors
        # change Signed area to Total signed area
        par2 = Polygon(
            [0, 0, 0],
            [v3_x.get_value(), v3_y.get_value(), 0],
            [
                v3_x.get_value()+v4_x.get_value(),
                v3_y.get_value()+v4_y.get_value(),
                0
            ],
            [v4_x.get_value(), v4_y.get_value(), 0],
            color=ORANGE)
        par2.set_fill(ORANGE, .5)
        text_area.clear_updaters()
        bgrect_text_area.clear_updaters()
        text_total_area = (Tex(
            f"Total signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y) + det_2d_vt(v3_x, v3_y, v4_x, v4_y), 2):.2f}"
        ).shift(LEFT*6.5+UP*3.5))
        text_total_area.shift(RIGHT * text_total_area.width/2)
        bgrect_text_total_area = BackgroundRectangle(text_total_area, buff=.2)
        self.play(Create(par2),
                  FadeOut(bgrect_text_area, text_area),
                  FadeIn(bgrect_text_total_area),
                  Write(text_total_area))

        # move par2
        self.play(VGroup(v3, v4, par2).animate.shift(LEFT*3+UP))

        # shear both parallelograms
        v3.add_updater(lambda m: m.become(
            Vector([v3_x.get_value(), v3_y.get_value(), 0])
                .shift(np.array([v2_x.get_value(), v2_y.get_value(), 0]))
        ))
        v4.add_updater(lambda m: m.become(
            Vector([v4_x.get_value(), v4_y.get_value(), 0])
                .shift(np.array([v2_x.get_value(), v2_y.get_value(), 0]))
        ))
        par2.add_updater(lambda m: m.become(
            Polygon(
                [0, 0, 0],
                [v3_x.get_value(), v3_y.get_value(), 0],
                [
                    v3_x.get_value()+v4_x.get_value(),
                    v3_y.get_value()+v4_y.get_value(),
                    0
                ],
                [v4_x.get_value(), v4_y.get_value(), 0],
            color=ORANGE)
                .shift(np.array([v2_x.get_value(), v2_y.get_value(), 0]))
                .set_fill(ORANGE, .5)
        ))
        self.play(v2_x.animate.set_value(-35/11), v2_y.animate.set_value(7/11),
                  v4_x.animate.set_value(-20/11), v4_y.animate.set_value(4/11))

        # explanation
        text_expl = (Text("With two matrices with only one different column,\nby rearranging and shearing the parallelograms formed by the columns,\nwe discover that the total area of the parallelograms is the same as\nthe area of the parallelogram formed by the columns of\nthe matrix with the different columns added.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=6)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # change Total signed area to Signed area
        # fade out par2
        # restore par1
        v3.clear_updaters()
        v4.clear_updaters()
        par2.clear_updaters()
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl,
                          v3, v4, par2),
                  FadeOut(bgrect_text_total_area, text_total_area),
                  FadeIn(bgrect_text_area),
                  Write(text_area),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))

        # restore text_area updater
        # restore bgrect_text_area updater
        text_area.add_updater(lambda m: m.become(
            Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                .shift(
                    LEFT*6.5 + UP*3.5
                    + RIGHT * Tex(
                        f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                    ).width/2)
        ))
        bgrect_text_area.add_updater(lambda m: m.become(
            BackgroundRectangle(
                Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                    .shift(
                        LEFT*6.5 + UP*3.5
                        + RIGHT * Tex(
                            f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                        ).width/2),
                buff=.2)
        ))


        # ---------------------------------------- #
        # Adding a multiple of a column to another #
        # ---------------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}+rA_{12}&A_{12}\\A_{21}+rA_{22}&A_{22}\end{vmatrix}=\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).scale(.6).shift(RIGHT*4.7+DOWN*3.4)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # a line
        line = Line(LEFT+UP*5, LEFT*6+DOWN*5)
        self.play(Create(line))

        # shear the parallelogram along the first column
        self.play(v2_x.animate.set_value(-4), v2_y.animate.set_value(-1))

        # explanation
        text_expl = (Text("Adding a multiple of column A to column B is equivalent to\nshearing the parallelogram along A,\nand its area remains the same.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # fade out the line
        # restore the parallelogram
        # stretch the axis by 1/2
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl,
                          line),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # ------------------------------------- #
        # Adding a multiple of a row to another #
        # ------------------------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}+rA_{21}&A_{12}+rA_{22}\\A_{21}&A_{22}\end{vmatrix}=\begin{vmatrix}A_{11}&A_{12}\\A_{21}&A_{22}\end{vmatrix}"
        ).scale(.6).shift(RIGHT*4.3+DOWN*3.4)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # shear the number plane
        self.play(v1_x.animate.set_value(4), v2_x.animate.set_value(-1.5),
                  plane.animate.apply_matrix([[1, 1.5], [0, 1]]))

        # explanation
        text_expl = (Text("Adding a multiple of row A to row B is equivalent to\nshearing the parallelogram along the B-axis,\nand its area remains the same.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        # restore the number plane
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v2_x.animate.set_value(-3),
                  plane.animate.apply_matrix([[1, -1.5], [0, 1]]))

        # ----------------------------------- #
        # The determinant of a matrix product #
        # ----------------------------------- #

        # the identity
        text_identity = MathTex(
            r"|AB|=|A||B|"
        ).shift(RIGHT*5.4+UP*3.5)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # transform the parallelogram to [1 0 ; 0 1]
        # change Signed area: 7.00 to Signed area: 1
        text_area.clear_updaters()
        bgrect_text_area.clear_updaters()
        text_area_alg = (Tex("Signed area: 1").shift(LEFT*6.5+UP*3.5))
        text_area_alg.shift(RIGHT * text_area_alg.width/2)
        bgrect_text_area_alg = BackgroundRectangle(text_area_alg, buff=.2)
        self.play(v1_x.animate.set_value(1), v1_y.animate.set_value(0),
                  v2_x.animate.set_value(0), v2_y.animate.set_value(1),
                  FadeOut(bgrect_text_area, text_area),
                  FadeIn(bgrect_text_area_alg),
                  Write(text_area_alg))
        self.wait(.5)

        # A = [1 -3 ; 2 1]
        # B = [1 -2 ; 1 -1]
        eq_A = MathTex(
            r"A=\begin{bmatrix}1&-3\\2&1\end{bmatrix}"
        ).shift(RIGHT*4+UP*2)
        eq_B = MathTex(
            r"B=\begin{bmatrix}1&-2\\1&-1\end{bmatrix}"
        ).shift(RIGHT*4)
        bgrect_eq_A = BackgroundRectangle(eq_A, buff=.2)
        bgrect_eq_B = BackgroundRectangle(eq_B, buff=.2)
        self.play(FadeIn(bgrect_eq_A, bgrect_eq_B),
                  Write(eq_A), Write(eq_B))

        # transform the parallelogram to [1 -3 ; 2 1]
        # change Signed area: 1 to Signed area: |A|
        text_area_alg2 = (Tex("Signed area: $|A|$").shift(LEFT*6.5+UP*3.5))
        text_area_alg2.shift(RIGHT * text_area_alg2.width/2)
        bgrect_text_area_alg2 = BackgroundRectangle(text_area_alg2, buff=.2)
        self.play(v1_x.animate.set_value(1), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1),
                  FadeOut(bgrect_text_area_alg, text_area_alg),
                  FadeIn(bgrect_text_area_alg2),
                  FadeIn(text_area_alg2))
        self.wait(.5)

        # transform the parallelogram to [1 -2 ; 1 -1] [1 -3 ; 2 1]
        # change Signed area: |A| to Signed area: |A||B|
        text_area_alg3 = (Tex("Signed area: $|A||B|$").shift(LEFT*6.5+UP*3.5))
        text_area_alg3.shift(RIGHT * text_area_alg3.width/2)
        bgrect_text_area_alg3 = BackgroundRectangle(text_area_alg3, buff=.2)
        self.play(v1_x.animate.set_value(-3), v1_y.animate.set_value(-1),
                  v2_x.animate.set_value(-5), v2_y.animate.set_value(-4),
                  FadeOut(bgrect_text_area_alg2, text_area_alg2),
                  FadeIn(bgrect_text_area_alg3),
                  FadeIn(text_area_alg3))
        self.wait(.5)

        # |A||B| = |AB|
        eq_AB = MathTex(
            r"|A||B|=|AB|"
        ).shift(LEFT*4+UP*2)
        bgrect_eq_AB = BackgroundRectangle(eq_AB, buff=.2)
        self.play(FadeIn(bgrect_eq_AB),
                  Write(eq_AB))

        # explanation
        text_expl = (Text("This is trivial from the definition of determinants\nas signed scaling factors.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=3)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        # restore the number plane
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl,
                          bgrect_text_area_alg3, text_area_alg3,
                          bgrect_eq_A, eq_A, bgrect_eq_B, eq_B,
                          bgrect_eq_AB, eq_AB),
                  FadeIn(bgrect_text_area),
                  Write(text_area),
                  v1_x.animate.set_value(1), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))

        # restore text_area updater
        # restore bgrect_text_area updater
        text_area.add_updater(lambda m: m.become(
            Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                .shift(
                    LEFT*6.5 + UP*3.5
                    + RIGHT * Tex(
                        f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                    ).width/2)
        ))
        bgrect_text_area.add_updater(lambda m: m.become(
            BackgroundRectangle(
                Tex(f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}")
                    .shift(
                        LEFT*6.5 + UP*3.5
                        + RIGHT * Tex(
                            f"Signed area: {rrnz(det_2d_vt(v1_x, v1_y, v2_x, v2_y), 2):.2f}"
                        ).width/2),
                buff=.2)
        ))


        # ----------------------- #
        # Upper triangular matrix #
        # ----------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&A_{12}\\0&A_{22}\end{vmatrix}=A_{11}A_{22}"
        ).shift(RIGHT*4.2+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # transform the parallelogram to [2 1 ; 0 3]
        self.play(v1_x.animate.set_value(2), v1_y.animate.set_value(0),
                  v2_x.animate.set_value(1), v2_y.animate.set_value(3))

        # explanation
        text_expl = (Text("The columns of an upper triangular matrix form\na parallelogram whose base lies on the x-axis,\nand its area is base times height, which is\nthe product of the entries on the main diagonal.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out the identity
        # fade out the explanation
        # restore the parallelogram
        self.play(FadeOut(bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl),
                  v1_x.animate.set_value(1), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(-3), v2_y.animate.set_value(1))


        # ----------------------- #
        # Lower triangular matrix #
        # ----------------------- #

        # the identity
        text_identity = MathTex(
            r"\begin{vmatrix}A_{11}&0\\A_{21}&A_{22}\end{vmatrix}=A_{11}A_{22}"
        ).shift(RIGHT*4.2+UP*3)
        bgrect_text_identity = BackgroundRectangle(text_identity, buff=.2)
        self.play(FadeIn(bgrect_text_identity), Write(text_identity))

        # transform the parallelogram to [2 0 ; 2 1]
        self.play(v1_x.animate.set_value(2), v1_y.animate.set_value(2),
                  v2_x.animate.set_value(0), v2_y.animate.set_value(1))

        # explanation
        text_expl = (Text("The columns of an upper triangular matrix form\na parallelogram whose base lies on the y-axis,\nand its area is base times height, which is\nthe product of the entries on the main diagonal.")
            .scale(.5).shift(DOWN*2))
        bgrect_text_expl = BackgroundRectangle(text_expl, buff=.2)
        self.play(FadeIn(bgrect_text_expl), Write(text_expl), run_time=5)
        self.wait(2)

        # fade out everything
        v1.clear_updaters()
        v2.clear_updaters()
        par.clear_updaters()
        text_area.clear_updaters()
        bgrect_text_area.clear_updaters()
        self.play(FadeOut(plane, plane_copy, v1, v2, par,
                          bgrect_text_area, text_area,
                          bgrect_text_identity, text_identity,
                          bgrect_text_expl, text_expl))


class DetIds2DTh(Scene):
    def construct(self):
        # a number plane
        plane = NumberPlane(y_range=(-64/9, 64/9, 1))

        # two vectors
        v1 = Vector([1, 2])
        v2 = Vector([-3, 1])

        # the parallelogram formed by the vectors
        par = Polygon(
            [0, 0, 0],
            [1, 2, 0],
            [-2, 3, 0],
            [-3, 1, 0],
            color=ORANGE)
        par.set_fill(ORANGE, .5)

        self.add(plane, v1, v2, par)
