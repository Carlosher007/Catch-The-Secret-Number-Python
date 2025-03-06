import random
import tkinter as tk
from tkinter import messagebox, font
import time


class JuegoAdivinanza:
    def __init__(self):
        """Inicializa el juego con valores predeterminados."""
        self.min_num = 1
        self.max_num = 100
        self.numero_secreto = None
        self.intentos = 0
        self.max_intentos = 10
        self.tiempo_inicio = None
        self.generar_numero()

    def generar_numero(self):
        """Genera un número aleatorio entre min_num y max_num."""
        self.numero_secreto = random.randint(self.min_num, self.max_num)
        self.intentos = 0
        self.tiempo_inicio = time.time()
        return self.numero_secreto

    def verificar_intento(self, intento):
        """Verifica si el intento es correcto y devuelve una pista."""
        try:
            intento = int(intento)
            self.intentos += 1

            if intento < self.min_num or intento > self.max_num:
                return "Fuera de rango", False

            if intento < self.numero_secreto:
                return "Más alto", False
            elif intento > self.numero_secreto:
                return "Más bajo", False
            else:
                tiempo_total = round(time.time() - self.tiempo_inicio, 2)
                return (
                    f"¡Correcto! Lo lograste en {self.intentos} intentos y {tiempo_total} segundos.",
                    True,
                )

        except ValueError:
            return "Por favor, ingresa un número válido.", False

    def obtener_estadisticas(self):
        """Devuelve estadísticas del juego actual."""
        return {
            "intentos": self.intentos,
            "max_intentos": self.max_intentos,
            "tiempo": (
                round(time.time() - self.tiempo_inicio, 2) if self.tiempo_inicio else 0
            ),
        }

    def quedan_intentos(self):
        """Verifica si quedan intentos disponibles."""
        return self.intentos < self.max_intentos
    
