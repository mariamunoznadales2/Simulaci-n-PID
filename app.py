import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from diseno_pid import diseñar_pid
from modelo_sistema import construir_lazo_cerrado
from simulaciones import simular_escalon, obtener_polos, calcular_metricas_respuesta





st.markdown(
    """
<style>
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Diseño y simulación de un PID térmico")

st.header("Parámetros físicos del sistema")

Cth = st.number_input("Capacidad térmica C_th", value=10.0)
kp = st.number_input("Pérdidas térmicas k_p", value=1.0)
Pmax = st.number_input("Potencia máxima P_max", value=100.0)
eta = st.number_input("Rendimiento η", value=0.9)
Ks = st.number_input("Ganancia del sensor K_s", value=1.0)
tau_m = st.number_input("Constante de tiempo del sensor τ_m", value=1.0)

st.subheader("Criterio de evaluación de $t_s$")
tol_opcion = st.selectbox("Banda de establecimiento", ["2%", "5%"], index=0)
tol = 0.02 if tol_opcion == "2%" else 0.05

tab1, tab2, tab3 = st.tabs(
    [
        "Caso 1 · Mp = 10%, ts = 8 s",
        "Caso 2 · Mp = 5%, ts = 5 s",
        "Comparación Caso 1 vs Caso 2",
    ]
)


def ejecutar_caso(Mp, ts, titulo, key_prefix):
    st.subheader(titulo)

    # === Diseño automático (Apartado A) ===
    zeta, omega_n, p3, KP0, KI0, KD0 = diseñar_pid(
        Mp, ts, Cth, kp, Pmax, eta, Ks, tau_m
    )

    st.markdown("### Diseño automático")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"ζ = {zeta:.3f}")
        st.write(f"ωₙ = {omega_n:.3f}")
    with col2:
        st.write(f"p₃ = {p3:.3f}")
    with col3:
        st.write(f"K_P = {KP0:.3f}")
        st.write(f"K_I = {KI0:.3f}")
        st.write(f"K_D = {KD0:.3f}")

    # =====================================================
    # SIMULACIÓN 1 — Respuesta temporal, polos y métricas
    # =====================================================
    st.markdown("### Simulación 1: respuesta temporal, polos y valores característicos")

    T_cl = construir_lazo_cerrado(
        Cth, kp, Pmax, eta, Ks, tau_m, KP0, KI0, KD0
    )

    t, y = simular_escalon(T_cl)
    polos = obtener_polos(T_cl)

    y_inf, Mp_med, ts_med = calcular_metricas_respuesta(t, y, tol=tol)

    colA, colB = st.columns(2)

    with colA:
        fig, ax = plt.subplots()
        ax.plot(t, y, label="Salida $y_m(t)$")
        ax.plot(t, np.ones_like(t), "--", label="Entrada (escalón)")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Señal")
        ax.grid()
        ax.legend()
        st.pyplot(fig)

    with colB:
        fig, ax = plt.subplots()
        ax.scatter(np.real(polos), np.imag(polos))
        ax.axhline(0)
        ax.axvline(0)
        ax.set_xlabel("Parte real")
        ax.set_ylabel("Parte imaginaria")
        ax.grid()
        st.pyplot(fig)

    colM1, colM2, colM3 = st.columns(3)
    with colM1:
        st.metric("Valor estacionario $y_\\infty$", f"{y_inf:.3f}")
    with colM2:
        st.metric("$M_p$ medido", f"{100*Mp_med:.2f}%")
    with colM3:
        ts_txt = "No definido" if np.isnan(ts_med) else f"{ts_med:.2f} s"
        st.metric(f"$t_s$ medido ({tol_opcion})", ts_txt)

    # =====================================================
    # SIMULACIÓN 2 — Variación independiente de una ganancia
    # =====================================================
    st.markdown("### Simulación 2: variación independiente de una ganancia")

    modo_var = st.radio(
        "Seleccione la ganancia a modificar:",
        ["K_P", "K_I", "K_D"],
        horizontal=True,
        key=f"{key_prefix}_modo",
    )

    escala = st.slider(
        "Factor de escala",
        0.2,
        2.0,
        1.0,
        key=f"{key_prefix}_escala",
    )

    KP, KI, KD = KP0, KI0, KD0
    if modo_var == "K_P":
        KP = escala * KP0
    elif modo_var == "K_I":
        KI = escala * KI0
    else:
        KD = escala * KD0

    T_var = construir_lazo_cerrado(
        Cth, kp, Pmax, eta, Ks, tau_m, KP, KI, KD
    )

    t_var, y_var = simular_escalon(T_var)
    polos_var = obtener_polos(T_var)

    colC, colD = st.columns(2)

    with colC:
        fig, ax = plt.subplots()
        ax.plot(t_var, y_var)
        ax.plot(t_var, np.ones_like(t_var), "--")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Señal")
        ax.grid()
        st.pyplot(fig)

    with colD:
        fig, ax = plt.subplots()
        ax.scatter(np.real(polos_var), np.imag(polos_var))
        ax.axhline(0)
        ax.axvline(0)
        ax.set_xlabel("Parte real")
        ax.set_ylabel("Parte imaginaria")
        ax.grid()
        st.pyplot(fig)
    
    return t, y, polos



with tab1:
    t1, y1, p1 = ejecutar_caso(
        Mp=0.10,
        ts=8.0,
        titulo="Caso 1: Mp = 10%, ts = 8 s",
        key_prefix="caso1",
    )

with tab2:
    t2, y2, p2 = ejecutar_caso(
        Mp=0.05,
        ts=5.0,
        titulo="Caso 2: Mp = 5%, ts = 5 s",
        key_prefix="caso2",
    )

with tab3:
    st.subheader("Comparación dinámica entre ambos casos")

    z1, w1, p3_1, KP1, KI1, KD1 = diseñar_pid(0.10, 8.0, Cth, kp, Pmax, eta, Ks, tau_m)
    z2, w2, p3_2, KP2, KI2, KD2 = diseñar_pid(0.05, 5.0, Cth, kp, Pmax, eta, Ks, tau_m)

    T1 = construir_lazo_cerrado(Cth, kp, Pmax, eta, Ks, tau_m, KP1, KI1, KD1)
    T2 = construir_lazo_cerrado(Cth, kp, Pmax, eta, Ks, tau_m, KP2, KI2, KD2)

    t1, y1 = simular_escalon(T1)
    t2, y2 = simular_escalon(T2)

    p1 = obtener_polos(T1)
    p2 = obtener_polos(T2)

    yinf1, Mp1m, ts1m = calcular_metricas_respuesta(t1, y1, tol=tol)
    yinf2, Mp2m, ts2m = calcular_metricas_respuesta(t2, y2, tol=tol)

    st.markdown("### Respuesta temporal comparada")
    fig, ax = plt.subplots()
    ax.plot(t1, y1, label="Caso 1 (Mp 10%, ts 8s)")
    ax.plot(t2, y2, label="Caso 2 (Mp 5%, ts 5s)")
    ax.plot(t1, np.ones_like(t1), "--", label="Entrada (escalón)")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Señal")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    st.markdown("### Comparación de polos")
    fig, ax = plt.subplots()
    ax.scatter(np.real(p1), np.imag(p1), label="Caso 1")
    ax.scatter(np.real(p2), np.imag(p2), label="Caso 2")
    ax.axhline(0)
    ax.axvline(0)
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginaria")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    st.markdown("### Valores característicos (medidos)")
    colc1, colc2 = st.columns(2)
    with colc1:
        st.write(f"**Caso 1:** $M_p$ = {100*Mp1m:.2f}\\%, $t_s$ ({tol_opcion}) = "
                 f"{'No definido' if np.isnan(ts1m) else f'{ts1m:.2f} s'}")
    with colc2:
        st.write(f"**Caso 2:** $M_p$ = {100*Mp2m:.2f}\\%, $t_s$ ({tol_opcion}) = "
                 f"{'No definido' if np.isnan(ts2m) else f'{ts2m:.2f} s'}")
