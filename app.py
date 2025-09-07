from flask import Flask, jsonify, render_template, send_file
import math
import matplotlib.pyplot as plt

app = Flask(__name__)

# ---------------- FUNCIONES ----------------
def trace_koch(order, length, heading, x, y, pts):
    """Genera los puntos de la curva de Koch recursivamente"""
    if order == 0:
        rad = math.radians(heading)
        x2 = x + length * math.cos(rad)
        y2 = y + length * math.sin(rad)
        pts.append((x2, y2))
        return x2, y2, heading
    else:
        order -= 1
        length /= 3.0
        x, y, heading = trace_koch(order, length, heading, x, y, pts)
        heading += 60
        x, y, heading = trace_koch(order, length, heading, x, y, pts)
        heading -= 120
        x, y, heading = trace_koch(order, length, heading, x, y, pts)
        heading += 60
        x, y, heading = trace_koch(order, length, heading, x, y, pts)
        return x, y, heading

def build_two_sides(order, length, start=(-200, -50), heading=60):
    """Genera los dos lados superiores del copo de Koch"""
    pts = [start]
    x, y = start
    hdg = heading
    x, y, hdg = trace_koch(order, length, hdg, x, y, pts)  # lado 1
    hdg -= 120                                            # giro para lado 2
    x, y, hdg = trace_koch(order, length, hdg, x, y, pts) # lado 2
    return pts

def clip_points(pts, y_limit):
    """Aplica el recorte horizontal, como draw_clipped en Turtle"""
    clipped = []
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]

        # ambos arriba → dibujar completo
        if y1 >= y_limit and y2 >= y_limit:
            clipped.append((x1, y1))
            clipped.append((x2, y2))
            continue

        # ambos abajo → no dibujar
        if y1 < y_limit and y2 < y_limit:
            continue

        # cruza la línea → calcular intersección
        dy = y2 - y1
        dx = x2 - x1
        if dy != 0:
            t_cross = (y_limit - y1) / dy
            x_cross = x1 + t_cross * dx
            y_cross = y_limit
            if y1 >= y_limit:
                clipped.append((x1, y1))
                clipped.append((x_cross, y_cross))
            else:
                clipped.append((x_cross, y_cross))
                clipped.append((x2, y2))
    return clipped

def build_fractal(order, length):
    """Genera los puntos finales del fractal con recorte"""
    pts = build_two_sides(order, length)
    ys = [p[1] for p in pts]
    y_limit = (max(ys) + min(ys)) / 2.0 - 60
    clipped_pts = clip_points(pts, y_limit)
    return clipped_pts

def save_fractal_as_png(pts, color, filename="static/fractal.png"):
    plt.figure(figsize=(6,6), facecolor="black")
    xs, ys = zip(*pts)
    plt.plot(xs, ys, color=color)
    plt.axis("equal")
    plt.axis("off")
    plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="black")
    plt.close()

# ---------------- RUTAS ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/koch/<int:iterations>/<int:length>/<int:rapidez>/<string:color>")
def fractal(iterations, length, rapidez, color):
    pts = build_fractal(iterations, length)
    return jsonify({"points": pts, "rapidez": rapidez, "color": f"#{color}"})

@app.route("/export/<int:iterations>/<int:length>/<string:color>")
def export(iterations, length, color):
    pts = build_fractal(iterations, length)
    save_fractal_as_png(pts, f"#{color}")
    return send_file("static/fractal.png", mimetype="image/png", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
