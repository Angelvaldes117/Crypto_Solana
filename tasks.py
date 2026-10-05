from celery_app import app

import MetaTrader5 as mt5
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os
import time


SIMBOLO = "SOLUSD"

INICIO = datetime(
    2026, 9, 25, 21, 0,
    tzinfo=timezone.utc
)

FIN = datetime(
    2026, 10, 2, 21, 0,
    tzinfo=timezone.utc
)


# ==========================================================
# TAREA 1 - CONSULTA DE VELAS
# ==========================================================

@app.task(bind=True)
def consultar_velas(self):
    inicio_tarea = time.perf_counter()

    if not mt5.initialize():
        raise RuntimeError(
            f"No se pudo iniciar MetaTrader 5: {mt5.last_error()}"
        )

    try:
        if not mt5.symbol_select(SIMBOLO, True):
            raise RuntimeError(
                f"No se pudo seleccionar {SIMBOLO}"
            )

        datos = mt5.copy_rates_range(
            SIMBOLO,
            mt5.TIMEFRAME_H1,
            INICIO,
            FIN
        )

        if datos is None or len(datos) == 0:
            raise ValueError(
                "La consulta no devolvió datos. "
                "No se generará un reporte."
            )

        df = pd.DataFrame(datos)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
            utc=True
        )

        archivo = "celery_velas_solana.csv"

        df.to_csv(
            archivo,
            index=False
        )

        duracion = time.perf_counter() - inicio_tarea

        return {
            "tarea": "Consulta de velas",
            "simbolo": SIMBOLO,
            "registros": len(df),
            "archivo": archivo,
            "duracion_segundos": round(duracion, 4)
        }

    finally:
        mt5.shutdown()


# ==========================================================
# TAREA 2 - GENERACIÓN DE GRÁFICA
# ==========================================================

@app.task(bind=True)
def generar_grafica(self):
    inicio_tarea = time.perf_counter()

    archivo = "celery_velas_solana.csv"

    if not os.path.exists(archivo):
        raise FileNotFoundError(
            "No existe celery_velas_solana.csv. "
            "Primero debe completarse la consulta de velas."
        )

    df = pd.read_csv(archivo)

    if df.empty:
        raise ValueError(
            "El archivo de datos está vacío."
        )

    df["time"] = pd.to_datetime(
        df["time"],
        utc=True
    )

    os.makedirs(
        "graficas",
        exist_ok=True
    )

    ruta = "graficas/actividad_19_celery_precio.png"

    plt.figure(
        figsize=(14, 7)
    )

    plt.plot(
        df["time"],
        df["close"],
        label="Precio de cierre"
    )

    plt.title(
        "SOLUSD - Consulta procesada con Celery\n"
        f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
        f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
    )

    plt.xlabel(
        "Fecha y hora (UTC)"
    )

    plt.ylabel(
        "Precio de cierre (USD)"
    )

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    duracion = time.perf_counter() - inicio_tarea

    return {
        "tarea": "Generación de gráfica",
        "archivo": ruta,
        "registros": len(df),
        "duracion_segundos": round(duracion, 4)
    }


# ==========================================================
# TAREA 3 - GENERACIÓN DEL INFORME EXCEL
# ==========================================================

@app.task(bind=True)
def generar_excel(self):
    inicio_tarea = time.perf_counter()

    archivo_csv = "celery_velas_solana.csv"

    if not os.path.exists(archivo_csv):
        raise FileNotFoundError(
            "No existen datos para generar el Excel."
        )

    df = pd.read_csv(
        archivo_csv
    )

    if df.empty:
        raise ValueError(
            "No se puede generar un reporte con datos vacíos."
        )

    df["time"] = pd.to_datetime(
        df["time"],
        utc=True
    )

    # Excel no admite fechas con zona horaria.
    # Se crea una copia sin timezone únicamente para Excel.
    df_excel = df.copy()

    df_excel["time"] = (
        df_excel["time"]
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
    )

    os.makedirs(
        "reportes",
        exist_ok=True
    )

    ruta = "reportes/actividad_19_reporte.xlsx"

    metadatos = pd.DataFrame({
        "Campo": [
            "Símbolo",
            "Temporalidad",
            "Período inicial UTC",
            "Período final UTC",
            "Cantidad de registros",
            "Generado mediante"
        ],
        "Valor": [
            SIMBOLO,
            "H1",
            str(df["time"].min()),
            str(df["time"].max()),
            len(df),
            "Celery"
        ]
    })

    with pd.ExcelWriter(
        ruta,
        engine="openpyxl"
    ) as writer:

        df_excel.to_excel(
            writer,
            sheet_name="Velas_SOL",
            index=False
        )

        metadatos.to_excel(
            writer,
            sheet_name="Metadatos",
            index=False
        )

    duracion = time.perf_counter() - inicio_tarea

    return {
        "tarea": "Generación de Excel",
        "archivo": ruta,
        "registros": len(df),
        "duracion_segundos": round(duracion, 4)
    }


