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