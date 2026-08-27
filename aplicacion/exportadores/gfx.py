import os
import shutil
def importar_imagenes(
    ruta_salida,
    nombre_mod,
    retratos
):
    ruta = os.path.join(
        ruta_salida,
        nombre_mod,
        "gfx",
        "interface",
        "portraits",
        "characters"
    )

    os.makedirs(ruta, exist_ok=True)

    for imagen in retratos:
        imagen_final= os.path.basename(imagen)
        destino = os.path.join(
            ruta,
            imagen_final)
        
        shutil.copy2(imagen, destino)

        #print(f"{imagen} -> {destino}")