# ==========================================================
# TAREA 4 - PRUEBA DE PERÍODO SIN DATOS
# ==========================================================

@app.task(bind=True)
def consultar_periodo_sin_datos(self):
    inicio_tarea = time.perf_counter()

    inicio = datetime(
        1971, 1, 1, 0, 0,
        tzinfo=timezone.utc
    )

    fin = datetime(
        1971, 1, 2, 0, 0,
        tzinfo=timezone.utc
    )

    if not mt5.initialize():
        raise RuntimeError(
            f"No se pudo iniciar MetaTrader 5: {mt5.last_error()}"
        )

    try:
        if not mt5.symbol_select(SIMBOLO, True):
            raise RuntimeError(
                f"No se pudo seleccionar {SIMBOLO}"
            )

        datos = mt5.copy_rates_range(
            SIMBOLO,
            mt5.TIMEFRAME_H1,
            inicio,
            fin
        )

        if datos is not None and len(datos) > 0:
            df = pd.DataFrame(datos)

            df["time"] = pd.to_datetime(
                df["time"],
                unit="s",
                utc=True
            )

            # Se verifica que los registros realmente
            # pertenezcan al período solicitado.
            df = df[
                (df["time"] >= inicio)
                & (df["time"] <= fin)
            ].copy()

        else:
            df = pd.DataFrame()

        if df.empty:
            duracion = time.perf_counter() - inicio_tarea

            raise ValueError(
                "No existen datos válidos de SOLUSD para el período "
                "1971-01-01 a 1971-01-02 UTC. "
                f"Duración de la consulta: {duracion:.4f} segundos. "
                "No se generó ningún reporte."
            )

        duracion = time.perf_counter() - inicio_tarea

        return {
            "tarea": "Consulta de período sin datos",
            "registros": len(df),
            "duracion_segundos": round(duracion, 4),
            "advertencia": (
                "Se encontraron datos válidos dentro del período solicitado."
            )
        }

    finally:
        mt5.shutdown()


# ==========================================================
# TAREA 5 - ACTUALIZACIÓN DEL REPORTE DE CUATRO SEMANAS
# ==========================================================

