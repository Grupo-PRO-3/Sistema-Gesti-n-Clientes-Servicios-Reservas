# APORTE 4 - Albaro Salgado
# Sección: clase GestorReservas, listas internas y simulación de operaciones.
# Este fragmento depende de los Aportes 1, 2 y 3.

class GestorReservas:

    # Constructor del gestor.
    def __init__(self):
        # Lista interna de clientes.
        self.clientes = []

        # Lista interna de servicios.
        self.servicios = []

        # Lista interna de reservas.
        self.reservas = []

    # Registra un cliente y lo guarda en la lista.
    def registrar_cliente(self, nombre, correo, telefono):
        try:
            # Crea objeto Cliente. Aquí se ejecutan validaciones.
            cliente = Cliente(nombre, correo, telefono)

            # Agrega cliente a lista interna.
            self.clientes.append(cliente)

        except SistemaReservaError as error:
            # Registra error controlado.
            logging.error(f"Error registrando cliente: {error}")
            raise

        else:
            # Registra éxito.
            logging.info(f"Cliente registrado: {cliente.resumen()}")
            return cliente

        finally:
            # Se ejecuta siempre.
            logging.info("Operación registrar_cliente finalizada.")

    # Crea un servicio según el tipo indicado.
    def crear_servicio(self, tipo, parametro):
        try:
            # Normaliza el texto del tipo de servicio.
            tipo = tipo.lower().strip()

            # Crea un servicio de spa.
            if tipo == "spa":
                servicio = ServicioSpa(parametro)

            # Crea un servicio de entrenamiento.
            elif tipo == "entrenamiento":
                servicio = ServicioEntrenamiento(parametro)

            # Crea un servicio de consultoría.
            elif tipo == "consultoria":
                servicio = ServicioConsultoria(parametro)

            # Si el tipo no existe, lanza error.
            else:
                raise DatosInvalidosError("Tipo de servicio desconocido.")

            # Guarda servicio en lista interna.
            self.servicios.append(servicio)

            # Registra evento.
            logging.info(f"Servicio creado: {servicio.resumen()}")

            # Retorna servicio creado.
            return servicio

        except TypeError as error:
            # Captura errores de tipo y los encadena.
            logging.error("Parámetro incorrecto al crear servicio.")
            raise DatosInvalidosError("Parámetro incorrecto para crear el servicio.") from error

        except SistemaReservaError as error:
            # Captura errores propios del sistema.
            logging.error(f"Error creando servicio: {error}")
            raise

    # Crea reserva con cliente, servicio y duración.
    def crear_reserva(self, cliente, servicio, duracion):
        try:
            # Crea objeto Reserva con validaciones.
            reserva = Reserva(cliente, servicio, duracion)

            # Guarda reserva en lista interna.
            self.reservas.append(reserva)

        except SistemaReservaError as error:
            # Registra error controlado.
            logging.error(f"Error creando reserva: {error}")
            raise

        else:
            # Registra éxito.
            logging.info(f"Reserva creada: {reserva.resumen()}")
            return reserva

    # Ejecuta al menos 10 operaciones completas válidas e inválidas.
    def simular_operaciones(self):
        # Lista donde se guardan resultados para mostrarlos en interfaz.
        resultados = []

        # Lista de funciones lambda. Cada una representa una operación.
        operaciones = [
            lambda: self.registrar_cliente("Ana Gómez", "ana@email.com", "3001234567"),     # Cliente válido.
            lambda: self.registrar_cliente("Li", "correo_invalido", "12"),                 # Cliente inválido.
            lambda: self.registrar_cliente("Carlos Ruiz", "carlos@email.com", "3109876543"), # Cliente válido.
            lambda: self.crear_servicio("spa", True),                                      # Servicio válido.
            lambda: self.crear_servicio("entrenamiento", "experto"),                       # Servicio inválido.
            lambda: self.crear_servicio("entrenamiento", "avanzado"),                      # Servicio válido.
            lambda: self.crear_servicio("consultoria", "virtual"),                         # Servicio válido.
            lambda: self.crear_reserva(self.clientes[0], self.servicios[0], 2),              # Reserva válida.
            lambda: self.crear_reserva("cliente falso", self.servicios[0], 1),              # Reserva inválida.
            lambda: self.crear_reserva(self.clientes[1], self.servicios[1], -3),             # Reserva inválida.
            lambda: self.crear_servicio("hotel", "premium"),                               # Tipo inválido.
            lambda: self.registrar_cliente("María López", "maria@email.com", "3215558888") # Cliente válido.
        ]

        # Recorre cada operación.
        for indice, operacion in enumerate(operaciones, start=1):
            try:
                # Ejecuta la operación.
                resultado = operacion()

                # Guarda resultado exitoso.
                resultados.append(f"Operación {indice}: OK -> {resultado}")

            except Exception as error:
                # Registra excepción completa sin detener el programa.
                logging.exception(f"Operación {indice} fallida y controlada.")

                # Guarda resultado fallido controlado.
                resultados.append(f"Operación {indice}: ERROR CONTROLADO -> {error}")

        # Procesa reservas válidas creadas durante la simulación.
        for reserva in self.reservas:
            try:
                # Confirma reserva.
                reserva.confirmar()

                # Procesa reserva.
                total = reserva.procesar()

                # Guarda resultado.
                resultados.append(f"Reserva procesada: {reserva.resumen()} | Total final: ${total:.2f}")

            except Exception as error:
                # Registra error sin detener aplicación.
                logging.exception("Error controlado procesando reserva durante simulación.")
                resultados.append(f"Procesamiento fallido controlado: {error}")

        # Devuelve resultados para mostrarlos en pantalla.
        return resultados
