import base64
from io import BytesIO

import matplotlib
from flask import Flask, redirect, render_template, request, url_for
from sympy import Symbol, diff, simplify
from sympy.plotting import PlotGrid, plot

matplotlib.use("Agg")


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("base.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        user_inp = request.form.get("input")
        user_inp = str(user_inp).replace("**", "^")

        return redirect(url_for("input", expr=user_inp))


@app.route("/input/expr=<path:expr>")
def input(expr):
    try:
        var = Symbol("x")

        try:
            deriv = simplify(diff(expr, var))
            deriv = str(deriv).replace("**", "^")

        except (MemoryError, TypeError, ValueError) as error:
            return render_template(
                "index.html",
                func_error=f"{expr} (Invalid input!)",
                deriv_error=f"{error} (Error occurred!)",
            )

        p1 = plot(
            deriv,
            (var, -3, 3),
            xlabel="x",
            ylabel="y",
            title="(x from -3 to 3)",
            show=False,
        )
        p2 = plot(
            deriv,
            (var, -20, 20),
            xlabel="x",
            ylabel="y",
            title="(x from -20 to 20)",
            show=False,
        )

        fig = PlotGrid(2, 1, p1, p2, show=False)

        buf = BytesIO()
        fig.save(buf)
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

    except (IndexError, ValueError) as error:
        return render_template(
            "index.html",
            func=f"`{expr}`",
            deriv=f"`d/dx({expr}) = {deriv}`",
            plot_error=f"{error} (Error occurred!)",
        )

    else:
        return render_template(
            "index.html",
            func=f"`{expr}`",
            deriv=f"`d/dx({expr}) = {deriv}`",
            plot=f"data:image/png;base64,{data}",
        )


@app.errorhandler(Exception)
def exception_handler(error):
    return str(error) + "!!"


if __name__ == "__main__":
    app.run(debug=False)