@app.task(bind=True)
def actualizar_reporte_4_semanas(self):
    inicio_tarea = time.perf_counter()

    archivo_anterior = "celery_velas_solana.csv"
    archivo_nuevo = "solana_4_semanas.csv"

    ruta_reporte_anterior = (
        "reportes/actividad_20_reporte_inicial.xlsx"
    )

    ruta_reporte_nuevo = (
        "reportes/actividad_29_reporte_actualizado.xlsx"
    )

    # ======================================================
    # COMPROBAR ARCHIVOS
    # ======================================================

    if not os.path.exists(archivo_anterior):
        raise FileNotFoundError(
            f"No se encontró {archivo_anterior}"
        )

    if not os.path.exists(archivo_nuevo):
        raise FileNotFoundError(
            f"No se encontró {archivo_nuevo}"
        )

    # ======================================================
    # CARGAR DATOS
    # ======================================================

    df_anterior = pd.read_csv(
        archivo_anterior
    )

    df_nuevo = pd.read_csv(
        archivo_nuevo
    )

    if df_anterior.empty:
        raise ValueError(
            "El archivo del período anterior está vacío."
        )

    if df_nuevo.empty:
        raise ValueError(
            "El archivo de cuatro semanas está vacío."
        )

    df_anterior["time"] = pd.to_datetime(
        df_anterior["time"],
        utc=True
    )

    df_nuevo["time"] = pd.to_datetime(
        df_nuevo["time"],
        utc=True
    )

    df_anterior = (
        df_anterior
        .sort_values("time")
        .reset_index(drop=True)
    )

    df_nuevo = (
        df_nuevo
        .sort_values("time")
        .reset_index(drop=True)
    )

    registros_anteriores = len(
        df_anterior
    )

    registros_nuevos = len(
        df_nuevo
    )

    diferencia_registros = (
        registros_nuevos
        - registros_anteriores
    )

    # ======================================================
    # FECHAS DE GENERACIÓN
    # ======================================================

    if os.path.exists(
        ruta_reporte_anterior
    ):

        fecha_anterior = datetime.fromtimestamp(
            os.path.getmtime(
                ruta_reporte_anterior
            ),
            tz=timezone.utc
        )

    else:
        fecha_anterior = None

    fecha_actualizacion = datetime.now(
        timezone.utc
    )

    # ======================================================
    # RESUMEN DIARIO
    # ======================================================

    df_nuevo["fecha"] = (
        df_nuevo["time"].dt.date
    )

    resumen_diario = (
        df_nuevo
        .groupby("fecha")
        .agg(
            apertura=("open", "first"),
            maximo=("high", "max"),
            minimo=("low", "min"),
            cierre=("close", "last"),
            volumen_ticks=("tick_volume", "sum"),
            velas=("time", "count")
        )
        .reset_index()
    )

    resumen_diario[
        "variacion_pct"
    ] = (
        (
            resumen_diario["cierre"]
            - resumen_diario["apertura"]
        )
        / resumen_diario["apertura"]
    ) * 100

    # ======================================================
    # MAYORES MOVIMIENTOS
    # ======================================================

    df_nuevo[
        "variacion_pct"
    ] = (
        df_nuevo["close"]
        .pct_change()
        * 100
    )

    df_nuevo[
        "movimiento_abs_pct"
    ] = (
        df_nuevo[
            "variacion_pct"
        ].abs()
    )

    mayores_movimientos = (
        df_nuevo
        .nlargest(
            10,
            "movimiento_abs_pct"
        )[
            [
                "time",
                "close",
                "variacion_pct",
                "movimiento_abs_pct",
                "tick_volume"
            ]
        ]
        .copy()
    )

    # ======================================================
    # COMPARACIÓN DE REPORTES
    # ======================================================

    comparacion = pd.DataFrame({
        "Campo": [
            "Registros reporte anterior",
            "Registros reporte actualizado",
            "Diferencia de registros",
            "Período anterior inicio",
            "Período anterior fin",
            "Período actualizado inicio",
            "Período actualizado fin",
            "Fecha generación anterior",
            "Fecha generación actual"
        ],

        "Valor": [
            registros_anteriores,
            registros_nuevos,
            diferencia_registros,

            str(
                df_anterior["time"].min()
            ),

            str(
                df_anterior["time"].max()
            ),

            str(
                df_nuevo["time"].min()
            ),

            str(
                df_nuevo["time"].max()
            ),

            (
                fecha_anterior.strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )
                if fecha_anterior
                else "No disponible"
            ),

            fecha_actualizacion.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        ]
    })

    # ======================================================
    # METADATOS
    # ======================================================

    metadatos = pd.DataFrame({
        "Campo": [
            "Instrumento",
            "Descripción",
            "Temporalidad",
            "Zona horaria",
            "Registros",
            "Período inicio",
            "Período fin",
            "Fuente",
            "Procesamiento",
            "Fecha de actualización"
        ],

        "Valor": [
            SIMBOLO,
            "Solana frente al dólar estadounidense",
            "H1",
            "UTC",
            registros_nuevos,
            str(
                df_nuevo["time"].min()
            ),
            str(
                df_nuevo["time"].max()
            ),
            "MetaTrader 5 - TIO Markets Demo",
            "Python, Pandas y Celery",
            fecha_actualizacion.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        ]
    })

    # ======================================================
    # PREPARAR DATOS PARA EXCEL
    # ======================================================

    # Excel no admite datetime con timezone.
    # Las copias siguientes conservan la misma hora UTC,
    # pero eliminan +00:00 antes de escribir el archivo.

    df_excel = df_nuevo.copy()

    df_excel["time"] = (
        df_excel["time"]
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
    )

    mayores_movimientos_excel = (
        mayores_movimientos.copy()
    )

    mayores_movimientos_excel["time"] = (
        mayores_movimientos_excel["time"]
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
    )

    # ======================================================
    # CREAR REPORTE
    # ======================================================

    os.makedirs(
        "reportes",
        exist_ok=True
    )

    with pd.ExcelWriter(
        ruta_reporte_nuevo,
        engine="openpyxl"
    ) as writer:

        df_excel.to_excel(
            writer,
            sheet_name="Velas_SOL",
            index=False
        )

        resumen_diario.to_excel(
            writer,
            sheet_name="Resumen_diario",
            index=False
        )

        mayores_movimientos_excel.to_excel(
            writer,
            sheet_name="Mayores_movimientos",
            index=False
        )

        comparacion.to_excel(
            writer,
            sheet_name="Comparacion_reportes",
            index=False
        )

        metadatos.to_excel(
            writer,
            sheet_name="Metadatos",
            index=False
        )

    # ======================================================
    # DURACIÓN Y RESULTADO
    # ======================================================

    duracion = (
        time.perf_counter()
        - inicio_tarea
    )

    return {
        "tarea": "Actualización del reporte",
        "archivo": ruta_reporte_nuevo,
        "registros_anteriores": registros_anteriores,
        "registros_actuales": registros_nuevos,
        "registros_agregados": diferencia_registros,

        "fecha_generacion_anterior": (
            fecha_anterior.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
            if fecha_anterior
            else "No disponible"
        ),

        "fecha_generacion_actual": (
            fecha_actualizacion.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        ),

        "duracion_segundos": round(
            duracion,
            4
        )
    }