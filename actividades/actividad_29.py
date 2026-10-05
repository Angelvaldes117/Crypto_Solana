from tasks import actualizar_reporte_4_semanas
import time
import os
import pandas as pd


print("=" * 70)
print("ACTIVIDAD 29 - ACTUALIZACIÓN DEL REPORTE CON CELERY")
print("=" * 70)


# ==========================================================
# 1. ENVIAR TAREA A CELERY
# ==========================================================

print("\nEnviando actualización del reporte a Celery...")

inicio = time.perf_counter()

tarea = actualizar_reporte_4_semanas.delay()


print(f"\nID de la tarea: {tarea.id}")
print(f"Estado inicial: {tarea.state}")


# ==========================================================
# 2. CONSULTAR ESTADO
# ==========================================================

ultimo_estado = None

while not tarea.ready():

    estado = tarea.state

    if estado != ultimo_estado:

        print(
            f"Estado actual: {estado}"
        )

        ultimo_estado = estado

    time.sleep(1)


duracion_observada = (
    time.perf_counter() - inicio
)


# ==========================================================
# 3. RESULTADO
# ==========================================================

print(
    f"\nEstado final: {tarea.state}"
)

print(
    "Duración observada: "
    f"{duracion_observada:.4f} segundos"
)


if tarea.successful():

    resultado = tarea.result

    print("\nRESULTADO DE CELERY")

    print(
        f"Archivo: "
        f"{resultado['archivo']}"
    )

    print(
        f"Registros anteriores: "
        f"{resultado['registros_anteriores']}"
    )

    print(
        f"Registros actuales: "
        f"{resultado['registros_actuales']}"
    )

    print(
        f"Registros agregados: "
        f"{resultado['registros_agregados']}"
    )

    print(
        "Fecha de generación anterior: "
        f"{resultado['fecha_generacion_anterior']}"
    )

    print(
        "Fecha de generación actual: "
        f"{resultado['fecha_generacion_actual']}"
    )

    print(
        "Duración interna de la tarea: "
        f"{resultado['duracion_segundos']} segundos"
    )

else:

    print("\nERROR EN LA TAREA")
    print(tarea.result)

    raise RuntimeError(
        "No fue posible actualizar el reporte."
    )


# ==========================================================
# 4. VERIFICAR REPORTE GENERADO
# ==========================================================

archivo = (
    "reportes/actividad_29_reporte_actualizado.xlsx"
)

if not os.path.exists(archivo):

    raise FileNotFoundError(
        "Celery indicó éxito, pero no se encontró "
        "el reporte actualizado."
    )


print("\n" + "=" * 70)
print("COMPROBACIÓN DEL REPORTE ACTUALIZADO")
print("=" * 70)


excel = pd.ExcelFile(
    archivo
)

print("\nHojas encontradas:")

for hoja in excel.sheet_names:
    print(f" - {hoja}")


# ==========================================================
# 5. RELEER DATOS
# ==========================================================

velas = pd.read_excel(
    archivo,
    sheet_name="Velas_SOL"
)

comparacion = pd.read_excel(
    archivo,
    sheet_name="Comparacion_reportes"
)

metadatos = pd.read_excel(
    archivo,
    sheet_name="Metadatos"
)


print("\nREGISTROS RECUPERADOS")

print(
    f"Velas_SOL: {len(velas)} registros"
)

print(
    f"Comparacion_reportes: "
    f"{len(comparacion)} registros"
)

print(
    f"Metadatos: "
    f"{len(metadatos)} registros"
)


# ==========================================================
# 6. COMPROBAR CANTIDAD
# ==========================================================

esperados = 672

print("\nCOMPROBACIÓN DE REGISTROS")

print(
    f"Registros esperados: {esperados}"
)

print(
    f"Registros encontrados: {len(velas)}"
)


if len(velas) == esperados:

    print(
        "OK - La actualización contiene "
        "los 672 registros de las cuatro semanas."
    )

else:

    print(
        "ADVERTENCIA - La cantidad de registros "
        "es diferente de 672."
    )


print("\n" + "=" * 70)
print("ACTIVIDAD 29 FINALIZADA")
print("=" * 70)