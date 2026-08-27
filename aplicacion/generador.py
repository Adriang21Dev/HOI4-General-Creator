import os
from modelos import General
from archivos import crear_estructura
from archivos import guardar_decisiones
from archivos import guardar_categorias
from archivos import guardar_mod
from archivos import guardar_descriptor
from archivos import crear_traits_personalizados
from exportadores.decisiones import exportar_decision
from exportadores.categorias import exportar_categoria
from exportadores.gfx import importar_imagenes
from exportadores.launcher import exportar_descriptor
from exportadores.launcher import exportar_mod
from utilidades import limpiar_nombre



def crear_generales(
        ruta_salida,
        nombre_mod,
        retratos,
        datos_generales
):
    nombre_mod = limpiar_nombre(nombre_mod)

    contenido_generales = ""

    for retrato, datos in zip(retratos, datos_generales):

        nombre = os.path.splitext(
            os.path.basename(retrato)
        )[0]

        personaje = General(
            nombre=nombre,

            ataque=datos["ataque"],

            defensa=datos["defensa"],

            planificacion=datos["planificacion"],

            logistica=datos["logistica"],

            traits=datos["traits"]
        )

        contenido_generales += personaje.convertir_decision()

        #print("Voy a guardar el archivo...")
        #print(retrato)

        
    crear_estructura(
        ruta_salida,
        nombre_mod
    )

    contenido_generales = exportar_decision(
        nombre_mod,
        contenido_generales
    )

    contenido_categoria = exportar_categoria(
        nombre_mod
    )

    contenido_descriptor = exportar_descriptor(
        nombre_mod
    )

    contenido_mod = exportar_mod(
        nombre_mod
    )

    guardar_mod(
        ruta_salida,
        nombre_mod,
        contenido_mod
    )

    guardar_descriptor(
        ruta_salida,
        nombre_mod,
        contenido_descriptor
    )

    importar_imagenes(
        ruta_salida,
        nombre_mod,
        retratos
    )

    guardar_decisiones(
        ruta_salida,
        nombre_mod,
        contenido_generales
    )

    guardar_categorias(
        ruta_salida,
        nombre_mod,
        contenido_categoria
    )

    crear_traits_personalizados(
        ruta_salida,
        nombre_mod
    )