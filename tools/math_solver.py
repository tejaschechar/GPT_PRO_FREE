from sympy import sympify, symbols, Eq, solve, diff, integrate


def solve_math(query: str):
    try:
        q = query.lower().strip()

        x = symbols('x')

        # 🧮 Equation solving
        if "=" in q:
            left, right = q.split("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)
            return f"Solution: {sol}"

        # 📈 Derivative
        if "derivative" in q:
            expr = q.replace("derivative of", "").strip()
            return f"Derivative: {diff(sympify(expr), x)}"

        # 📉 Integration
        if "integrate" in q:
            expr = q.replace("integrate", "").strip()
            return f"Integral: {integrate(sympify(expr), x)}"

        # ➗ Basic expression
        result = sympify(q)
        return f"Result: {result}"

    except Exception as e:
        return None