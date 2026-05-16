import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


class PlatformModel:
    def __init__(self):
        self.N = 1000
        self.alpha = 0.12
        self.beta = 0.08
        self.delta = 0.15
        self.mu = 0.05
        self.omega = 0.04
        self.rho = 0.02
        self.sigma0 = 0.85
        self.theta = 0.80

    def gamma(self, U, G, k):
        if U / self.N > self.theta:
            return k * (U / self.N - self.theta) * G
        return 0.0

    def system(self, t, S, k):
        U, D, A, G = S

        U = np.clip(U, 1e-6, self.N)
        D = max(D, 1e-6)
        A = np.clip(A, 1e-6, 0.999)
        G = np.clip(G, 1e-6, 1.0)

        g = self.gamma(U, G, k)
        Cs = self.sigma0 * np.exp(-1.5 * g) * (2 - G)

        dU = self.alpha * A * U * (1 - U / self.N) - Cs * U
        dD = self.beta * U - self.delta * g * D
        dA = np.log(1 + D) * (1 - A) - self.mu * A
        dG = self.rho * (1 - G) - self.omega * (U / self.N) * g * G

        return [dU, dD, dA, dG]

    def run(self, k):
        sol = solve_ivp(
            lambda t, y: self.system(t, y, k),
            (0, 400),
            [50, 5, 0.1, 1.0],
            t_eval=np.linspace(0, 400, 1000)
        )

        return sol


def main():
    model = PlatformModel()
    k_values = [0.5, 1.5, 3.0]

    plt.figure(figsize=(10, 6))

    for k in k_values:
        sol = model.run(k)
        U = sol.y[0]

        plt.plot(sol.t, U, label=f"k={k}")

    plt.title("Platform Dynamics under Regulatory Feedback")
    plt.xlabel("Time")
    plt.ylabel("User Capacity (U)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
