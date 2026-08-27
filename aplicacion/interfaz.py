import customtkinter as stk
import os
import sys
import random
import webbrowser
from tkinter import messagebox
import ctypes



def iniciar(
        funcion_obtener,
        funcion_ruta,
        funcion_crear,
):
    retratos=[]
    ruta_salida = ""

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("mi.empresa.miapp.1.0")
    ventana = stk.CTk()

# Icono de la ventana (formato .ico en Windows)
    if getattr(sys, "frozen", False):
        ruta_icono = os.path.join(
            sys._MEIPASS,
            "HOI4_General_Creator.ico"
        )
    else:
        ruta_icono = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "HOI4_General_Creator.ico"
        )

    ventana.iconbitmap(ruta_icono)
    ventana.title("HOI4 General Creator")
    ventana.geometry("700x600")

    frame_principal = stk.CTkScrollableFrame(ventana)
    frame_principal.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
    )
    frame_principal.focus_set()
    # ========================================================
    VELOCIDAD_FLECHAS = 2    # unidades por pulsación de flecha
    VELOCIDAD_PAG = 10       # unidades por AvPág / RePág

    def _desplazar(cantidad):
        """Mueve el scroll del canvas interno del CTkScrollableFrame."""
        frame_principal._parent_canvas.yview("scroll", cantidad, "units")

    def _foco_en_entry():
        """Devuelve True si el widget con el foco es un CTkEntry
        (para no robarte las flechas al editar texto)."""
        w = frame_principal.focus_get()
        return isinstance(w, stk.CTkEntry)

    def _flecha_arriba(event):
        if _foco_en_entry():
            return  # deja que el Entry mueva su cursor
        _desplazar(-VELOCIDAD_FLECHAS)

    def _flecha_abajo(event):
        if _foco_en_entry():
            return
        _desplazar(VELOCIDAD_FLECHAS)

    def _repag(event):
        _desplazar(-VELOCIDAD_PAG)

    def _avpag(event):
        _desplazar(VELOCIDAD_PAG)

    def _inicio(event):
        frame_principal._parent_canvas.yview("moveto", 0.0)

    def _fin(event):
        frame_principal._parent_canvas.yview("moveto", 1.0)

    # bind_all para que funcione sin importar qué widget tenga el foco
    ventana.bind_all("<Up>", _flecha_arriba, add="+")
    ventana.bind_all("<Down>", _flecha_abajo, add="+")
    ventana.bind_all("<Prior>", _repag, add="+")    # RePág
    ventana.bind_all("<Next>", _avpag, add="+")     # AvPág
    ventana.bind_all("<Home>", _inicio, add="+")    # Inicio
    ventana.bind_all("<End>", _fin, add="+")        # Fin

    
    frame_retratos = stk.CTkFrame(frame_principal)
    frame_retratos.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def donar():
        webbrowser.open("https://ko-fi.com/adriang21dev")

    boton_donar = stk.CTkButton(
        ventana,
        text="Apoyar el proyecto",
        command=donar,
        width=140,
        height=32
    )

    boton_donar.place(relx=0.96, x=-10, y=10, anchor="ne")

    #)

    def mostrar_tooltip(widget, texto):
        tooltip = None

        def entrar(event):
            nonlocal tooltip

            tooltip = stk.CTkToplevel(widget)
            tooltip.wm_overrideredirect(True)

            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty()

            tooltip.geometry(f"+{x}+{y}")

            label = stk.CTkLabel(
                tooltip,
                text=texto,
                justify="left",
                corner_radius=5
            )

            label.pack(
                padx=8,
                pady=5
            )

        def salir(event):
            nonlocal tooltip

            if tooltip is not None:
                tooltip.destroy()
                tooltip = None

        widget.bind(
            "<Enter>",
            entrar
        )

        widget.bind(
            "<Leave>",
            salir
        )

    def cargar_retratos():
        nonlocal retratos

        retratos, nombre_carpeta = funcion_obtener()

        if not retratos:
            label_estado_retratos.configure(
                text="Ninguna carpeta"
            )
            return

        label_estado_retratos.configure(
            text=(f"({len(retratos)}) Retratos de:\n{nombre_carpeta}")
    )

    label_estado_retratos = stk.CTkLabel(
    frame_retratos,
    text="Ninguna carpeta\nseleccionada"
    )
    label_estado_retratos.grid(row=1, column=1, padx=10, sticky="w")

    label_retrato =stk.CTkLabel(frame_retratos, text=(
    "Formato admitido: .dds\n"
    "Las imágenes .png, .jpg y .jpeg no serán importadas."
    )
    )
    label_retrato.grid(row=0, column=0, pady=10)

    selec_imagen = stk.CTkButton(
    frame_retratos, text="selecciona una carpeta\ncon imagenes", font=("Arial",16,"bold"), command=cargar_retratos
    )
    selec_imagen.grid(row=1, column=0, pady=10)


    frame_aleatorio = stk.CTkFrame(frame_principal)
    frame_aleatorio.grid(
        row=1,
        column=0,
        columnspan=2,
        padx=10,
        pady=10,
        sticky="ew"
    )
    ####################
    modo_generacion = stk.StringVar(value="manual")
    radio_manual = stk.CTkRadioButton(
        frame_aleatorio,
        text="Manual",
        variable=modo_generacion,
        value="manual",
        command=lambda: cambiar_modo()
    )
    radio_manual.grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    radio_aleatorio = stk.CTkRadioButton(
        frame_aleatorio,
        text="Aleatorio",
        variable=modo_generacion,
        value="aleatorio",
        command=lambda: cambiar_modo()
        )
    radio_aleatorio.grid(
        row=2,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    radio_aleatorio_personalizado = stk.CTkRadioButton(
        frame_aleatorio,
        text="Aleatorio + personalizados",
        variable=modo_generacion,
        value="aleatorio_personalizado",
        command=lambda: cambiar_modo()
    )
    radio_aleatorio_personalizado.grid(
        row=3,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    tooltip_manual = (
        "Manual\n\n"
        "Los atributos y rasgos son establecidos\n"
        "manualmente por el usuario.\n"
        "ESTOS SE APLICAN A TODOS LOS GENERALES,\n"
        "NO SE PUEDE EDITAR UNO POR UNO (al menos por ahora)."
    )

    tooltip_aleatorio = (
        "Aleatorio\n\n"
        "Los atributos y los rasgos se generan "
        "aleatoriamente para cada general.\n\n"
        "Se utilizan únicamente los 8 rasgos base."
    )

    tooltip_aleatorio_personalizado = (
        "Aleatorio + personalizados\n\n"
        "Los atributos y los rasgos se generan "
        "aleatoriamente para cada general.\n\n"
        "Se utilizan los 8 rasgos base y los 2 rasgos "
        "personalizados, para un total de 10 rasgos disponibles."
    )
    # =========================================================
# TOOLTIPS DE LOS MODOS DE GENERACIÓN
# =========================================================

    mostrar_tooltip(
        radio_manual,
        tooltip_manual
    )

    mostrar_tooltip(
        radio_aleatorio,
        tooltip_aleatorio
    )

    mostrar_tooltip(
        radio_aleatorio_personalizado,
        tooltip_aleatorio_personalizado
    )
    ###
    frame_atributos = stk.CTkFrame(frame_principal)
    frame_atributos.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=10,
        pady=15,
        sticky="ew"
    )
    frame_stats = stk.CTkFrame(frame_atributos)
    frame_stats.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="n"
    )

    frame_traits = stk.CTkFrame(frame_atributos)
    frame_traits.grid(
        row=0,
        column=1,
        padx=10,
        pady=10,
        sticky="n"
    )
    frame_traits.grid_columnconfigure(0, minsize=180)
    frame_traits.grid_columnconfigure(1, minsize=180)

    label_nombre_de_atributo = stk.CTkLabel(
        frame_stats,
        text="Atributos",
        font=("Arial",16,"bold")
    )
    label_nombre_de_atributo.grid(row=0, column=0, columnspan=2, pady=10)

    label_ataque = stk.CTkLabel(frame_stats, text="ataque", )
    label_ataque.grid(row=1, column=0, pady=2, padx=10, sticky="w")

    label_defensa = stk.CTkLabel(frame_stats, text="defensa")
    label_defensa.grid(row=2, column=0, pady=2, padx=10, sticky="w")

    label_planificacion = stk.CTkLabel(frame_stats, text="planificacion")
    label_planificacion.grid(row=3, column=0, pady=2, padx=10, sticky="w")

    label_logistica = stk.CTkLabel(frame_stats, text="logistica")
    label_logistica.grid(row=4, column=0, pady=2, padx=10, sticky="w")

    

    entry_ataque = stk.CTkEntry(frame_stats, width=60, placeholder_text="1-10")
    entry_ataque.grid(row=1, column=1, padx=10, pady=2)
    entry_ataque.bind(
        "<KeyRelease>",
        lambda event: limitar_maximo(entry_ataque)
    )

    entry_ataque.bind(
        "<FocusOut>",
        lambda event: corregir_minimo(entry_ataque)
    )
        

    entry_defensa = stk.CTkEntry(frame_stats, width=60, placeholder_text="1-10")
    entry_defensa.grid(row=2, column=1, padx=10, pady=2)
    entry_defensa.bind(
        "<KeyRelease>",
        lambda event: limitar_maximo(entry_defensa)
    )

    entry_defensa.bind(
        "<FocusOut>",
        lambda event: corregir_minimo(entry_defensa)
    )

    entry_planificacion = stk.CTkEntry(frame_stats, width=60, placeholder_text="1-10")
    entry_planificacion.grid(row=3, column=1, padx=10, pady=2)
    entry_planificacion.bind(
        "<KeyRelease>",
        lambda event: limitar_maximo(entry_planificacion)
    )

    entry_planificacion.bind(
        "<FocusOut>",
        lambda event: corregir_minimo(entry_planificacion)
    )

    entry_logistica = stk.CTkEntry(frame_stats, width=60, placeholder_text="1-10")
    entry_logistica.grid(row=4, column=1, padx=10, pady=2)
    entry_logistica.bind(
        "<KeyRelease>",
        lambda event: limitar_maximo(entry_logistica)
    )

    entry_logistica.bind(
        "<FocusOut>",
        lambda event: corregir_minimo(entry_logistica)
    )


