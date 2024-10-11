import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

def punto_fijo(g, x0, tolerancia, max_iter):
    x = x0
    iteraciones = []
    for i in range(max_iter):
        x_nuevo = g(x)
        error = abs((x_nuevo - x) / x_nuevo) * 100 if x_nuevo != 0 else 0
        iteraciones.append((i+1, x, g(x), x_nuevo, error))
        if abs(x_nuevo - x) < tolerancia:
            return x_nuevo, iteraciones
        x = x_nuevo
    return None, iteraciones

class AplicacionPuntoFijo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Método del Punto Fijo")
        self.geometry("1200x800")

        ctk.set_appearance_mode("dark")  # Opciones: "dark", "light"
        ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(6, weight=1)

        self.label_funcion = ctk.CTkLabel(self.frame, text="Función g(x):")
        self.label_funcion.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_funcion = ctk.CTkEntry(self.frame, width=200)
        self.entry_funcion.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_funcion.insert(0, "np.cos(x)")

        self.label_x0 = ctk.CTkLabel(self.frame, text="Valor inicial (x0):")
        self.label_x0.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_x0 = ctk.CTkEntry(self.frame, width=200)
        self.entry_x0.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_x0.insert(0, "0.5")

        self.label_tolerancia = ctk.CTkLabel(self.frame, text="Tolerancia:")
        self.label_tolerancia.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_tolerancia = ctk.CTkEntry(self.frame, width=200)
        self.entry_tolerancia.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entry_tolerancia.insert(0, "1e-6")

        self.label_max_iter = ctk.CTkLabel(self.frame, text="Máximo de iteraciones:")
        self.label_max_iter.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_max_iter = ctk.CTkEntry(self.frame, width=200)
        self.entry_max_iter.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.entry_max_iter.insert(0, "100")

        self.boton_calcular = ctk.CTkButton(self.frame, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.label_resultado = ctk.CTkLabel(self.frame, text="")
        self.label_resultado.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Frame para gráfica y tabla
        self.frame_resultados = ctk.CTkFrame(self.frame)
        self.frame_resultados.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.frame_resultados.grid_columnconfigure(0, weight=1)
        self.frame_resultados.grid_columnconfigure(1, weight=1)
        self.frame_resultados.grid_rowconfigure(0, weight=1)

        # Gráfica
        self.figura = plt.Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_resultados)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Tabla

        style = ttk.Style()
        style.theme_use("clam")  # Usar un tema más moderno

        # Configurar colores para el tema oscuro
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        self.tabla = ttk.Treeview(self.frame_resultados, columns=("i", "Xi", "f(Xi)", "g(Xi)", "Error"), show="headings")
        self.tabla.heading("i", text="i")
        self.tabla.heading("Xi", text="Xi")
        self.tabla.heading("f(Xi)", text="f(Xi)")
        self.tabla.heading("g(Xi)", text="g(Xi)")
        self.tabla.heading("Error", text="Error (%)")
        self.tabla.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Scrollbar para la tabla
        self.scrollbar = ttk.Scrollbar(self.frame_resultados, orient="vertical", command=self.tabla.yview)
        self.scrollbar.grid(row=0, column=2, sticky="ns")
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        # Panel de calculadora
        self.frame_calculadora = ctk.CTkFrame(self.frame)
        self.frame_calculadora.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="nsew")

        botones = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'C', '+'
        ]

        for i, boton in enumerate(botones):
            cmd = lambda x=boton: self.click_boton(x)
            ctk.CTkButton(self.frame_calculadora, text=boton, command=cmd, width=50).grid(row=i//4, column=i%4, padx=5, pady=5)

        # Funciones matemáticas básicas
        funciones_basicas = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']
        for i, func in enumerate(funciones_basicas):
            cmd = lambda x=func: self.click_funcion(x)
            ctk.CTkButton(self.frame_calculadora, text=func, command=cmd, width=50).grid(row=i//3 + 4, column=i%3, padx=5, pady=5)

        # Funciones matemáticas adicionales
        funciones_adicionales = [
            ('arcsin', 'asin'), ('arccos', 'acos'), ('arctan', 'atan'),
            ('sinh', 'sinh'), ('cosh', 'cosh'), ('tanh', 'tanh'),
            ('log10', 'log10'), ('log2', 'log2'), ('abs', 'abs'),
            ('ceil', 'ceil'), ('floor', 'floor'), ('round', 'round')
        ]
        for i, (texto, func) in enumerate(funciones_adicionales):
            cmd = lambda x=func: self.click_funcion(x)
            ctk.CTkButton(self.frame_calculadora, text=texto, command=cmd, width=50).grid(row=i//3 + 6, column=i%3, padx=5, pady=5)

        # Constantes y símbolos adicionales
        constantes = [
            ('π', 'np.pi'), ('e', 'np.e'), ('^', '**'),
            ('(', '('), (')', ')'), (',', ',')
        ]
        for i, (texto, valor) in enumerate(constantes):
            cmd = lambda x=valor: self.click_boton(x)
            ctk.CTkButton(self.frame_calculadora, text=texto, command=cmd, width=50).grid(row=i//3 + 10, column=i%3, padx=5, pady=5)

    def click_boton(self, key):
        if key == 'C':
            self.entry_funcion.delete(0, ctk.END)
        else:
            current = self.entry_funcion.get()
            self.entry_funcion.delete(0, ctk.END)
            self.entry_funcion.insert(ctk.END, current + key)

    def click_funcion(self, func):
        current = self.entry_funcion.get()
        self.entry_funcion.delete(0, ctk.END)
        self.entry_funcion.insert(ctk.END, current + f"np.{func}(")

    def calcular(self):
        g_str = self.entry_funcion.get()
        x0 = float(self.entry_x0.get())
        tolerancia = float(self.entry_tolerancia.get())
        max_iter = int(self.entry_max_iter.get())

        g = lambda x: eval(g_str)
        f = lambda x: g(x) - x

        resultado, iteraciones = punto_fijo(g, x0, tolerancia, max_iter)

        if resultado is not None:
            self.label_resultado.configure(text=f"Punto fijo: {resultado:.4f}\nIteraciones: {len(iteraciones)}")
            self.graficar(g, f, resultado)
            self.actualizar_tabla(iteraciones)
        else:
            self.label_resultado.configure(text="No se encontró un punto fijo")

    def graficar(self, g, f, punto_fijo):
        self.subplot.clear()
        
        # Determinar el rango para x
        x_min = punto_fijo - 1
        x_max = punto_fijo + 1
        x = np.linspace(x_min, x_max, 100)
        y_g = g(x)
        y_f = f(x)
        
        # Graficar las funciones
        self.subplot.plot(x, y_g, label="g(x)")
        self.subplot.plot(x, y_f, label="f(x) = g(x) - x")
        self.subplot.plot(x, x, label="y = x")
        self.subplot.plot(punto_fijo, punto_fijo, 'ro', label="Punto fijo")
        
        # Configurar leyenda
        self.subplot.legend()
        
        # Configurar título y etiquetas de ejes
        self.subplot.set_title("Gráfica de g(x), f(x) y y = x")
        self.subplot.set_xlabel("x")
        self.subplot.set_ylabel("y")
        
        # Ajustar los límites de los ejes
        y_min = min(min(y_g), min(y_f), x_min)
        y_max = max(max(y_g), max(y_f), x_max)
        self.subplot.set_xlim(x_min, x_max)
        self.subplot.set_ylim(y_min, y_max)
        
        # Mostrar los ejes x e y
        self.subplot.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
        self.subplot.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
        
        # Añadir cuadrícula
        self.subplot.grid(True, linestyle=':', alpha=0.7)
        
        # Ajustar el espaciado
        self.figura.tight_layout()
        
        # Redibujar el canvas
        self.canvas.draw()


    def actualizar_tabla(self, iteraciones):
        # Limpiar tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        # Insertar nuevos datos
        for i, (iter, x, fx, gx, error) in enumerate(iteraciones):
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            self.tabla.insert("", "end", values=(iter, f"{x:.4f}", f"{fx:.4f}", f"{gx:.4f}", f"{error:.4f}"), tags=tags)
        
        # Configurar colores alternados para las filas
        self.tabla.tag_configure('oddrow', background='#2a2d2e')
        self.tabla.tag_configure('evenrow', background='#3c4043')

if __name__ == "__main__":
    app = AplicacionPuntoFijo()
    app.mainloop()