import os
import re
import shutil
from tkinter import filedialog
from tkinter import messagebox


def obtener_ruta_salida():
    return filedialog.askdirectory(
        title="Seleccionar carpeta donde guardar el mod"
    )

def obtener_retratos():
    carpeta = filedialog.askdirectory(
        title= "Seleccionar carpeta de retratos"
    )
    if not carpeta:
        return []
    
    retratos = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".dds"):
            retratos.append(
                os.path.join(carpeta, archivo)
            )
    if not retratos:
        messagebox.showwarning(
            "Sin retratos",
            "No se encontraron archivos .dds en la carpeta seleccionada."
            )
    nombre_carpeta = os.path.basename(carpeta)

    return retratos, nombre_carpeta
def crear_estructura(ruta_salida, nombre_mod):

    carpeta_mod = os.path.join(
        ruta_salida,
        nombre_mod
    )

    carpetas = [
        "common",
        "common/decisions",
        "common/unit_leader",
        
        "common/decisions/categories",

        "gfx",
        "gfx/interface",
        "gfx/interface/portraits",
        "gfx/interface/portraits/characters",
        "gfx/interface/traits/personal",

        "interface",

        "localisation"
    ]

    for carpeta in carpetas:
        os.makedirs(
            os.path.join(carpeta_mod, carpeta),
            exist_ok=True
        )

    return carpeta_mod
def guardar_decisiones( ruta_salida, nombre_mod, contenido_generales):

    carpeta_mod = os.path.join(
        ruta_salida,
        nombre_mod
    )

    ruta = os.path.join(
        carpeta_mod,
        "common",
        "decisions",
        f"{nombre_mod}_decisions.txt"
    )

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_generales)
    print("Decisiones guardadas.")

def guardar_categorias(ruta_salida, nombre_mod, contenido_generales):

    carpeta_mod = os.path.join(
        ruta_salida,
        nombre_mod
    )

    ruta = os.path.join(
        carpeta_mod,
        "common",
        "decisions",
        "categories",
        f"{nombre_mod}_categories.txt"
    )

    

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_generales)

    print("Categorías guardadas.")

def guardar_mod(
    ruta_salida,
    nombre_mod,
    contenido_generales
):

    carpeta_mod= os.path.join(
        ruta_salida,
        nombre_mod
    )

    ruta = os.path.join(
        carpeta_mod,
        ruta_salida,
        f"{nombre_mod}.mod"
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido_generales)

    print(".mod guardado.")

def guardar_descriptor(
    ruta_salida,
    nombre_mod,
    contenido_generales
):
    nombre_carpeta = os.path.join(
        ruta_salida,
        nombre_mod
    )
    ruta = os.path.join(
        nombre_carpeta,
        "descriptor.mod"
    )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido_generales)

    print(".mod guardado.")

def crear_traits_personalizados(ruta_salida, nombre_mod):
    carpeta_mod = os.path.join(
        ruta_salida,
        nombre_mod
    )

    ruta_traits = os.path.join(
        carpeta_mod,
        "common",
        "unit_leader",
        "especialista_armamento.txt"
    )

    ruta_gfx = os.path.join(
        carpeta_mod,
        "interface",
        "especialista_armamento.gfx"
    )

    contenido_traits = """leader_traits = {

    especialista_en_armamento = {
        type = corps_commander

        trait_type = personality_trait

        gain_xp = {
            always = no
        }

        cost = 5

        modifier = {
            army_attack_factor = 1.0
			army_defence_factor = 1.2
            breakthrough_factor = 1.0
            max_commander_army_size = 26
            equipment_capture = 0.40
            forest = {
				movement = 0.4
				attack = 0.4
				defence = 0.4
            }
            mountain = {
				movement = 0.40
				attack = 0.40
				defence = 0.40
            }
        }

        ai_will_do = {
            factor = 0
        }
    }

    especialista_en_armamento_elite = {
        type = corps_commander

        trait_type = personality_trait

        gain_xp = {
            always = no
        }

        cost = 5

        modifier = {
            army_attack_factor = 6.0                # +100% Ataque
            army_defence_factor = 5.0             # +100% Defensa
            breakthrough_factor = 5.0      # +1000% Ruptura
            max_commander_army_size = 26
            equipment_capture = 0.80                     
            mountain = {
				movement = 0.80
				attack = 0.80
				defence = 0.80
			}
            forest = {
				movement = 0.8
				attack = 0.8
				defence = 0.8
            }  
        }

        ai_will_do = {
            factor = 0
        }
    }

}
"""

    contenido_gfx = """spriteTypes = {

    spriteType = {
        name = "GFX_trait_especialista_en_armamento"
        texturefile = "gfx/interface/traits/personal/especialista_en_armamento.dds"
    }

    spriteType = {
        name = "GFX_trait_especialista_en_armamento_elite"
        texturefile = "gfx/interface/traits/personal/especialista_en_armamento_elite.dds"
    }

}
"""

    with open(
        ruta_traits,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido_traits)

    with open(
        ruta_gfx,
        "w",
        encoding="utf-8"
    ) as archivo:
        archivo.write(contenido_gfx)

    carpeta_recursos = os.path.join(
        os.path.dirname(__file__),
        "recursos",
        "traits"
    )
    iconos = [
        "especialista_en_armamento.dds",
        "especialista_en_armamento_elite.dds"
    ]
    carpeta_destino = os.path.join(
        carpeta_mod,
        "gfx",
        "interface",
        "traits",
        "personal"
    )

    for icono in iconos:

        origen = os.path.join(
            carpeta_recursos,
            icono
        )

        destino = os.path.join(
            carpeta_destino,
            icono
        )

        if os.path.exists(origen):
            shutil.copy2(
                origen,
                destino
            )
        else:
            print(f"No se encontró el icono: {icono}")

    print("Traits personalizados creados.")

