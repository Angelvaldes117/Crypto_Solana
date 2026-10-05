import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tasks import (
    consultar_velas,
    generar_grafica,
    generar_excel,
    consultar_periodo_sin_datos
)
import time


def esperar_tarea(resultado, nombre):
    print("\n" + "=" * 70)
    print(nombre)
    print("=" * 70)

    print(f"ID: {resultado.id}")
    print(f"Estado inicial: {resultado.state}")

    inicio = time.perf_counter()

    while not resultado.ready():
        print(f"Estado actual: {resultado.state}")
        time.sleep(1)

    duracion_total = time.perf_counter() - inicio

    print(f"Estado final: {resultado.state}")
    print(f"Duración observada: {duracion_total:.4f} segundos")

    if resultado.successful():
        print("Resultado:")
        print(resultado.result)
        return True

    print("Error:")
    print(resultado.result)
    return False


print("=" * 70)
print("ACTIVIDAD 19 - PROCESAMIENTO EN SEGUNDO PLANO CON CELERY")
print("=" * 70)

# --------------------------------------------------
# TAREA 1 - CONSULTA DE VELAS
# --------------------------------------------------

tarea_consulta = consultar_velas.delay()

consulta_correcta = esperar_tarea(
    tarea_consulta,
    "TAREA 1 - CONSULTA DE VELAS"
)

# Las siguientes tareas solamente se envían si existen datos válidos.

if consulta_correcta:

    # ----------------------------------------------
    # TAREA 2 - GENERACIÓN DE GRÁFICA
    # ----------------------------------------------

    tarea_grafica = generar_grafica.delay()

    grafica_correcta = esperar_tarea(
        tarea_grafica,
        "TAREA 2 - GENERACIÓN DE GRÁFICA"
    )

    # ----------------------------------------------
    # TAREA 3 - GENERACIÓN DEL EXCEL
    # ----------------------------------------------

    tarea_excel = generar_excel.delay()

    excel_correcto = esperar_tarea(
        tarea_excel,
        "TAREA 3 - GENERACIÓN DEL INFORME EXCEL"
    )

else:
    print(
        "\nNo se generaron la gráfica ni el Excel "
        "porque la consulta no produjo datos válidos."
    )


print("\n" + "=" * 70)
print("PRUEBA DE MANEJO DE ERRORES - PERÍODO SIN DATOS")
print("=" * 70)

tarea_error = consultar_periodo_sin_datos.delay()

esperar_tarea(
    tarea_error,
    "CONSULTA DE UN PERÍODO SIN DATOS"
)

print("\nComprobación:")
print(
    "La aplicación detectó que el período solicitado no contiene "
    "datos y evitó generar un reporte engañoso."
)

print("\n" + "=" * 70)
print("ACTIVIDAD 19 FINALIZADA")
print("=" * 70)