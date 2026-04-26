# -*- coding: utf-8 -*-
"""Modulo que define la ventana principal de la aplicacion."""

import random
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional

from .lanzador import Lanzador
from .tirada import Tirada

# Posiciones de los puntos (en % del tamanio del dado) para cada cara d6
POSICIONES_PUNTOS = {
    1: [(50, 50)],
    2: [(25, 75), (75, 25)],
    3: [(25, 75), (50, 50), (75, 25)],
    4: [(25, 25), (75, 25), (25, 75), (75, 75)],
    5: [(25, 25), (75, 25), (50, 50), (25, 75), (75, 75)],
    6: [(25, 25), (75, 25), (25, 50), (75, 50), (25, 75), (75, 75)],
}

# Duracion y cadencia de la animacion
DURACION_ANIMACION_MS = 3000
INTERVALO_ANIMACION_MS = 500

# Colores del tema oscuro W40K
COLOR_FONDO = "#1a1a2e"
COLOR_ACENTO = "#c0a060"
COLOR_TEXTO = "#e0e0e0"
COLOR_TEXTO_TENUE = "#a0a0c0"
COLOR_DADO_FONDO = "#f5e6c8"
COLOR_DADO_PUNTO = "#2c1810"
COLOR_DADO_BORDE = "#8b6020"
COLOR_CANVAS = "#0d1b2a"
COLOR_BTN_PRIMARIO = "#8b0000"
COLOR_BTN_SECUNDARIO = "#2a2a5e"
COLOR_BTN_CERRAR = "#4a1010"
COLOR_HISTORICO_BG = "#0d1b2a"
COLOR_HISTORICO_FG = "#a0c0a0"


