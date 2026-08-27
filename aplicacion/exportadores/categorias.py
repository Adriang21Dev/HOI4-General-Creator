def exportar_categoria(nombre_mod):

    id_mod = nombre_mod

    return f"""
{id_mod} = {{
    icon = generic_political_actions

    visible = {{
        is_ai = no
    }}

    priority = 1000
}}
"""