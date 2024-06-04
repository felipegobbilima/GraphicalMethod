import numpy as np
import matplotlib.pyplot as plt
import re

def parse_constraint(constraint):
    pattern = r"([-+]?\d*\.?\d*)\s*x1?\s*([-+]?\d*\.?\d*)\s*x2?\s*([<>]=?)\s*([-+]?\d*\.?\d*)"
    match = re.match(pattern, constraint.replace(' ', ''))
    if not match:
        raise ValueError(f"Formato de restrição inválido: {constraint}")
    a, b, inequality, c = match.groups()
    a = float(a) if a else 1.0
    b = float(b) if b else 1.0
    c = float(c)
    return a, b, inequality, c

constraints = []
while True:
    constraint = input("Digite uma restrição (ex.: '1x1 + 2x2 <= 4') ou 'done' para finalizar: ")
    if constraint.lower() == 'done':
        break
    try:
        constraints.append(parse_constraint(constraint))
    except ValueError as e:
        print(e)
        continue

objective = input("Digite a função objetivo (ex.: '3x1 + 2x2'): ")
a_obj, b_obj = parse_constraint(objective + ' <= 0')[:2]

x1 = np.linspace(0, 10, 400)
x2 = np.linspace(0, 10, 400)
X1, X2 = np.meshgrid(x1, x2)

region = np.ones_like(X1, dtype=bool)

plt.figure(figsize=(10, 8))
for a, b, inequality, c in constraints:
    if inequality == '<=':
        y_vals = (c - a * x1) / b
        x_intercept = c / a if a != 0 else np.inf
        y_intercept = c / b if b != 0 else np.inf
        plt.plot(x1, y_vals, label=f'{a}*x1 + {b}*x2 <= {c}, Interseções: (x1={x_intercept:.2f}, x2=0), (x1=0, x2={y_intercept:.2f})')
        region &= (a * X1 + b * X2 <= c)
    elif inequality == '>=':
        y_vals = (c - a * x1) / b
        x_intercept = c / a if a != 0 else np.inf
        y_intercept = c / b if b != 0 else np.inf
        plt.plot(x1, y_vals, label=f'{a}*x1 + {b}*x2 >= {c}, Interseções: (x1={x_intercept:.2f}, x2=0), (x1=0, x2={y_intercept:.2f})')
        region &= (a * X1 + b * X2 >= c)

plt.imshow(region, extent=(0, 10, 0, 10), origin='lower', cmap='Greys', alpha=0.3)

plt.quiver(0, 0, a_obj, b_obj, angles='xy', scale_units='xy', scale=1, color='red', label='Vetor Gradiente')

plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(0, 11, 1))
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('x1')
plt.ylabel('x2')
plt.legend()
plt.title('Método Gráfico de Programação Linear')
plt.grid(True)

plt.savefig('grafico_programacao_linear.png')
plt.show()
