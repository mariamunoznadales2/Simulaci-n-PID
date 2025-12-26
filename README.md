# Diseño y simulación de un PID térmico con sensor dinámico

En esta práctica se estudiará el diseño y la simulación de un sistema de control destinado a regular la temperatura en el interior de una pequeña cámara térmica o horno didáctico. El objetivo del sistema es mantener la temperatura en un valor deseado mediante la aplicación de una potencia eléctrica modulada a través de una resistencia calefactora. Este tipo de sistema presenta dinámica lenta, inercia térmica y comportamiento continuo, lo que lo convierte en un ejemplo ideal para el estudio de la teoría clásica de control. Los detalles de las instrucciones están detalladas en la memoria del trabajo: *CASO2 PID.pdf*.

Este repositorio contiene la implementación computacional del **Apartado B** del trabajo *Diseño y simulación de un lazo PID térmico con sensor dinámico*, desarrollado para la asignatura **Técnicas de Optimización y Control**, aparte del desarrollo analítico del **Apartado A**, en el archivo *CASO2 PID.pdf*.

La aplicación permite implementar y analizar el diseño analítico del controlador PID obtenido en el **Apartado A**, incorporando explícitamente la dinámica del sensor y proporcionando herramientas de simulación y visualización para el estudio del comportamiento dinámico del sistema.

---

## 1. Objetivo del Apartado B

El Apartado B tiene como objetivo trasladar el desarrollo teórico del Apartado A a una herramienta computacional interactiva que permita:

- Automatizar el diseño del controlador PID a partir de especificaciones temporales.
- Construir el sistema completo en lazo cerrado, incluyendo planta, sensor y controlador.
- Simular la respuesta temporal del sistema.
- Analizar la estabilidad y la dinámica mediante la visualización de polos.
- Estudiar el efecto de la variación de las ganancias del PID.
- Comparar directamente los dos casos de diseño planteados en el enunciado.

El Apartado B no introduce nuevos criterios de diseño, sino que implementa de forma fiel las expresiones y razonamientos desarrollados analíticamente.

---

## 2. Estructura del proyecto

El código se ha organizado de forma modular para separar claramente cada parte del problema:

CASO 2 PID/

 app.py  # Interfaz interactiva (Apartado B.3)

 diseno_pid.py  # Diseño automático del PID (Apartado B.1)

 modelo_sistema.py  # Modelo del sistema en lazo cerrado (Apartado B.2)

 simulaciones.py  # Simulación temporal y análisis de polos (Apartado B.2)
 
 CASO 2 PID.pdf  # Desarrollo analítico (Apartado A) y memoria del proyecto



Esta estructura facilita la comprensión del código y refleja directamente la organización del trabajo escrito.

---

## 3. Apartado B.1 – Diseño automático del PID

**Archivo:** `diseno_pid.py`

Este módulo implementa el procedimiento de diseño del controlador PID desarrollado en el Apartado A.

A partir de las especificaciones temporales (sobreoscilación y tiempo de establecimiento) y de los parámetros físicos del sistema, el módulo:

1. Calcula los parámetros equivalentes de un modelo de segundo orden de referencia.
2. Selecciona un polo adicional más rápido para garantizar la dominancia del segundo orden.
3. Obtiene las ganancias del controlador PID mediante la igualación de coeficientes del polinomio característico.

El resultado es un conjunto de ganancias coherente con el diseño analítico y reproducible para distintos valores de las especificaciones.

---

## 4. Apartado B.2 – Modelo del sistema y simulación

### 4.1 Construcción del sistema en lazo cerrado  
**Archivo:** `modelo_sistema.py`

En este módulo se construye el sistema dinámico completo utilizando funciones de transferencia:

- Planta térmica.
- Sensor con dinámica propia.
- Controlador PID continuo.

Los tres bloques se conectan para formar el lazo abierto, y posteriormente se aplica realimentación negativa para obtener el sistema en lazo cerrado. Esta estructura coincide exactamente con la analizada en el Apartado A.

---

### 4.2 Simulación temporal y análisis de polos  
**Archivo:** `simulaciones.py`

Este módulo proporciona funciones para:

- Simular la respuesta temporal del sistema en lazo cerrado ante una entrada escalón.
- Calcular los polos del sistema.

La combinación de ambas herramientas permite relacionar directamente la respuesta observada con la ubicación de los polos en el plano complejo.

---

## 5. Apartado B.3 – Interfaz interactiva

**Archivo:** `app.py`

El archivo `app.py` integra todos los módulos anteriores en una aplicación interactiva desarrollada con **Streamlit**.

### Funcionalidades principales

#### Parámetros físicos comunes
El usuario puede introducir los parámetros físicos del sistema, que se mantienen constantes para todos los análisis realizados en la aplicación.

#### Casos de diseño
Se han implementado dos pestañas independientes, correspondientes a los dos casos de estudio definidos en el enunciado:

- **Caso 1:** mayor sobreoscilación permitida y mayor tiempo de establecimiento.
- **Caso 2:** menor sobreoscilación y respuesta más rápida.

En cada caso se muestran:
- Los parámetros del modelo de segundo orden equivalente.
- Las ganancias del PID obtenidas mediante el diseño analítico.
- La respuesta temporal del sistema.
- Los polos del sistema en el plano complejo.

#### Análisis de variación de ganancias
Para estudiar el efecto de cada término del controlador, se han añadido controles deslizantes que permiten modificar de forma independiente las ganancias proporcional, integral y derivativa alrededor del diseño base. Este análisis tiene un carácter cualitativo y no persigue la obtención de un nuevo ajuste numérico.

Esto permite observar en tiempo real:
- Cómo cambia la forma de la respuesta temporal.
- Cómo se desplazan los polos del sistema.
- Cómo se ve afectada la estabilidad relativa.

Esta funcionalidad implementa directamente el análisis solicitado en el Apartado B.3 del enunciado.

---

## 6. Comparación entre casos de diseño

Además de los requisitos mínimos, se ha incorporado una pestaña de comparación que muestra:

- La respuesta temporal de ambos casos en una misma gráfica.
- La ubicación de los polos correspondientes a cada caso, representados de forma diferenciada.

Esta comparación permite analizar de forma clara el impacto de especificaciones más exigentes sobre la dinámica del sistema y refuerza el análisis cualitativo realizado en el Apartado A.

---

## 7. Ejecución de la aplicación

streamlit run app.py

## 8. Conclusión
La herramienta desarrollada implementa de forma fiel el diseño analítico del controlador PID y permite validar y analizar el comportamiento dinámico del sistema mediante simulación. La combinación de modelado, simulación y visualización interactiva proporciona una comprensión clara de la relación entre las especificaciones temporales, las ganancias del controlador y la dinámica del sistema en lazo cerrado.

El Apartado B no solo valida el diseño teórico, sino que lo complementa con un análisis dinámico y comparativo que refuerza los conceptos fundamentales de control automático.
