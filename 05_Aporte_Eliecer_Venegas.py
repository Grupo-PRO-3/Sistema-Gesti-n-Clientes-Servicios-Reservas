# APORTE 5 - Eliecer Venegas
# Sección: interfaz gráfica con Tkinter y función principal.
# Este fragmento depende de los Aportes 1, 2, 3 y 4.

class AppReservas:

    # Constructor de la aplicación.
    def __init__(self, root):
        # Guarda referencia a la ventana principal.
        self.root = root

        # Título de la ventana.
        self.root.title("Sistema OOP de Reservas")

        # Tamaño inicial de la ventana.
        self.root.geometry("950x650")

        # Color de fondo cálido.
        self.root.configure(bg="#F7D9B7")

        # Crea el gestor principal.
        self.gestor = GestorReservas()

        # Paleta de colores cálidos.
        self.color_fondo = "#F7D9B7"      # Beige cálido.
        self.color_panel = "#FFE8CC"      # Naranja claro.
        self.color_boton = "#D97941"      # Naranja fuerte.
        self.color_boton_sec = "#A64B2A"  # Marrón cálido.
        self.color_texto = "#4A2C2A"      # Café oscuro.

        # Crea todos los elementos visuales.
        self.crear_widgets()

    # Crea etiquetas, entradas, botones y área de salida.
    def crear_widgets(self):
        # Etiqueta principal del título.
        titulo = tk.Label(
            self.root,
            text="Sistema de Reservas con POO y Excepciones",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=15)

        # Panel para registrar clientes.
        panel = tk.Frame(self.root, bg=self.color_panel, padx=15, pady=15)
        panel.pack(fill="x", padx=20)

        # Etiquetas del formulario de cliente.
        tk.Label(panel, text="Nombre", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=0)
        tk.Label(panel, text="Correo", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=1)
        tk.Label(panel, text="Teléfono", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=2)

        # Campos de entrada para cliente.
        self.nombre_entry = tk.Entry(panel, width=25)
        self.correo_entry = tk.Entry(panel, width=25)
        self.telefono_entry = tk.Entry(panel, width=20)

        # Ubicación de campos en la cuadrícula.
        self.nombre_entry.grid(row=1, column=0, padx=5)
        self.correo_entry.grid(row=1, column=1, padx=5)
        self.telefono_entry.grid(row=1, column=2, padx=5)

        # Botón para registrar cliente.
        tk.Button(
            panel,
            text="Registrar Cliente",
            bg=self.color_boton,
            fg="white",
            command=self.registrar_cliente_ui
        ).grid(row=1, column=3, padx=10)

        # Panel de servicios y reservas.
        panel_servicio = tk.Frame(self.root, bg=self.color_panel, padx=15, pady=15)
        panel_servicio.pack(fill="x", padx=20, pady=10)

        # Etiquetas del formulario de servicio.
        tk.Label(panel_servicio, text="Tipo de servicio", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=0)
        tk.Label(panel_servicio, text="Parámetro", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=1)
        tk.Label(panel_servicio, text="Duración", bg=self.color_panel, fg=self.color_texto).grid(row=0, column=2)

        # Combo para seleccionar tipo de servicio.
        self.tipo_servicio = ttk.Combobox(panel_servicio, values=["spa", "entrenamiento", "consultoria"], width=22)
        self.tipo_servicio.grid(row=1, column=0, padx=5)
        self.tipo_servicio.set("spa")

        # Campo para parámetro del servicio.
        # spa: True o False.
        # entrenamiento: basico, intermedio o avanzado.
        # consultoria: virtual o presencial.
        self.parametro_entry = tk.Entry(panel_servicio, width=25)
        self.parametro_entry.insert(0, "True")
        self.parametro_entry.grid(row=1, column=1, padx=5)

        # Campo para duración en horas.
        self.duracion_entry = tk.Entry(panel_servicio, width=10)
        self.duracion_entry.insert(0, "2")
        self.duracion_entry.grid(row=1, column=2, padx=5)

        # Botón para crear servicio.
        tk.Button(
            panel_servicio,
            text="Crear Servicio",
            bg=self.color_boton,
            fg="white",
            command=self.crear_servicio_ui
        ).grid(row=1, column=3, padx=5)

        # Botón para crear reserva usando último cliente y último servicio creados.
        tk.Button(
            panel_servicio,
            text="Crear Reserva",
            bg=self.color_boton_sec,
            fg="white",
            command=self.crear_reserva_ui
        ).grid(row=1, column=4, padx=5)

        # Botón para ejecutar simulación completa.
        tk.Button(
            self.root,
            text="Ejecutar Simulación de 10+ Operaciones",
            bg="#BF6F41",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.simular_ui
        ).pack(pady=8)

        # Área de texto para mostrar resultados.
        self.salida = tk.Text(
            self.root,
            height=22,
            bg="#FFF7ED",
            fg=self.color_texto,
            font=("Consolas", 10)
        )
        self.salida.pack(fill="both", expand=True, padx=20, pady=10)

    # Escribe mensajes en el área de salida.
    def escribir(self, texto):
        self.salida.insert(tk.END, texto + "\n")
        self.salida.see(tk.END)

    # Acción del botón Registrar Cliente.
    def registrar_cliente_ui(self):
        try:
            # Obtiene datos desde la interfaz y registra cliente.
            cliente = self.gestor.registrar_cliente(
                self.nombre_entry.get(),
                self.correo_entry.get(),
                self.telefono_entry.get()
            )

        except SistemaReservaError as error:
            # Muestra error sin cerrar la aplicación.
            messagebox.showerror("Error controlado", str(error))
            self.escribir(f"ERROR: {error}")

        else:
            # Muestra éxito.
            self.escribir(f"Cliente registrado: {cliente.resumen()}")

    # Acción del botón Crear Servicio.
    def crear_servicio_ui(self):
        try:
            # Obtiene tipo de servicio.
            tipo = self.tipo_servicio.get()

            # Obtiene parámetro escrito por el usuario.
            parametro = self.parametro_entry.get().strip()

            # Para spa, convierte texto True/False a booleano.
            if tipo == "spa":
                parametro = parametro.lower() == "true"

            # Crea servicio mediante el gestor.
            servicio = self.gestor.crear_servicio(tipo, parametro)

        except SistemaReservaError as error:
            # Muestra error controlado.
            messagebox.showerror("Error controlado", str(error))
            self.escribir(f"ERROR: {error}")

        else:
            # Muestra servicio creado.
            self.escribir(f"Servicio creado: {servicio.resumen()} | {servicio.describir()}")

    # Acción del botón Crear Reserva.
    def crear_reserva_ui(self):
        try:
            # Verifica que exista al menos un cliente.
            if not self.gestor.clientes:
                raise ReservaInvalidaError("Debe registrar al menos un cliente.")

            # Verifica que exista al menos un servicio.
            if not self.gestor.servicios:
                raise ReservaInvalidaError("Debe crear al menos un servicio.")

            # Convierte duración a entero.
            duracion = int(self.duracion_entry.get())

            # Crea reserva con el último cliente y servicio registrados.
            reserva = self.gestor.crear_reserva(
                self.gestor.clientes[-1],
                self.gestor.servicios[-1],
                duracion
            )

            # Confirma reserva.
            reserva.confirmar()

            # Procesa reserva.
            reserva.procesar()

        except ValueError:
            # Captura duración no numérica.
            logging.error("Duración no numérica.")
            messagebox.showerror("Error", "La duración debe ser un número entero.")
            self.escribir("ERROR: La duración debe ser un número entero.")

        except SistemaReservaError as error:
            # Captura errores controlados.
            messagebox.showerror("Error controlado", str(error))
            self.escribir(f"ERROR: {error}")

        else:
            # Muestra reserva exitosa.
            self.escribir(f"Reserva exitosa: {reserva.resumen()}")

        finally:
            # Siempre registra fin de operación.
            logging.info("Operación crear_reserva_ui finalizada.")

    # Acción del botón de simulación.
    def simular_ui(self):
        # Muestra inicio.
        self.escribir("\n===== SIMULACIÓN INICIADA =====")

        # Ejecuta simulación.
        resultados = self.gestor.simular_operaciones()

        # Muestra cada resultado.
        for resultado in resultados:
            self.escribir(resultado)

        # Muestra cierre.
        self.escribir("===== SIMULACIÓN FINALIZADA =====")
        self.escribir("Revisa el archivo sistema_reservas.log para eventos y errores.\n")


# ======================================================
# 10. FUNCIÓN PRINCIPAL
# ======================================================

# main inicia la aplicación.
def main():
    try:
        # Registra inicio.
        logging.info("Aplicación iniciada.")

        # Crea ventana principal.
        root = tk.Tk()

        # Crea aplicación.
        AppReservas(root)

        # Mantiene la ventana abierta.
        root.mainloop()

    except Exception as error:
        # Registra cualquier error crítico inesperado.
        logging.critical(f"Error crítico en la aplicación: {error}", exc_info=True)
        raise

    finally:
        # Registra cierre de aplicación.
        logging.info("Aplicación finalizada.")


# Este bloque permite ejecutar el programa directamente.
if __name__ == "__main__":
    main()
