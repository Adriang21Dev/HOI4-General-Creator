from utilidades import limpiar_nombre

class General:

    def __init__(
        self,
        nombre="",
        ataque=0,
        defensa=0,
        planificacion=0,
        logistica=0,
        retrato="",
        traits=None
    ):
        self.nombre = nombre
        self.id = limpiar_nombre(nombre)
        self.ataque = ataque
        self.defensa = defensa
        self.planificacion = planificacion
        self.logistica = logistica
        self.retrato = retrato

        if traits is None:
            traits = []
        self.traits = traits

    def convertir_decision(self):
        traits_texto ="\n               ".join(self.traits)

        return f"""

        create_corps_commander = {{
            name = "{self.nombre}"
            portrait_path = "gfx/interface/portraits/characters/{self.nombre}.dds"
            traits = {{
                {traits_texto}
            }}
            skill = 1
            attack_skill = {self.ataque}
            defense_skill = {self.defensa}
            planning_skill = {self.planificacion}
            logistics_skill = {self.logistica}
            }}
"""