class VentanaPrincipal:
    """Ventana principal de la aplicacion lanzadora de dados."""

    TITULO = "Lanzador de Dados Warhammer 40K"
    ANCHO = 640
    ALTO = 720

    def __init__(self) -> None:
        """Inicializa la ventana principal y sus componentes."""
        self._lanzador = Lanzador()
        self._raiz = tk.Tk()
        self._raiz.title(self.TITULO)
        self._raiz.geometry(f"{self.ANCHO}x{self.ALTO}")
        self._raiz.configure(bg=COLOR_FONDO)
        self._raiz.resizable(True, True)
        self._raiz.minsize(480, 560)

        # Estado de la animacion
        self._animacion_activa = False
        self._contador_frames = 0
        self._max_frames = DURACION_ANIMACION_MS // INTERVALO_ANIMACION_MS
        self._tirada_pendiente: Optional[Tirada] = None
        self._cantidad_animacion = 1
        self._lados_animacion = 6

        self._configurar_estilos()
        self._crear_interfaz()

    # ------------------------------------------------------------------
    # Configuracion de estilos
    # ------------------------------------------------------------------

    def _configurar_estilos(self) -> None:
        """Configura los estilos ttk de la interfaz."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure(
            "TLabelframe",
            background=COLOR_FONDO,
            foreground=COLOR_ACENTO,
            bordercolor=COLOR_ACENTO,
        )
        estilo.configure(
            "TLabelframe.Label",
            background=COLOR_FONDO,
            foreground=COLOR_ACENTO,
            font=("Arial", 10, "bold"),
        )
        estilo.configure(
            "TLabel",
            background=COLOR_FONDO,
            foreground=COLOR_TEXTO,
        )
        estilo.configure(
            "TSpinbox",
            fieldbackground="#2a2a4e",
            foreground=COLOR_TEXTO,
            background=COLOR_BTN_SECUNDARIO,
            arrowcolor=COLOR_ACENTO,
        )
        estilo.configure(
            "TButton",
            background=COLOR_BTN_SECUNDARIO,
            foreground=COLOR_TEXTO,
            padding=5,
            font=("Arial", 9),
        )
        estilo.map(
            "TButton",
            background=[("active", "#4a4a8e"), ("disabled", "#333333")],
            foreground=[("disabled", "#666666")],
        )
        estilo.configure(
            "Lanzar.TButton",
            background=COLOR_BTN_PRIMARIO,
            foreground="white",
            font=("Arial", 11, "bold"),
            padding=8,
        )
        estilo.map(
            "Lanzar.TButton",
            background=[("active", "#cc0000"), ("disabled", "#555555")],
        )
        estilo.configure(
            "Cerrar.TButton",
            background=COLOR_BTN_CERRAR,
            foreground="white",
            padding=5,
        )
        estilo.map(
            "Cerrar.TButton",
            background=[("active", "#6a2020")],
        )

    # ------------------------------------------------------------------
    # Construccion de la interfaz
    # ------------------------------------------------------------------

    def _crear_interfaz(self) -> None:
        """Crea todos los componentes de la interfaz de usuario."""
        self._crear_frame_configuracion()
        self._crear_frame_botones()
        self._crear_frame_animacion()
        self._crear_frame_resultados()
        self._crear_frame_historico()

    def _crear_frame_configuracion(self) -> None:
        """Crea el frame de configuracion de dados."""
        frame = ttk.LabelFrame(self._raiz, text="Configuracion de tirada", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(frame, text="Cantidad de dados:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=4
        )
        self._var_cantidad = tk.IntVar(value=1)
        self._spin_cantidad = ttk.Spinbox(
            frame, from_=1, to=100, textvariable=self._var_cantidad, width=8
        )
        self._spin_cantidad.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(frame, text="Lados por dado:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=4
        )
        self._var_lados = tk.IntVar(value=6)
        self._spin_lados = ttk.Spinbox(
            frame, from_=2, to=100, textvariable=self._var_lados, width=8
        )
        self._spin_lados.grid(row=0, column=3, padx=5, pady=4)

        self._label_tipo_dado = ttk.Label(
            frame, text="(1d6)", foreground=COLOR_ACENTO, font=("Arial", 10, "italic")
        )
        self._label_tipo_dado.grid(row=0, column=4, padx=10)

        # Actualizar etiqueta de tipo al cambiar los spinboxes
        self._var_cantidad.trace_add("write", self._on_cambio_configuracion)
        self._var_lados.trace_add("write", self._on_cambio_configuracion)

    def _crear_frame_botones(self) -> None:
        """Crea el frame con los botones de accion."""
        frame = ttk.Frame(self._raiz, padding=5)
        frame.pack(fill=tk.X, padx=10, pady=5)

        self._btn_lanzar = ttk.Button(
            frame,
            text="\U0001f3b2 Lanzar dados",
            command=self._on_lanzar,
            style="Lanzar.TButton",
        )
        self._btn_lanzar.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame,
            text="Resetear historico",
            command=self._on_reset_historico,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame,
            text="Reseteo global",
            command=self._on_reset_global,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame,
            text="Cerrar",
            command=self._on_cerrar,
            style="Cerrar.TButton",
        ).pack(side=tk.RIGHT, padx=5)

    def _crear_frame_animacion(self) -> None:
        """Crea el frame de animacion (no se empaqueta hasta que empiece la animacion)."""
        self._frame_anim = ttk.LabelFrame(
            self._raiz, text="Lanzando...", padding=5
        )
        # No se llama a pack() aqui; se mostrara durante la animacion

        self._canvas_dados = tk.Canvas(
            self._frame_anim,
            height=110,
            bg=COLOR_CANVAS,
            highlightthickness=0,
        )
        self._canvas_dados.pack(fill=tk.X, padx=5, pady=5)

        self._var_tirando = tk.StringVar(value="Tirando...")
        ttk.Label(
            self._frame_anim,
            textvariable=self._var_tirando,
            font=("Arial", 11, "italic"),
            foreground=COLOR_ACENTO,
        ).pack(pady=2)

    def _crear_frame_resultados(self) -> None:
        """Crea el frame de resultados de la ultima tirada."""
        self._frame_resultados = ttk.LabelFrame(
            self._raiz, text="Resultado de la tirada", padding=10
        )
        self._frame_resultados.pack(fill=tk.X, padx=10, pady=5)

        self._label_total = ttk.Label(
            self._frame_resultados,
            text="Sin tirar",
            font=("Arial", 17, "bold"),
            foreground=COLOR_ACENTO,
        )
        self._label_total.pack()

        self._label_detalle = ttk.Label(
            self._frame_resultados,
            text="",
            font=("Arial", 10),
            foreground=COLOR_TEXTO_TENUE,
        )
        self._label_detalle.pack()

    def _crear_frame_historico(self) -> None:
        """Crea el frame del historico de tiradas."""
        frame = ttk.LabelFrame(
            self._raiz, text="Historico de tiradas", padding=8
        )
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text_historico = tk.Text(
            frame,
            height=8,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            bg=COLOR_HISTORICO_BG,
            fg=COLOR_HISTORICO_FG,
            insertbackground="white",
            selectbackground=COLOR_BTN_SECUNDARIO,
            relief=tk.FLAT,
        )
        self._text_historico.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._text_historico.yview)

    # ------------------------------------------------------------------
    # Manejadores de eventos
    # ------------------------------------------------------------------

    def _on_cambio_configuracion(self, *args) -> None:
        """Actualiza la etiqueta de tipo de dado al cambiar la configuracion."""
        try:
            cantidad = self._var_cantidad.get()
            lados = self._var_lados.get()
            self._label_tipo_dado.config(text=f"({cantidad}d{lados})")
        except (tk.TclError, ValueError):
            pass

    def _on_lanzar(self) -> None:
        """Maneja el evento de lanzar dados."""
        if self._animacion_activa:
            return

        try:
            cantidad = self._var_cantidad.get()
            lados = self._var_lados.get()
        except (tk.TclError, ValueError):
            messagebox.showerror("Error", "Los valores deben ser numeros enteros validos.")
            return

        if cantidad < 1:
            messagebox.showerror("Error", "La cantidad minima de dados es 1.")
            return
        if lados < 2:
            messagebox.showerror("Error", "El numero minimo de lados es 2.")
            return

        tirada = self._lanzador.lanzar(cantidad, lados)
        self._tirada_pendiente = tirada
        self._cantidad_animacion = cantidad
        self._lados_animacion = lados
        self._iniciar_animacion()

    def _on_reset_historico(self) -> None:
        """Maneja el evento de resetear el historico."""
        self._lanzador.resetear_historico()
        self._actualizar_historico()
        self._label_total.config(text="Sin tirar")
        self._label_detalle.config(text="")

    def _on_reset_global(self) -> None:
        """Maneja el evento de reseteo global: resetea configuracion e historico."""
        self._lanzador.resetear_todo()
        self._var_cantidad.set(1)
        self._var_lados.set(6)
        self._actualizar_historico()
        self._label_total.config(text="Sin tirar")
        self._label_detalle.config(text="")

    def _on_cerrar(self) -> None:
        """Maneja el evento de cerrar la aplicacion."""
        self._raiz.quit()
        self._raiz.destroy()

    # ------------------------------------------------------------------
    # Logica de animacion
    # ------------------------------------------------------------------

    def _iniciar_animacion(self) -> None:
        """Inicia la animacion de lanzamiento de dados."""
        self._animacion_activa = True
        self._contador_frames = 0
        self._btn_lanzar.config(state=tk.DISABLED)
        # Insertar el frame de animacion justo antes del frame de resultados
        self._frame_anim.pack(
            fill=tk.X, padx=10, pady=5, before=self._frame_resultados
        )
        self._paso_animacion()

    def _paso_animacion(self) -> None:
        """Ejecuta un paso de la animacion y programa el siguiente."""
        if self._contador_frames >= self._max_frames:
            self._finalizar_animacion()
            return

        self._dibujar_dados_aleatorios()
        puntos_str = "." * ((self._contador_frames % 4) + 1)
        self._var_tirando.set(f"Tirando{puntos_str}")

        self._contador_frames += 1
        self._raiz.after(INTERVALO_ANIMACION_MS, self._paso_animacion)

    def _dibujar_dados_aleatorios(self) -> None:
        """Dibuja dados con valores aleatorios en el canvas de animacion."""
        self._canvas_dados.delete("all")
        ancho = self._canvas_dados.winfo_width()
        if ancho < 20:
            ancho = 600

        num_visibles = min(self._cantidad_animacion, 6)
        tamanio = min(84, (ancho - 20) // num_visibles - 10)
        tamanio = max(tamanio, 30)
        margen_x = (ancho - num_visibles * (tamanio + 10)) // 2

        for i in range(num_visibles):
            x = margen_x + i * (tamanio + 10)
            y = (110 - tamanio) // 2
            valor = random.randint(1, min(self._lados_animacion, 6))
            self._dibujar_cara_dado(x, y, tamanio, valor)

    def _dibujar_cara_dado(
        self, x: int, y: int, tamanio: int, valor: int
    ) -> None:
        """
        Dibuja la cara de un dado en el canvas.

        Usa un poligono octagonal para simular esquinas redondeadas.
        Muestra puntos para valores 1-6 o el numero para otros.
        """
        radio = max(5, tamanio // 8)
        x2, y2 = x + tamanio, y + tamanio

        # Poligono octagonal (imita esquinas redondeadas)
        puntos_poligono: List[int] = [
            x + radio, y,
            x2 - radio, y,
            x2, y + radio,
            x2, y2 - radio,
            x2 - radio, y2,
            x + radio, y2,
            x, y2 - radio,
            x, y + radio,
        ]
        self._canvas_dados.create_polygon(
            puntos_poligono,
            fill=COLOR_DADO_FONDO,
            outline=COLOR_DADO_BORDE,
            width=2,
        )

        # Dibujar puntos si el valor esta en POSICIONES_PUNTOS
        if valor in POSICIONES_PUNTOS:
            radio_punto = max(3, tamanio // 10)
            for (px, py) in POSICIONES_PUNTOS[valor]:
                cx = x + tamanio * px // 100
                cy = y + tamanio * py // 100
                self._canvas_dados.create_oval(
                    cx - radio_punto,
                    cy - radio_punto,
                    cx + radio_punto,
                    cy + radio_punto,
                    fill=COLOR_DADO_PUNTO,
                    outline="",
                )
        else:
            self._canvas_dados.create_text(
                x + tamanio // 2,
                y + tamanio // 2,
                text=str(valor),
                font=("Arial", max(10, tamanio // 3), "bold"),
                fill=COLOR_DADO_PUNTO,
            )

    def _finalizar_animacion(self) -> None:
        """Finaliza la animacion y muestra los resultados."""
        self._animacion_activa = False
        self._btn_lanzar.config(state=tk.NORMAL)
        self._frame_anim.pack_forget()

        if self._tirada_pendiente:
            self._mostrar_resultados(self._tirada_pendiente)
            self._actualizar_historico()
            self._tirada_pendiente = None

    # ------------------------------------------------------------------
    # Actualizacion de la interfaz
    # ------------------------------------------------------------------

    def _mostrar_resultados(self, tirada: Tirada) -> None:
        """Muestra los resultados de la tirada en la interfaz."""
        resultados_str = ", ".join(str(r) for r in tirada.resultados)
        self._label_total.config(text=f"Total: {tirada.total}")
        self._label_detalle.config(
            text=f"{tirada.cantidad}d{tirada.lados}  \u2192  [{resultados_str}]"
        )

    def _actualizar_historico(self) -> None:
        """Actualiza el widget de texto del historico con las tiradas almacenadas."""
        self._text_historico.config(state=tk.NORMAL)
        self._text_historico.delete(1.0, tk.END)

        for i, tirada in enumerate(self._lanzador.historico.entradas, 1):
            hora_str = (
                tirada.fecha.strftime("%H:%M:%S") if tirada.fecha else "??:??:??"
            )
            self._text_historico.insert(
                tk.END, f"[{hora_str}] #{i:3d}  {tirada}\n"
            )

        self._text_historico.config(state=tk.DISABLED)
        self._text_historico.see(tk.END)

    # ------------------------------------------------------------------
    # Punto de entrada
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        """Inicia el bucle principal de la aplicacion."""
        self._raiz.mainloop()