# AQUÍ VAN LAS FUNCIONES
    def limitar_maximo(entry):
        texto = entry.get()

        if texto == "":
            return

        try:
            valor = int(texto)
        except ValueError:
            return

        if valor > 10:
            entry.delete(0, "end")
            entry.insert(0, "10")


    def corregir_minimo(entry):
        texto = entry.get()

        if texto == "":
            entry.insert(0, "1")
            return

        try:
            valor = int(texto)
        except ValueError:
            entry.delete(0, "end")
            entry.insert(0, "1")
            return

        if valor < 1:
            valor = 1

        entry.delete(0, "end")
        entry.insert(0, str(valor))

    ##
    label_trait = stk.CTkLabel(
        frame_traits,
        text="Rasgos",
        font=("Arial",16,"bold")
    )

    label_trait.grid(
        row=0,
        column=0,
        columnspan=2,
        padx=10,
        pady=(10, 2)
    )

    check_brilliant = stk.CTkCheckBox(
        frame_traits,
        text="Estratega brillante",
        width=180
    )
    check_brilliant.grid(row=1,column=0, padx=10, pady=2, sticky="w")

    check_panzer = stk.CTkCheckBox(
        frame_traits,
        text="Panzer Leader",
        width=180
    )
    check_panzer.grid(row=2,column=0, padx=10, sticky="w")

    check_infantry = stk.CTkCheckBox(
        frame_traits,
        text="líder de infantería",
        width=180
    )

    check_infantry.grid(row=3,column=0, padx=10, pady=2, sticky="w")

    check_commando = stk.CTkCheckBox(
        frame_traits,
        text="Commando",
        width=180
    )
    check_commando.grid(row=4,column=0, padx=10, sticky="w")

    ckeck_ingenieros = stk.CTkCheckBox(
        frame_traits,
        text="Ingenieros",
        width=180
    )
    ckeck_ingenieros.grid(row=1, column=1, padx=10, pady=2, sticky="w")

    ckeck_organizador= stk.CTkCheckBox(
        frame_traits,
        text="Organizador",
        width=180
    )
    ckeck_organizador.grid(row=2, column=1, padx=10, sticky="w")

    check_mago_de_la_logistica = stk.CTkCheckBox(
        frame_traits,
        text="Mago de la logistica",
        width=180
    )
    check_mago_de_la_logistica.grid(row=3, column=1, padx=10, pady=2, sticky="w")

    ckeck_adaptable = stk.CTkCheckBox(
        frame_traits,
        text="Adaptable",
        width=180
    )
    ckeck_adaptable.grid(
        row=4,
        column=1,
        padx=10,
        pady=2,
        sticky="w"
    )



    label_trait_personalizado = stk.CTkLabel(
        frame_traits,
        text="rasgos personalizados",
        font=("Arial",16,"bold")
    )

    label_trait_personalizado.grid(
        row=5,
        column=0,
        columnspan=2,
        padx=10,
        pady=(10, 2)
    )
    ckeck_especialista_armamento = stk.CTkCheckBox(
        frame_traits,
        text="Especialista en armamento",
        width=180
    )
    ckeck_especialista_armamento.grid(
        row=6,
        column=0,
        padx=10,
        sticky="w"
    )

    ckeck_especialista_armamento_elite = stk.CTkCheckBox(
        frame_traits,
        text="Especialista en armamento Elite",
        width=180
    )
    ckeck_especialista_armamento_elite.grid(
        row=6,
        column=1,
        padx=10,
        sticky="w"
    )
    ##
    # =========================================================
