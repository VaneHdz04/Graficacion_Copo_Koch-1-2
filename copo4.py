import turtle
import math

# --- Parámetros ---
NIVEL = 4        # profundidad del fractal
LONGITUD = 400   # longitud inicial

# --- Función recursiva: genera los puntos de la curva de Koch ---
def trace_koch(order, length, heading, x, y, pts):
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

# --- Construir los dos lados superiores del copo ---
def build_two_sides(order, length, start=(-200, -50), heading=60):
    pts = [start]
    x, y = start
    hdg = heading
    x, y, hdg = trace_koch(order, length, hdg, x, y, pts)  # lado 1
    hdg -= 120                                            # giro
    x, y, hdg = trace_koch(order, length, hdg, x, y, pts) # lado 2
    return pts

# --- Dibujar puntos con un corte horizontal ---
def draw_clipped(t, pts, y_limit):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]

        # Caso 1: ambos arriba → dibujar completo
        if y1 >= y_limit and y2 >= y_limit:
            t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)
            continue

        # Caso 2: ambos abajo → no dibujar
        if y1 < y_limit and y2 < y_limit:
            continue

        # Caso 3: cruza la línea → calcular intersección
        dy = y2 - y1
        dx = x2 - x1
        if dy != 0:
            t_cross = (y_limit - y1) / dy
            x_cross = x1 + t_cross * dx
            y_cross = y_limit
            if y1 >= y_limit:
                t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x_cross, y_cross)
            else:
                t.penup(); t.goto(x_cross, y_cross); t.pendown(); t.goto(x2, y2)

# ---------------- MAIN ----------------
# Configuración de ventana
screen = turtle.Screen()
screen.bgcolor("black")

# Configuración de la tortuga
t = turtle.Turtle()
t.speed(0)
t.color("cyan")
t.hideturtle()

# Generar puntos del fractal
pts = build_two_sides(NIVEL, LONGITUD)

# Calcular la línea de corte
ys = [p[1] for p in pts]
Y_LIMIT = (max(ys) + min(ys)) / 2.0 - 60

# Dibujar el fractal con recorte
draw_clipped(t, pts, Y_LIMIT)

# (Opcional) dibujar línea de corte
t.color("black")
t.penup(); t.goto(min(p[0] for p in pts) - 20, Y_LIMIT)
t.setheading(0); t.pendown()
t.forward((max(p[0] for p in pts) - min(p[0] for p in pts)) + 40)

turtle.done()
