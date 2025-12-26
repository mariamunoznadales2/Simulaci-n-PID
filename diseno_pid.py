
import numpy as np
from scipy.optimize import fsolve


def calcular_zeta(Mp):
    """
    Calcula el coeficiente de amortiguamiento zeta
    a partir de la sobreoscilación Mp (en tanto por uno).
    """

    def ecuacion(z):
        return np.exp(-np.pi * z / np.sqrt(1 - z**2)) - Mp

    zeta_inicial = 0.5
    zeta = fsolve(ecuacion, zeta_inicial)[0]
    return zeta


def diseñar_pid(Mp, ts, Cth, kp, Pmax, eta, Ks, tau_m, m=7):
    """
    Diseña el controlador PID usando el criterio de polos dominantes
    desarrollado en el Apartado A.
    """

    # Paso 1: parámetros del segundo orden
    zeta = calcular_zeta(Mp)
    omega_n = 4 / (zeta * ts)

    # Paso 2: polo no dominante
    p3 = m * zeta * omega_n

    # Paso 3: cálculo de ganancias PID
    KD = (Cth * tau_m * (2 * zeta * omega_n + p3)
          - (Cth + kp * tau_m)) / (Ks * eta * Pmax)

    KP = (Cth * tau_m * (omega_n**2 + 2 * zeta * omega_n * p3)
          - kp) / (Ks * eta * Pmax)

    KI = (Cth * tau_m * (omega_n**2 * p3)) / (Ks * eta * Pmax)

    return zeta, omega_n, p3, KP, KI, KD