# DESCRIPCIONES DE LOS RASGOS
# =========================================================

    tooltip_brilliant = (
        "Estratega brillante\n"
        "Ataque: +1\n"
        "Planificación: +1"
    )

    tooltip_panzer = (
        "Panzer Leader\n"
        "Velocidad de blindado: +5.0%\n"
        "Ataque de blindado: +16.0%"
    )

    tooltip_infantry = (
        "Líder de infantería\n"
        "Defensa de infantería: 13.0%"
    )

    tooltip_commando = (
        "Commando\n"
        "Penalización de no combatiente sin suministros: -15.0%"
    )

    tooltip_trait_engineer = (
        "Ingenieros\n"
        "Río\n"
        "Ataque: +5.0%\n"
        "Fuerte\n"
        "Ataque: +10.0%"
    )

    tooltip_organizer = (
        "Organizador\n"
        "Velocidad de planificación: +10.0%"
    )

    tooltip_logistics = (
        "Mago de la logística\n"
        "Consumo de suministros: -15.0%"
    )

    tooltip_adaptable = (
        "Adaptable\n"
        "Factor de ganancia de aclimatación al frío: +10.0%\n"
        "Factor de ganancia de aclimatación al calor: +10.0%\n"
        "Reducción de penalizaciones de terreno: +30.0%"
    )

    tooltip_armamento = (
        "Especialista en armamento\n"
        "Ataque de divisiones: +100.0%\n"
        "Defensa de divisiones: +120.0%\n"
        "Índice de equipo capturado: +40.0%\n"
        "Tamaño máximo del ejército del general: +26\n"
        "Incursión: +100.00%\n"
        "Bosque\n"
        "Movimiento: +40.0%\n"
        "Ataque: +40.0\n"
        "Defensa: +40.0\n"
        "Montaña\n"
        "Movimiento: +40.0%\n"
        "Ataque: +40.0\n"
        "Defensa: +40.0"

    )

    tooltip_armamento_elite = (
        "Especialista en armamento Elite\n"
        "Ataque de divisiones: +600.0%\n"
        "Defensa de divisiones: +500.0%\n"
        "Índice de equipo capturado: +80.0%\n"
        "Tamaño máximo del ejército del general: +26\n"
        "Incursión: +500.00%\n"
        "Montaña\n"
        "Movimiento: +80.0%\n"
        "Ataque: +80.0\n"
        "Defensa: +80.0\n"
        "Bosque\n"
        "Movimiento: +80.0%\n"
        "Ataque: +80.0\n"
        "Defensa: +80.0"
    )
