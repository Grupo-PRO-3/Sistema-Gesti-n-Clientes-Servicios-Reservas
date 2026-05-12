# APORTE 3 - Victor Jaraba
# Sección: clase Reserva, estados, confirmación, cancelación y procesamiento.
# Este fragmento depende de los Aportes 1 y 2.

class Reserva(EntidadSistema):

    # Estados permitidos para una reserva.
    ESTADOS_VALIDOS = ["pendiente", "confirmada", "cancelada", "procesada"]

    # Constructor de reserva.
    def __init__(self, cliente, servicio, duracion):
        # Inicializa ID y fecha.
        super().__init__()

        # Valida que cliente sea un objeto Cliente.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")

        # Valida que servicio sea un objeto Servicio.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")

        # Valida duración positiva.
        if duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser positiva.")

        # Valida disponibilidad del servicio.
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")

        # Guarda los datos de la reserva.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"
        self.total = 0

    # Confirma una reserva pendiente.
    def confirmar(self):
        try:
            # Solo se pueden confirmar reservas pendientes.
            if self.estado != "pendiente":
                raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")

            # Cambia estado a confirmada.
            self.estado = "confirmada"

            # Registra evento exitoso.
            logging.info(f"Reserva confirmada: {self.resumen()}")

        except OperacionNoPermitidaError as error:
            # Registra error controlado.
            logging.error(error)

            # Relanza el error para que la interfaz o simulación lo maneje.
            raise

        else:
            # Se ejecuta solo si no hubo excepción.
            return True

        finally:
            # Se ejecuta siempre, haya error o no.
            logging.info(f"Intento de confirmación finalizado para reserva #{self.id}.")

    # Cancela una reserva si las reglas lo permiten.
    def cancelar(self):
        try:
            # No se puede cancelar una reserva procesada.
            if self.estado == "procesada":
                raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")

            # No se puede cancelar dos veces.
            if self.estado == "cancelada":
                raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")

            # Cambia estado a cancelada.
            self.estado = "cancelada"

            # Registra cancelación.
            logging.info(f"Reserva cancelada: {self.resumen()}")

        except OperacionNoPermitidaError as error:
            # Registra error.
            logging.error(error)
            raise

        finally:
            # Siempre registra fin del intento.
            logging.info(f"Intento de cancelación finalizado para reserva #{self.id}.")

    # Procesa la reserva y calcula total final.
    def procesar(self):
        try:
            # Solo se pueden procesar reservas confirmadas.
            if self.estado != "confirmada":
                raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")

            # Calcula total usando método sobrecargado con tupla.
            # Parámetros: duración, impuesto del 19%, descuento de 5000.
            self.total = self.servicio.calcular_total((self.duracion, 0.19, 5000))

            # Cambia estado a procesada.
            self.estado = "procesada"

        except SistemaReservaError as error:
            # Registra errores propios del sistema.
            logging.error(f"Error procesando reserva: {error}")
            raise

        except Exception as error:
            # Captura cualquier error inesperado.
            logging.critical(f"Error inesperado procesando reserva: {error}")

            # Encadena excepción inesperada dentro de una excepción del sistema.
            raise SistemaReservaError("Fallo general al procesar la reserva.") from error

        else:
            # Se ejecuta solo si todo salió bien.
            logging.info(f"Reserva procesada correctamente: {self.resumen()} | Total: ${self.total:.2f}")
            return self.total

        finally:
            # Siempre se ejecuta al terminar el procesamiento.
            logging.info(f"Proceso de reserva #{self.id} finalizado con estado {self.estado}.")

    # Resumen de reserva.
    def resumen(self):
        return (
            f"Reserva #{self.id}: {self.cliente.nombre} - {self.servicio.nombre} | "
            f"Duración: {self.duracion}h | Estado: {self.estado} | Total: ${self.total:.2f}"
        )

    # Representación textual.
    def __str__(self):
        return self.resumen()
