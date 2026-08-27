
def exportar_decision(nombre_mod, contenido_generales):
    id_mod = nombre_mod
    return f"""
{id_mod} = {{

    recruit_{id_mod}_1 = {{
        icon = generic_political_actions

        allowed = {{
            always = yes
        }}

        available = {{
            always = yes
        }}

        visible = {{
            always = yes
        }}

        modifier = {{

        }}

        cost = 0

        fire_only_once = yes

        complete_effect = {{

{contenido_generales}

        }}
    }}
}}
"""