####################


# =========================================================
# TOOLTIPS
# =========================================================

    mostrar_tooltip(
        check_brilliant,
        tooltip_brilliant
    )

    mostrar_tooltip(
        check_panzer,
        tooltip_panzer
    )

    mostrar_tooltip(
        check_infantry,
        tooltip_infantry
    )

    mostrar_tooltip(
        check_commando,
        tooltip_commando
    )

    mostrar_tooltip(
        ckeck_ingenieros,
        tooltip_trait_engineer
    )

    mostrar_tooltip(
        ckeck_organizador,
        tooltip_organizer
    )

    mostrar_tooltip(
        check_mago_de_la_logistica,
        tooltip_logistics
    )

    mostrar_tooltip(
        ckeck_adaptable,
        tooltip_adaptable
    )

    mostrar_tooltip(
        ckeck_especialista_armamento,
        tooltip_armamento
    )

    mostrar_tooltip(
        ckeck_especialista_armamento_elite,
        tooltip_armamento_elite
    )
###############################
    traits_base = [
        "brilliant_strategist",
        "panzer_leader",
        "infantry_leader",
        "commando",
        "trait_engineer",
        "organizer",
        "logistics_wizard",
        "adaptable"
    ]

    traits_personalizados = [
        "especialista_en_armamento",
        "especialista_en_armamento_elite"
    ]

    
        # GENERACIÓN ALEATORIA
    # =========================================================

    def generar_estadisticas_aleatorias():
        ataque = random.randint(1, 10)
        defensa = random.randint(1, 10)
        planificacion = random.randint(1, 10)
        logistica = random.randint(1, 10)

        return ataque, defensa, planificacion, logistica

    def generar_cantidad_traits():
        cantidades = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ]

        pesos = [
            1,   # 1
            1,   # 2
            2,   # 3
            25,  # 4
            25,  # 5
            12,  # 6
            7,   # 7
            3,   # 8
            1,   # 9
            1    # 10
        ]

        return random.choices(
            cantidades,
            weights=pesos,
            k=1
        )[0]

    def generar_traits_aleatorios(
            incluir_personalizados=False
    ):
        traits_disponibles = traits_base.copy()

        if incluir_personalizados:
            traits_disponibles.extend(
                traits_personalizados
            )

        cantidad = generar_cantidad_traits()

        # La cantidad nunca puede superar la cantidad
        # real de rasgos disponibles.
        cantidad = min(
            cantidad,
            len(traits_disponibles)
        )

        return random.sample(
            traits_disponibles,
            cantidad
        )

    # =========================================================
    # ACTIVAR / DESACTIVAR CONTROLES SEGÚN EL MODO
    # =========================================================

    def cambiar_modo():
        modo = modo_generacion.get()

        if modo == "manual":

            entry_ataque.configure(state="normal")
            entry_defensa.configure(state="normal")
            entry_planificacion.configure(state="normal")
            entry_logistica.configure(state="normal")

            check_brilliant.configure(state="normal")
            check_panzer.configure(state="normal")
            check_infantry.configure(state="normal")
            check_commando.configure(state="normal")
            ckeck_ingenieros.configure(state="normal")
            ckeck_organizador.configure(state="normal")
            check_mago_de_la_logistica.configure(state="normal")
            ckeck_adaptable.configure(state="normal")

            ckeck_especialista_armamento.configure(
                state="normal"
            )
            ckeck_especialista_armamento_elite.configure(
                state="normal"
            )

        elif modo == "aleatorio":

            entry_ataque.configure(state="disabled")
            entry_defensa.configure(state="disabled")
            entry_planificacion.configure(state="disabled")
            entry_logistica.configure(state="disabled")

            check_brilliant.configure(state="disabled")
            check_panzer.configure(state="disabled")
            check_infantry.configure(state="disabled")
            check_commando.configure(state="disabled")
            ckeck_ingenieros.configure(state="disabled")
            ckeck_organizador.configure(state="disabled")
            check_mago_de_la_logistica.configure(state="disabled")
            ckeck_adaptable.configure(state="disabled")

            ckeck_especialista_armamento.configure(
                state="disabled"
            )
            ckeck_especialista_armamento_elite.configure(
                state="disabled"
            )

        elif modo == "aleatorio_personalizado":

            entry_ataque.configure(state="disabled")
            entry_defensa.configure(state="disabled")
            entry_planificacion.configure(state="disabled")
            entry_logistica.configure(state="disabled")

            check_brilliant.configure(state="disabled")
            check_panzer.configure(state="disabled")
            check_infantry.configure(state="disabled")
            check_commando.configure(state="disabled")
            ckeck_ingenieros.configure(state="disabled")
            ckeck_organizador.configure(state="disabled")
            check_mago_de_la_logistica.configure(state="disabled")
            ckeck_adaptable.configure(state="disabled")

            ckeck_especialista_armamento.configure(
                state="disabled"
            )
            ckeck_especialista_armamento_elite.configure(
                state="disabled"
            )

    # =========================================================
    # MOD
    # =========================================================

    frame_mod = stk.CTkFrame(frame_principal)
    frame_mod.grid(
        row=3,
        column=0,
        columnspan=2,
        padx=10,
        pady=15,
        sticky="ew"
    )
    def guardar():
        nombre_grupo = entry_grupo.get().strip()

        if not nombre_grupo:
            messagebox.showwarning(
                "Nombre del grupo",
                "Debes escribir un nombre para el grupo."
            )
            return
        if not ruta_salida:
            messagebox.showwarning(
                "Carpeta de salida",
                "Primero selecciona una carpeta de salida."
            )
            return
        if not retratos:
            return
        modo = modo_generacion.get()

        datos_generales = []

        for retrato in retratos:

        # =====================================================
        # MODO MANUAL
        # =====================================================

            if modo == "manual":
                try:
                    ataque = max(
                        1,
                        min(10, int(entry_ataque.get() or 0))
                    )
                    defensa = max(
                        1,
                        min(10, int(entry_defensa.get() or 0))
                    )
                    planificacion = max(
                        1,
                        min(10, int(entry_planificacion.get() or 0))
                    )
                    logistica = max(
                        1,
                        min(10, int(entry_logistica.get() or 0))
                    )

                except ValueError:
                    messagebox.showerror(
                        "Atributos inválidos",
                        "Los atributos deben ser números."
                    )
                    return
            # CREAR LA LISTA NUEVA CADA VEZ
                traits = []

                if check_brilliant.get():
                    traits.append("brilliant_strategist")

                if check_panzer.get():
                    traits.append("panzer_leader")

                if check_infantry.get():
                    traits.append("infantry_leader")

                if check_commando.get():
                    traits.append("commando")

                if ckeck_ingenieros.get():
                    traits.append("trait_engineer")

                if ckeck_organizador.get():
                    traits.append("organizer")

                if check_mago_de_la_logistica.get():
                    traits.append("logistics_wizard")

                if ckeck_adaptable.get():
                    traits.append("adaptable")

                if ckeck_especialista_armamento.get():
                    traits.append(
                        "especialista_en_armamento"
                    )
                if ckeck_especialista_armamento_elite.get():
                    traits.append(
                        "especialista_en_armamento_elite"
                    )

            # =====================================================
            # MODO ALEATORIO
            # =====================================================

            elif modo == "aleatorio":

                ataque, defensa, planificacion, logistica = (
                    generar_estadisticas_aleatorias()
                )

                traits = generar_traits_aleatorios(
                    incluir_personalizados=False
                )

            # =====================================================
            # MODO ALEATORIO + PERSONALIZADOS
            # =====================================================

            elif modo == "aleatorio_personalizado":

                ataque, defensa, planificacion, logistica = (
                    generar_estadisticas_aleatorias()
                )

                traits = generar_traits_aleatorios(
                    incluir_personalizados=True
                )
            datos_generales.append(
                {
                    "ataque": ataque,
                    "defensa": defensa,
                    "planificacion": planificacion,
                    "logistica": logistica,
                    "traits": traits
                }
            )

        # =====================================================
        # CREAR GENERAL
        # =====================================================
        funcion_crear(
            ruta_salida,
            nombre_grupo,
            retratos,
            datos_generales
        )

        messagebox.showinfo(
            "Creación exitosa",
            "General creado exitosamente\n\n"
            f"El mod fue creado en:\n{ruta_salida}"
        )
    
    label_grupo = stk.CTkLabel(frame_mod, text="Nombre del grupo")
    label_grupo.grid(
        row=1,
        column=0,
        padx=10,
        pady=(10,2),
        sticky="w"
    )

    entry_grupo = stk.CTkEntry(frame_mod, width=250)
    entry_grupo.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=10,
        pady=(0,10),
        sticky="ew"
    )

    label_estado_salida = stk.CTkLabel(
        frame_mod,
        text="Ninguna carpeta\nseleccionada"
    )
    label_estado_salida.grid(
        row=0,
        column=1,
        padx=10,
        sticky="w"
    )

    def cargar_ruta():
        nonlocal ruta_salida

        ruta_salida = funcion_ruta()

        if not ruta_salida:
            label_estado_salida.configure(
                text="No se seleccionó carpeta de salida."
            )
            return
        nombre_destino = os.path.basename(
            ruta_salida
        )

        label_estado_salida.configure(
            text=(
                "carpeta seleccionada\n"
                f"{nombre_destino}"
            )
        )

    guardar_mod = stk.CTkButton(
        frame_mod,
        text="selecciona una carpeta\npara guardar el mod.",
        font=("Arial",16,"bold"),
        command=cargar_ruta
    )
    guardar_mod.grid(
        row=0,
        column=0,
        padx=10,
        pady=20
    )
    generar_mod = stk.CTkButton(
        frame_mod,
        text="Crear mod.",
        font=("Arial",16,"bold"),
        command=guardar
    )
    generar_mod.grid(
        row=9,
        column=0,
        columnspan=2,
        pady=20,
        sticky="ew",
        padx=50
    )
    
    # =========================================================
    # INICIAR EN MODO MANUAL
    # =========================================================

    cambiar_modo()

    ventana.mainloop()