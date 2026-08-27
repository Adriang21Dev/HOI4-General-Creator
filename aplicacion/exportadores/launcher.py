

def exportar_descriptor(nombre_mod):

    return f'''version="1"

tags={{
    "Gameplay"
}}

name="{nombre_mod}"

supported_version="1.1*.*"

path="mod/{nombre_mod}"
'''

def exportar_mod(nombre_mod):

    return f'''version="1"

tags={{
    "Gameplay"
}}

name="{nombre_mod}"

supported_version="1.*.*"

path="mod/{nombre_mod}"
'''