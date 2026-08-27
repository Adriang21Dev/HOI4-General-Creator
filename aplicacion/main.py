
from interfaz import iniciar
from archivos import obtener_retratos
from archivos import obtener_ruta_salida
from generador import crear_generales

def main():
    iniciar(
        obtener_retratos,
        obtener_ruta_salida,
        crear_generales
    )


if __name__ == "__main__":
    main()