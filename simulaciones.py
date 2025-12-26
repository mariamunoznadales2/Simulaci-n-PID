import numpy as np
import control as ctrl


def simular_escalon(T_cl, tiempo=50):
    """
    Simula la respuesta al escalón del sistema en lazo cerrado.
    """
    t = np.linspace(0, tiempo, 1000)
    t, y = ctrl.step_response(T_cl, t)
    return t, y


def obtener_polos(T_cl):
    """
    Devuelve los polos del sistema en lazo cerrado.
    """
    return ctrl.poles(T_cl)


def calcular_metricas_respuesta(t, y, tol=0.02):
    """
    Calcula métricas características de la respuesta al escalón:
    - y_inf: valor estacionario aproximado
    - Mp: sobreoscilación (en tanto por uno)
    - ts: tiempo de establecimiento según banda relativa tol (p.ej. 0.02 -> 2%)
    """
    y = np.asarray(y, dtype=float)
    t = np.asarray(t, dtype=float)

    y_inf = float(y[-1])
    if np.isclose(y_inf, 0.0):
        return y_inf, np.nan, np.nan

    y_max = float(np.max(y))
    Mp = max(0.0, (y_max - y_inf) / abs(y_inf))

    banda = tol * abs(y_inf)
    dentro = np.abs(y - y_inf) <= banda

    if not np.any(dentro):
        ts = np.nan
    else:
        idx_fuera = np.where(~dentro)[0]
        if len(idx_fuera) == 0:
            ts = float(t[0])
        else:
            ultimo_fuera = int(idx_fuera[-1])
            if ultimo_fuera + 1 < len(t):
                ts = float(t[ultimo_fuera + 1])
            else:
                ts = np.nan

    return y_inf, Mp, ts
