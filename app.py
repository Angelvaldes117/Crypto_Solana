from celery_app import app as celery_app

from tasks import (
    consultar_velas,
    generar_grafica,
    generar_excel,
    consultar_periodo_sin_datos,
    actualizar_reporte_4_semanas
)


# ==========================================================
# MOSTRAR INFORMACIÓN DE UNA TAREA ENVIADA
# ==========================================================

def mostrar_tarea(tarea):

    print("\n" + "=" * 65)
    print("                    TAREA ENVIADA")
    print("=" * 65)

    print(f"\n ID     : {tarea.id}")
    print(f" Estado : {tarea.state}")

    print("\n La tarea fue enviada correctamente a Celery.")
    print(" Puede consultar su resultado utilizando la opción 5.")

    print("\n" + "-" * 65)
    input(" Presione ENTER para volver al menú...")


# ==========================================================
# MOSTRAR RESULTADO DE UNA TAREA
# ==========================================================

def mostrar_resultado(resultado):

    datos = resultado.result

    if isinstance(datos, dict):

        for clave, valor in datos.items():

            nombre = (
                clave
                .replace("_", " ")
                .capitalize()
            )

            print(f" {nombre:<20}: {valor}")

    else:

        print(f" {datos}")


# ==========================================================
# CONSULTAR ESTADO DE UNA TAREA
# ==========================================================

def consultar_estado():

    print("\n" + "=" * 65)
    print("                 CONSULTAR ESTADO DE TAREA")
    print("=" * 65)

    tarea_id = input(
        "\n Ingrese el ID de la tarea: "
    ).strip()

    if not tarea_id:

        print("\n [!] Debe ingresar un ID.")

        input(
            "\n Presione ENTER para volver al menú..."
        )

        return

    resultado = celery_app.AsyncResult(
        tarea_id
    )

    print("\n" + "=" * 65)
    print("                    ESTADO DE LA TAREA")
    print("=" * 65)

    print(f"\n ID     : {tarea_id}")
    print(f" Estado : {resultado.state}")

    # ------------------------------------------------------
    # PENDING
    # ------------------------------------------------------

    if resultado.state == "PENDING":

        print("\n" + "-" * 65)

        print(
            " [PENDIENTE] La tarea todavía no ha sido procesada."
        )

        print(
            "\n Verifique que Redis y el worker de Celery "
            "se encuentren activos."
        )

        print(
            " Si acaba de enviar la tarea, espere unos "
            "segundos e intente nuevamente."
        )

    # ------------------------------------------------------
    # STARTED
    # ------------------------------------------------------

    elif resultado.state == "STARTED":

        print("\n" + "-" * 65)

        print(
            " [EN PROCESO] Celery está ejecutando la tarea."
        )

    # ------------------------------------------------------
    # SUCCESS
    # ------------------------------------------------------

    elif resultado.state == "SUCCESS":

        print("\n" + "-" * 65)
        print("              OPERACIÓN COMPLETADA")
        print("-" * 65)

        mostrar_resultado(
            resultado
        )

        print("-" * 65)

        print(
            "\n [OK] La tarea terminó correctamente."
        )

    # ------------------------------------------------------
    # FAILURE
    # ------------------------------------------------------

    elif resultado.state == "FAILURE":

        print("\n" + "-" * 65)
        print("                 ERROR EN LA TAREA")
        print("-" * 65)

        print(
            f"\n {resultado.result}"
        )

        print(
            "\n [ERROR] Celery registró correctamente "
            "el fallo de la tarea."
        )

    # ------------------------------------------------------
    # OTRO ESTADO
    # ------------------------------------------------------

    else:

        print(
            f"\n Estado actual: {resultado.state}"
        )

        if resultado.ready():

            print("\n Resultado:")
            print("-" * 65)

            mostrar_resultado(
                resultado
            )

    print("\n" + "=" * 65)

    input(
        " Presione ENTER para volver al menú..."
    )


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

def mostrar_menu():

    print("\n" + "=" * 65)
    print("             SISTEMA DE ANÁLISIS DE SOLANA")
    print("=" * 65)

    print("          MetaTrader 5 | Celery | Redis | Python")

    print("-" * 65)

    print(" Símbolo      : SOLUSD")
    print(" Temporalidad : H1")

    print("=" * 65)

    print("\n CONSULTAS Y REPORTES\n")

    print(" [1] Consultar velas de SOLUSD")
    print(" [2] Generar gráfica de precios")
    print(" [3] Generar reporte Excel")
    print(" [4] Actualizar reporte de cuatro semanas")

    print("\n CELERY Y CONTROL\n")

    print(" [5] Consultar estado de una tarea")
    print(" [6] Probar manejo de período sin datos")

    print("\n [7] Salir")

    print("\n" + "=" * 65)


# ==========================================================
# APLICACIÓN PRINCIPAL
# ==========================================================

def main():

    while True:

        mostrar_menu()

        opcion = input(
            " Seleccione una opción: "
        ).strip()

        # ==================================================
        # OPCIÓN 1
        # CONSULTAR VELAS
        # ==================================================

        if opcion == "1":

            print("\n" + "-" * 65)
            print(" Enviando consulta de velas de SOLUSD...")
            print("-" * 65)

            tarea = consultar_velas.delay()

            mostrar_tarea(
                tarea
            )

        # ==================================================
        # OPCIÓN 2
        # GENERAR GRÁFICA
        # ==================================================

        elif opcion == "2":

            print("\n" + "-" * 65)
            print(" Enviando generación de gráfica...")
            print("-" * 65)

            tarea = generar_grafica.delay()

            mostrar_tarea(
                tarea
            )

        # ==================================================
        # OPCIÓN 3
        # GENERAR REPORTE EXCEL
        # ==================================================

        elif opcion == "3":

            print("\n" + "-" * 65)
            print(" Enviando generación del reporte Excel...")
            print("-" * 65)

            tarea = generar_excel.delay()

            mostrar_tarea(
                tarea
            )

        # ==================================================
        # OPCIÓN 4
        # ACTUALIZAR REPORTE
        # ==================================================

        elif opcion == "4":

            print("\n" + "-" * 65)

            print(
                " Enviando actualización del reporte "
                "de cuatro semanas..."
            )

            print("-" * 65)

            tarea = (
                actualizar_reporte_4_semanas
                .delay()
            )

            mostrar_tarea(
                tarea
            )

        # ==================================================
        # OPCIÓN 5
        # CONSULTAR ESTADO
        # ==================================================

        elif opcion == "5":

            consultar_estado()

        # ==================================================
        # OPCIÓN 6
        # PRUEBA SIN DATOS
        # ==================================================

        elif opcion == "6":

            print("\n" + "-" * 65)

            print(
                " Enviando prueba de período sin datos..."
            )

            print("-" * 65)

            tarea = (
                consultar_periodo_sin_datos
                .delay()
            )

            mostrar_tarea(
                tarea
            )

        # ==================================================
        # OPCIÓN 7
        # SALIR
        # ==================================================

        elif opcion == "7":

            print("\n" + "=" * 65)
            print("                  APLICACIÓN FINALIZADA")
            print("=" * 65)

            print(
                "\n Gracias por utilizar el Sistema "
                "de Análisis de Solana."
            )

            print()

            break

        # ==================================================
        # OPCIÓN INCORRECTA
        # ==================================================

        else:

            print("\n" + "-" * 65)

            print(
                " [!] Opción no válida."
            )

            print(
                " Seleccione un número del 1 al 7."
            )

            print("-" * 65)

            input(
                "\n Presione ENTER para continuar..."
            )


# ==========================================================
# INICIAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    main()