class InterfazJuegoRetro:
    def __init__(self, root):
        """Inicializa la interfaz gráfica del juego con estilo retro."""
        self.root = root
        self.root.title("ADIVINA EL NÚMERO")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        # Crear fuentes retro
        self.fuente_titulo = font.Font(family="Courier", size=20, weight="bold")
        self.fuente_normal = font.Font(family="Courier", size=12)
        self.fuente_grande = font.Font(family="Courier", size=14, weight="bold")

        self.juego = JuegoAdivinanza()

        # Efecto de parpadeo para elementos retro
        self.parpadeo = False
        self.elementos_parpadeo = []
        self.configurar_interfaz()
        self.iniciar_parpadeo()

    def configurar_interfaz(self):
        """Configura los componentes de la interfaz con estilo retro."""
        # Marco principal con borde retro
        main_frame = tk.Frame(
            self.root,
            bg="black",
            bd=5,
            relief="ridge",
            highlightbackground="#00FF00",
            highlightthickness=2,
        )
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título del juego con estilo retro
        titulo_frame = tk.Frame(main_frame, bg="black", bd=0)
        titulo_frame.pack(pady=10, fill="x")

        titulo = tk.Label(
            titulo_frame,
            text="== ADIVINA EL NÚMERO ==",
            font=self.fuente_titulo,
            bg="black",
            fg="#00FF00",
            pady=10,
        )
        titulo.pack()
        self.elementos_parpadeo.append(titulo)

        # Línea separadora retro
        separador = tk.Frame(main_frame, height=2, bg="#00FF00")
        separador.pack(fill="x", padx=20, pady=5)

        # Instrucciones con estilo de terminal
        tk.Label(
            main_frame,
            text=f"MISIÓN: Adivinar un número entre {self.juego.min_num} y {self.juego.max_num}",
            font=self.fuente_normal,
            bg="black",
            fg="#00FFFF",
            pady=5,
            justify="left",
        ).pack(padx=20, anchor="w")

        # Frame para entrada con estilo terminal
        input_frame = tk.Frame(main_frame, bg="black", pady=15)
        input_frame.pack(fill="x", padx=20)

        tk.Label(
            input_frame, text="> ", font=self.fuente_grande, bg="black", fg="#00FF00"
        ).pack(side="left")

        # Campo de entrada con estilo retro
        self.entrada = tk.Entry(
            input_frame,
            font=self.fuente_grande,
            width=10,
            bg="black",
            fg="#00FF00",
            insertbackground="#00FF00",  # cursor verde
            bd=0,
            highlightthickness=1,
            highlightbackground="#00FF00",
        )
        self.entrada.pack(side="left", padx=5)
        self.entrada.bind("<Return>", lambda event: self.verificar_intento())
        self.entrada.focus()

        # Botón para verificar con estilo arcade
        verificar_btn = tk.Button(
            input_frame,
            text="VERIFICAR",
            font=self.fuente_normal,
            bg="black",
            fg="#FFFF00",
            activebackground="#333333",
            activeforeground="#FFFF00",
            bd=2,
            relief="raised",
            command=self.verificar_intento,
        )
        verificar_btn.pack(side="left", padx=10)

        # Panel para las pistas con estilo de terminal
        pista_frame = tk.Frame(
            main_frame,
            bg="#000033",
            bd=2,
            relief="sunken",
            highlightbackground="#00FFFF",
            highlightthickness=1,
        )
        pista_frame.pack(padx=20, pady=15, fill="both", expand=True)

        # Etiqueta de "TERMINAL" para el panel de pistas
        tk.Label(
            pista_frame,
            text="TERMINAL DE SISTEMA",
            font=self.fuente_normal,
            bg="#000033",
            fg="#FFFF00",
            anchor="w",
        ).pack(fill="x", padx=5, pady=2)

        # Etiqueta para las pistas con estilo de terminal
        self.label_pista = tk.Label(
            pista_frame,
            text="Iniciando sistema... \nListo para recibir comandos.\n\nEsperando tu primer intento.",
            font=("Courier", 12),
            bg="#000033",
            fg="#00FFFF",
            justify="left",
            anchor="w",
            padx=10,
            pady=10,
            height=6,
        )
        self.label_pista.pack(fill="both", expand=True)

        # Panel de información con estilo retro
        info_frame = tk.Frame(main_frame, bg="black", pady=10)
        info_frame.pack(fill="x", padx=20)

        # Contador de intentos con estilo LED
        intentos_frame = tk.Frame(info_frame, bg="#330000", bd=2, relief="sunken")
        intentos_frame.pack(side="left", expand=True, fill="x", padx=5)

        tk.Label(
            intentos_frame,
            text="INTENTOS",
            font=self.fuente_normal,
            bg="#330000",
            fg="#FF0000",
        ).pack(pady=2)

        self.label_intentos = tk.Label(
            intentos_frame,
            text=f"0/{self.juego.max_intentos}",
            font=self.fuente_grande,
            bg="#330000",
            fg="#FF5555",
        )
        self.label_intentos.pack(pady=2)

        # Tiempo con estilo LED
        tiempo_frame = tk.Frame(info_frame, bg="#003300", bd=2, relief="sunken")
        tiempo_frame.pack(side="right", expand=True, fill="x", padx=5)

        tk.Label(
            tiempo_frame,
            text="TIEMPO",
            font=self.fuente_normal,
            bg="#003300",
            fg="#33FF33",
        ).pack(pady=2)

        self.label_tiempo = tk.Label(
            tiempo_frame, text="0s", font=self.fuente_grande, bg="#003300", fg="#55FF55"
        )
        self.label_tiempo.pack(pady=2)

        # Separador inferior
        separador2 = tk.Frame(main_frame, height=2, bg="#00FF00")
        separador2.pack(fill="x", padx=20, pady=10)

        # Botones de control con estilo arcade
        control_frame = tk.Frame(main_frame, bg="black")
        control_frame.pack(pady=10)

        reiniciar_btn = tk.Button(
            control_frame,
            text="[ REINICIAR ]",
            font=self.fuente_normal,
            bg="black",
            fg="#00FFFF",
            activebackground="#003333",
            activeforeground="#00FFFF",
            bd=2,
            relief="raised",
            width=15,
            command=self.reiniciar_juego,
        )
        reiniciar_btn.pack(side="left", padx=10)

        salir_btn = tk.Button(
            control_frame,
            text="[ SALIR ]",
            font=self.fuente_normal,
            bg="black",
            fg="#FF3333",
            activebackground="#330000",
            activeforeground="#FF3333",
            bd=2,
            relief="raised",
            width=15,
            command=self.root.destroy,
        )
        salir_btn.pack(side="left", padx=10)

        # Copyright retro
        tk.Label(
            main_frame,
            text="(C) 2025 RETROGAMES",
            font=("Courier", 8),
            bg="black",
            fg="#777777",
        ).pack(side="bottom", pady=5)

        # Actualizar tiempo cada segundo
        self.actualizar_tiempo()

    def verificar_intento(self):
        """Verifica el intento del jugador y actualiza la interfaz."""
        intento = self.entrada.get()
        self.entrada.delete(0, tk.END)

        if not self.juego.quedan_intentos():
            self.mostrar_mensaje_arcade(
                "¡GAME OVER!",
                f"Se agotaron tus intentos.\nEl número era {self.juego.numero_secreto}.\n\n¿Quieres jugar de nuevo?",
            )
            return

        mensaje, correcto = self.juego.verificar_intento(intento)

        # Mensaje de terminal para las pistas
        if correcto:
            pista_texto = f">>> CORRECTO! <<<\n\nEl número secreto era: {self.juego.numero_secreto}\n\nMisión cumplida en {self.juego.intentos} intentos."
            self.label_pista.config(text=pista_texto, fg="#00FF00")
            self.mostrar_mensaje_victoria()
        elif "Más alto" in mensaje:
            pista_texto = f"Analizando entrada: {intento}\n\n>>> MÁS ALTO <<<\nEl número secreto es mayor."
            self.label_pista.config(text=pista_texto, fg="#FFFF00")
        elif "Más bajo" in mensaje:
            pista_texto = f"Analizando entrada: {intento}\n\n>>> MÁS BAJO <<<\nEl número secreto es menor."
            self.label_pista.config(text=pista_texto, fg="#00FFFF")
        else:
            pista_texto = f"ERROR: {mensaje}\n\nReintenta con un número válido."
            self.label_pista.config(text=pista_texto, fg="#FF5555")

        # Actualizar contador de intentos
        stats = self.juego.obtener_estadisticas()
        self.label_intentos.config(text=f"{stats['intentos']}/{stats['max_intentos']}")

        # Efecto de intermitencia en el panel de pistas
        self.root.after(100, lambda: self.label_pista.config(bg="#000066"))
        self.root.after(200, lambda: self.label_pista.config(bg="#000033"))

    def mostrar_mensaje_victoria(self):
        """Muestra un mensaje de victoria con estilo retro."""
        stats = self.juego.obtener_estadisticas()
        self.mostrar_mensaje_arcade(
            "¡VICTORIA!",
            f"Has descubierto el código secreto: {self.juego.numero_secreto}\n\n"
            f"Intentos: {stats['intentos']}/{stats['max_intentos']}\n"
            f"Tiempo: {int(stats['tiempo'])} segundos\n\n"
            "¿Quieres iniciar una nueva misión?",
        )

    def mostrar_mensaje_arcade(self, titulo, mensaje):
        """Muestra un mensaje con estilo arcade clásico."""
        resultado = messagebox.askquestion(titulo, mensaje, icon="question")

        if resultado == "yes":
            self.reiniciar_juego()
        else:
            self.root.destroy()

    def reiniciar_juego(self):
        """Reinicia el juego con un nuevo número secreto."""
        self.juego.generar_numero()
        self.label_pista.config(
            text="Sistema reiniciado.\nNuevo código secreto generado.\n\nEsperando tu primer intento.",
            fg="#00FFFF",
        )
        stats = self.juego.obtener_estadisticas()
        self.label_intentos.config(text=f"{stats['intentos']}/{stats['max_intentos']}")
        self.entrada.focus()

        # Efecto de reinicio
        for i in range(3):
            self.root.after(i * 200, lambda: self.label_pista.config(bg="#000066"))
            self.root.after(
                i * 200 + 100, lambda: self.label_pista.config(bg="#000033")
            )

    def actualizar_tiempo(self):
        """Actualiza el tiempo transcurrido en la interfaz."""
        if self.juego.tiempo_inicio:
            tiempo_actual = int(time.time() - self.juego.tiempo_inicio)
            self.label_tiempo.config(text=f"{tiempo_actual}s")

        # Actualizar cada segundo
        self.root.after(1000, self.actualizar_tiempo)

    def iniciar_parpadeo(self):
        """Inicia efecto de parpadeo para elementos retro."""

        def parpadear():
            self.parpadeo = not self.parpadeo
            for elemento in self.elementos_parpadeo:
                if self.parpadeo:
                    elemento.config(fg="#55FF55")
                else:
                    elemento.config(fg="#00FF00")
            self.root.after(500, parpadear)

        parpadear()