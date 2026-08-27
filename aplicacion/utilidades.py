import re

def limpiar_nombre(nombre):
    nombre = re.sub(r"[^\w]", "_", nombre)
    nombre = re.sub(r"_+", "_", nombre)
    nombre = nombre.strip("_")
    return nombre