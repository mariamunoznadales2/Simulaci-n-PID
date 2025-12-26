import control as ctrl


def construir_lazo_cerrado(Cth, kp, Pmax, eta, Ks, tau_m, KP, KI, KD):
    """
    Construye el sistema en lazo cerrado T_cl(s)
    a partir de los parámetros físicos y del PID.
    """

    # Planta térmica
    G = ctrl.TransferFunction([eta * Pmax], [Cth, kp])

    # Sensor
    H = ctrl.TransferFunction([Ks], [tau_m, 1])

    # Controlador PID
    C = ctrl.TransferFunction([KD, KP, KI], [1, 0])

    # Lazo abierto
    L = C * G * H

    # Lazo cerrado
    T_cl = ctrl.feedback(L, 1)

    return T_cl
