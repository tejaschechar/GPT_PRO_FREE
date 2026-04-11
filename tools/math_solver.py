from sympy import sympify, symbols, Eq, solve, diff, integrate

x = symbols('x')


def solve_math(query: str):
    try:
        q = query.strip()

        # 🧮 EQUATION SOLVING
        if "=" in q:
            left, right = q.split("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)
            return f"Solution: {sol}"

        q_lower = q.lower()

        # 📈 DERIVATIVE
        if "derivative" in q_lower:
            expr = q_lower.replace("derivative of", "").strip()
            return f"Derivative: {diff(sympify(expr), x)}"

        # 📉 INTEGRATION
        if "integrate" in q_lower:
            expr = q_lower.replace("integrate", "").strip()
            return f"Integral: {integrate(sympify(expr), x)}"

        # ➗ GENERAL EXPRESSION
        result = sympify(q)
        return f"Result: {result}"

    except Exception as e:
        return f"Math Error: {str(e)}"