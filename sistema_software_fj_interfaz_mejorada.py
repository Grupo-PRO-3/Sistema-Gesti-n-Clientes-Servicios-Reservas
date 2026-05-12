"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Empresa: Software FJ.
Curso: Programación 213023 - UNAD.
Fase 4 - Prácticas simuladas.

Este archivo fue documentado de forma detallada para cumplir con la guía,
la cual solicita explicar claramente el código desarrollado por el equipo.
El programa aplica programación orientada a objetos, clases abstractas,
herencia, polimorfismo, encapsulación, manejo de listas, excepciones
personalizadas, bloques try/except/else/finally, encadenamiento de
excepciones y registro de eventos en archivo log.
"""

from __future__ import annotations  # Permite usar anotaciones de tipo modernas sin problemas de compatibilidad.

from abc import ABC, abstractmethod  # Importa herramientas para crear clases abstractas y métodos obligatorios.
from dataclasses import dataclass  # Permite crear clases simples para almacenar datos de configuración.
from datetime import datetime  # Permite registrar la fecha y hora de creación de las entidades.
from functools import singledispatchmethod  # Permite simular sobrecarga de métodos según el tipo de dato recibido.
import logging  # Permite registrar eventos, errores y advertencias del sistema.
from logging.handlers import RotatingFileHandler  # Permite crear logs con rotación automática de archivos.
from pathlib import Path  # Permite manejar rutas de archivos de forma clara y multiplataforma.
import re  # Permite validar textos usando expresiones regulares.
import tkinter as tk  # Permite construir la interfaz gráfica principal.
from tkinter import ttk, messagebox  # Importa widgets modernos y ventanas emergentes de mensajes.


# ======================================================
# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS
# ======================================================

LOG_FILE = Path("sistema_software_fj.log")  # Define el nombre del archivo donde se guardarán eventos y errores.

logger = logging.getLogger("SoftwareFJ")  # Crea un registrador de eventos propio para el sistema.
logger.setLevel(logging.INFO)  # Define que se guardarán eventos informativos, errores y eventos críticos.
logger.propagate = False  # Evita que los mensajes se dupliquen en otros registradores de Python.

if not logger.handlers:  # Verifica que no exista un manejador previo para evitar registros duplicados.
    handler = RotatingFileHandler(  # Crea un manejador de archivo con rotación automática.
        LOG_FILE,  # Indica el archivo donde se almacenarán los logs.
        maxBytes=300_000,  # Define el tamaño máximo del archivo antes de crear otro respaldo.
        backupCount=3,  # Define cuántos archivos de respaldo se conservarán.
        encoding="utf-8"  # Define la codificación para permitir tildes y caracteres especiales.
    )
    formatter = logging.Formatter(  # Crea el formato que tendrá cada línea del log.
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"  # Fecha, nivel, sistema y mensaje.
    )
    handler.setFormatter(formatter)  # Asigna el formato anterior al manejador de logs.
    logger.addHandler(handler)  # Agrega el manejador configurado al registrador principal.


# ======================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ======================================================

class SistemaReservaError(Exception):
    """Excepción base para todos los errores controlados del sistema."""


class DatosInvalidosError(SistemaReservaError):
    """Se lanza cuando un dato recibido no cumple las reglas de validación."""


class ParametroFaltanteError(SistemaReservaError):
    """Se lanza cuando falta un dato obligatorio para ejecutar una operación."""


class OperacionNoPermitidaError(SistemaReservaError):
    """Se lanza cuando el usuario intenta realizar una acción no autorizada."""


class ServicioNoDisponibleError(SistemaReservaError):
    """Se lanza cuando se intenta reservar un servicio marcado como no disponible."""


class ReservaInvalidaError(SistemaReservaError):
    """Se lanza cuando una reserva se intenta crear con información incorrecta."""


class CalculoInconsistenteError(SistemaReservaError):
    """Se lanza cuando el cálculo de un costo produce un resultado incorrecto."""


# ======================================================
# 3. CLASE ABSTRACTA GENERAL DEL SISTEMA
# ======================================================

class EntidadSistema(ABC):
    """Clase abstracta que representa una entidad general del sistema."""

    _contador_global = 1  # Contador compartido para asignar identificadores únicos a cada entidad.

    def __init__(self) -> None:
        """Inicializa el identificador y la fecha de creación de la entidad."""
        self._id = EntidadSistema._contador_global  # Asigna el identificador actual a la entidad creada.
        EntidadSistema._contador_global += 1  # Incrementa el contador para la siguiente entidad.
        self._fecha_creacion = datetime.now()  # Guarda la fecha y hora exacta de creación.

    @property
    def id(self) -> int:
        """Retorna el identificador único de la entidad."""
        return self._id  # Devuelve el ID protegido sin permitir modificación directa.

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha de creación de la entidad."""
        return self._fecha_creacion  # Devuelve la fecha protegida de creación.

    @abstractmethod
    def resumen(self) -> str:
        """Obliga a cada clase hija a entregar un resumen textual de la entidad."""


# ======================================================
# 4. CLASE CLIENTE CON ENCAPSULACIÓN Y VALIDACIONES
# ======================================================

class Cliente(EntidadSistema):
    """Representa a un cliente de Software FJ con datos protegidos."""

    PATRON_CORREO = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")  # Patrón para validar correos electrónicos.

    def __init__(self, nombre: str, correo: str, telefono: str) -> None:
        """Crea un cliente validando nombre, correo y teléfono."""
        super().__init__()  # Ejecuta el constructor de EntidadSistema para asignar ID y fecha.
        self.__nombre = ""  # Crea atributo privado para almacenar el nombre del cliente.
        self.__correo = ""  # Crea atributo privado para almacenar el correo del cliente.
        self.__telefono = ""  # Crea atributo privado para almacenar el teléfono del cliente.
        self.nombre = nombre  # Usa el setter para validar y guardar el nombre recibido.
        self.correo = correo  # Usa el setter para validar y guardar el correo recibido.
        self.telefono = telefono  # Usa el setter para validar y guardar el teléfono recibido.

    @property
    def nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self.__nombre  # Devuelve el nombre privado de forma controlada.

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if not valor or not isinstance(valor, str):  # Verifica que el nombre exista y sea texto.
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")  # Informa falta de parámetro.
        valor = valor.strip()  # Elimina espacios innecesarios al inicio y al final.
        if len(valor) < 3:  # Verifica que el nombre tenga una longitud mínima aceptable.
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")  # Informa longitud inválida.
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):  # Verifica que solo contenga letras y espacios.
            raise DatosInvalidosError("El nombre solo debe contener letras y espacios.")  # Informa formato inválido.
        self.__nombre = valor.title()  # Guarda el nombre con formato de título.

    @property
    def correo(self) -> str:
        """Retorna el correo del cliente."""
        return self.__correo  # Devuelve el correo privado de forma controlada.

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida y asigna el correo electrónico del cliente."""
        if not valor or not isinstance(valor, str):  # Verifica que el correo exista y sea texto.
            raise ParametroFaltanteError("El correo del cliente es obligatorio.")  # Informa falta de correo.
        valor = valor.strip().lower()  # Elimina espacios y convierte el correo a minúsculas.
        if not self.PATRON_CORREO.match(valor):  # Comprueba si el correo cumple el patrón establecido.
            raise DatosInvalidosError("El correo no tiene un formato válido.")  # Informa formato inválido.
        self.__correo = valor  # Guarda el correo validado.

    @property
    def telefono(self) -> str:
        """Retorna el teléfono del cliente."""
        return self.__telefono  # Devuelve el teléfono privado de forma controlada.

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida y asigna el teléfono del cliente."""
        if not valor:  # Verifica que el teléfono no esté vacío.
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")  # Informa falta de teléfono.
        valor = str(valor).strip()  # Convierte el valor a texto y elimina espacios externos.
        if not valor.isdigit() or not (7 <= len(valor) <= 10):  # Valida que sea numérico y tenga longitud correcta.
            raise DatosInvalidosError("El teléfono debe ser numérico y tener entre 7 y 10 dígitos.")  # Informa error.
        self.__telefono = valor  # Guarda el teléfono validado.

    def resumen(self) -> str:
        """Entrega un resumen del cliente registrado."""
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | {self.telefono}"  # Retorna datos clave.

    def __str__(self) -> str:
        """Permite mostrar el cliente como texto legible."""
        return self.resumen()  # Usa el resumen como representación textual.


# ======================================================
# 5. CLASE ABSTRACTA SERVICIO
# ======================================================

class Servicio(EntidadSistema, ABC):
    """Clase abstracta para todos los servicios ofrecidos por Software FJ."""

    def __init__(self, nombre: str, precio_base: float, disponible: bool = True) -> None:
        """Inicializa los datos comunes de cualquier servicio."""
        super().__init__()  # Asigna identificador y fecha de creación desde la clase base.
        if not nombre or not isinstance(nombre, str):  # Verifica que el nombre del servicio sea válido.
            raise ParametroFaltanteError("El servicio necesita un nombre.")  # Informa falta de nombre.
        if precio_base <= 0:  # Verifica que el precio base sea positivo.
            raise DatosInvalidosError("El precio base debe ser mayor que cero.")  # Informa precio incorrecto.
        if not isinstance(disponible, bool):  # Verifica que la disponibilidad sea booleana.
            raise DatosInvalidosError("La disponibilidad debe ser True o False.")  # Informa tipo incorrecto.
        self.nombre = nombre.strip().title()  # Guarda el nombre limpio y con formato de título.
        self.precio_base = float(precio_base)  # Guarda el precio base como número decimal.
        self.disponible = disponible  # Guarda si el servicio está disponible para reservar.

    @abstractmethod
    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo del servicio según su duración."""

    @abstractmethod
    def describir(self) -> str:
        """Describe las características específicas del servicio."""

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los parámetros propios del servicio especializado."""

    @singledispatchmethod
    def calcular_total(self, valor) -> float:
        """Método sobrecargado base para calcular totales."""
        raise CalculoInconsistenteError("Tipo de dato no soportado para calcular total.")  # Controla tipos no válidos.

    @calcular_total.register
    def _(self, duracion: int) -> float:
        """Calcula el total cuando solo se recibe la duración."""
        return self.calcular_costo(duracion)  # Delega el cálculo al método polimórfico del servicio.

    @calcular_total.register
    def _(self, datos: tuple) -> float:
        """Calcula el total cuando se recibe duración, impuesto y descuento."""
        try:  # Inicia bloque para capturar errores de desempaquetado o cálculo.
            duracion, impuesto, descuento = datos  # Extrae duración, impuesto y descuento desde la tupla.
            subtotal = self.calcular_costo(duracion)  # Calcula el subtotal usando polimorfismo.
            total = subtotal + (subtotal * impuesto) - descuento  # Aplica impuesto y descuento al subtotal.
            if total < 0:  # Verifica que el resultado final no sea negativo.
                raise CalculoInconsistenteError("El total no puede ser negativo.")  # Lanza error controlado.
            return round(total, 2)  # Retorna el valor final redondeado a dos decimales.
        except ValueError as error:  # Captura errores cuando la tupla no tiene tres elementos.
            raise CalculoInconsistenteError("La tupla debe contener duración, impuesto y descuento.") from error  # Encadena excepción.

    def resumen(self) -> str:
        """Entrega un resumen general del servicio."""
        estado = "Disponible" if self.disponible else "No disponible"  # Convierte el estado booleano en texto.
        return f"Servicio #{self.id}: {self.nombre} | Base: ${self.precio_base:,.0f} | {estado}"  # Retorna resumen.

    def __str__(self) -> str:
        """Permite mostrar el servicio como texto legible."""
        return self.resumen()  # Usa el resumen como representación textual.


# ======================================================
# 6. SERVICIOS DERIVADOS SEGÚN SOFTWARE FJ
# ======================================================

class ReservaSala(Servicio):
    """Servicio especializado para reservar salas de reuniones o capacitaciones."""

    TIPOS_SALA = {"pequena": 1.0, "mediana": 1.35, "grande": 1.75}  # Opciones válidas y multiplicadores.

    def __init__(self, tipo_sala: str) -> None:
        """Crea un servicio de reserva de sala según el tipo seleccionado."""
        super().__init__("Reserva de Sala", 80_000)  # Inicializa el servicio con nombre y precio base.
        self.tipo_sala = tipo_sala.strip().lower() if isinstance(tipo_sala, str) else tipo_sala  # Normaliza el tipo.
        self.validar_parametros()  # Valida que el tipo de sala exista en las opciones permitidas.

    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo de la sala según duración y tamaño."""
        if duracion <= 0:  # Verifica que la duración sea positiva.
            raise CalculoInconsistenteError("La duración de la reserva de sala debe ser positiva.")  # Error controlado.
        multiplicador = self.TIPOS_SALA[self.tipo_sala]  # Obtiene el multiplicador según el tipo de sala.
        return round(self.precio_base * duracion * multiplicador, 2)  # Calcula y retorna el costo final.

    def describir(self) -> str:
        """Describe el servicio de reserva de sala."""
        return f"Reserva de sala tipo {self.tipo_sala} para reuniones o eventos empresariales."  # Retorna descripción.

    def validar_parametros(self) -> None:
        """Valida que el tipo de sala sea permitido."""
        if self.tipo_sala not in self.TIPOS_SALA:  # Comprueba si el tipo se encuentra en el diccionario.
            raise DatosInvalidosError("Tipo de sala inválido. Use: pequena, mediana o grande.")  # Informa error.


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquilar equipos tecnológicos."""

    EQUIPOS = {"portatil": 1.0, "proyector": 0.8, "sonido": 1.25}  # Equipos válidos y multiplicadores.

    def __init__(self, tipo_equipo: str) -> None:
        """Crea un servicio de alquiler según el equipo seleccionado."""
        super().__init__("Alquiler de Equipo", 55_000)  # Inicializa el servicio con nombre y precio base.
        self.tipo_equipo = tipo_equipo.strip().lower() if isinstance(tipo_equipo, str) else tipo_equipo  # Normaliza dato.
        self.validar_parametros()  # Valida que el tipo de equipo exista.

    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo de alquiler según duración y tipo de equipo."""
        if duracion <= 0:  # Verifica que la duración sea positiva.
            raise CalculoInconsistenteError("La duración del alquiler debe ser positiva.")  # Error controlado.
        multiplicador = self.EQUIPOS[self.tipo_equipo]  # Obtiene el multiplicador del equipo.
        return round(self.precio_base * duracion * multiplicador, 2)  # Calcula y retorna el costo.

    def describir(self) -> str:
        """Describe el servicio de alquiler de equipos."""
        return f"Alquiler de equipo tecnológico tipo {self.tipo_equipo}."  # Retorna descripción del servicio.

    def validar_parametros(self) -> None:
        """Valida que el equipo solicitado sea permitido."""
        if self.tipo_equipo not in self.EQUIPOS:  # Comprueba si el equipo está registrado.
            raise DatosInvalidosError("Tipo de equipo inválido. Use: portatil, proyector o sonido.")  # Informa error.


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas empresariales."""

    AREAS = {"software": 1.0, "redes": 1.2, "seguridad": 1.45}  # Áreas válidas y multiplicadores.

    def __init__(self, area: str) -> None:
        """Crea un servicio de asesoría según el área seleccionada."""
        super().__init__("Asesoría Especializada", 120_000)  # Inicializa el servicio con nombre y precio base.
        self.area = area.strip().lower() if isinstance(area, str) else area  # Normaliza el área recibida.
        self.validar_parametros()  # Valida que el área exista en las opciones permitidas.

    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo de la asesoría según duración y área."""
        if duracion <= 0:  # Verifica que la duración sea positiva.
            raise CalculoInconsistenteError("La duración de la asesoría debe ser positiva.")  # Error controlado.
        multiplicador = self.AREAS[self.area]  # Obtiene el multiplicador según el área.
        return round(self.precio_base * duracion * multiplicador, 2)  # Calcula y retorna el costo.

    def describir(self) -> str:
        """Describe el servicio de asesoría especializada."""
        return f"Asesoría especializada en el área de {self.area}."  # Retorna descripción del servicio.

    def validar_parametros(self) -> None:
        """Valida que el área de asesoría sea permitida."""
        if self.area not in self.AREAS:  # Comprueba si el área está registrada.
            raise DatosInvalidosError("Área inválida. Use: software, redes o seguridad.")  # Informa error.


# ======================================================
# 7. CLASE RESERVA
# ======================================================

class Reserva(EntidadSistema):
    """Integra cliente, servicio, duración, estado y total calculado."""

    ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "procesada"}  # Estados permitidos.

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: int) -> None:
        """Crea una reserva validando cliente, servicio y duración."""
        super().__init__()  # Asigna ID y fecha de creación a la reserva.
        if not isinstance(cliente, Cliente):  # Valida que el cliente sea un objeto Cliente.
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")  # Informa cliente inválido.
        if not isinstance(servicio, Servicio):  # Valida que el servicio herede de Servicio.
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")  # Informa servicio inválido.
        if not isinstance(duracion, int):  # Valida que la duración sea entera.
            raise ReservaInvalidaError("La duración debe ser un número entero.")  # Informa duración inválida.
        if duracion <= 0:  # Valida que la duración sea positiva.
            raise ReservaInvalidaError("La duración de la reserva debe ser positiva.")  # Informa error de duración.
        if not servicio.disponible:  # Verifica que el servicio esté disponible.
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")  # Informa no disponibilidad.
        self.cliente = cliente  # Guarda el cliente asociado a la reserva.
        self.servicio = servicio  # Guarda el servicio asociado a la reserva.
        self.duracion = duracion  # Guarda la duración de la reserva.
        self.estado = "pendiente"  # Define el estado inicial de la reserva.
        self.total = 0.0  # Inicializa el total en cero antes de procesar.

    def confirmar(self) -> bool:
        """Confirma una reserva pendiente utilizando try/except/else/finally."""
        try:  # Intenta confirmar la reserva.
            if self.estado != "pendiente":  # Verifica que la reserva esté pendiente.
                raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")  # Error controlado.
            self.estado = "confirmada"  # Cambia el estado a confirmada.
        except OperacionNoPermitidaError as error:  # Captura errores de confirmación.
            logger.error("Error confirmando reserva #%s: %s", self.id, error)  # Registra el error en el log.
            raise  # Vuelve a lanzar el error para que la interfaz o simulación lo controle.
        else:  # Se ejecuta solo si no ocurrió ningún error.
            logger.info("Reserva confirmada: %s", self.resumen())  # Registra confirmación exitosa.
            return True  # Retorna éxito.
        finally:  # Se ejecuta siempre, exista o no error.
            logger.info("Intento de confirmación finalizado para reserva #%s.", self.id)  # Registra cierre.

    def cancelar(self) -> bool:
        """Cancela una reserva si su estado lo permite."""
        try:  # Intenta cancelar la reserva.
            if self.estado == "procesada":  # Valida que no esté procesada.
                raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")  # Error controlado.
            if self.estado == "cancelada":  # Valida que no esté cancelada previamente.
                raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")  # Error controlado.
            self.estado = "cancelada"  # Cambia el estado a cancelada.
        except OperacionNoPermitidaError as error:  # Captura errores de cancelación.
            logger.error("Error cancelando reserva #%s: %s", self.id, error)  # Registra el error.
            raise  # Propaga el error controlado.
        else:  # Se ejecuta si la cancelación fue exitosa.
            logger.info("Reserva cancelada: %s", self.resumen())  # Registra cancelación correcta.
            return True  # Retorna éxito.
        finally:  # Se ejecuta al finalizar el intento.
            logger.info("Intento de cancelación finalizado para reserva #%s.", self.id)  # Registra cierre.

    def procesar(self) -> float:
        """Procesa la reserva confirmada y calcula el valor final."""
        try:  # Intenta procesar la reserva.
            if self.estado != "confirmada":  # Verifica que la reserva esté confirmada.
                raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")  # Error controlado.
            self.total = self.servicio.calcular_total((self.duracion, 0.19, 5_000))  # Calcula total con IVA y descuento.
            self.estado = "procesada"  # Cambia el estado a procesada.
        except SistemaReservaError as error:  # Captura errores personalizados del sistema.
            logger.error("Error procesando reserva #%s: %s", self.id, error)  # Registra error controlado.
            raise  # Propaga el error.
        except Exception as error:  # Captura errores inesperados no contemplados.
            logger.critical("Error inesperado procesando reserva #%s: %s", self.id, error, exc_info=True)  # Log crítico.
            raise SistemaReservaError("Fallo general al procesar la reserva.") from error  # Encadena excepción inesperada.
        else:  # Se ejecuta si el procesamiento fue exitoso.
            logger.info("Reserva procesada correctamente: %s", self.resumen())  # Registra éxito.
            return self.total  # Retorna el total calculado.
        finally:  # Se ejecuta siempre al finalizar el procesamiento.
            logger.info("Proceso de reserva #%s finalizado con estado %s.", self.id, self.estado)  # Registra cierre.

    def resumen(self) -> str:
        """Entrega un resumen completo de la reserva."""
        return (  # Construye una cadena de texto con los datos principales.
            f"Reserva #{self.id}: {self.cliente.nombre} - {self.servicio.nombre} | "  # Cliente y servicio.
            f"Duración: {self.duracion}h | Estado: {self.estado} | Total: ${self.total:,.0f}"  # Duración, estado y total.
        )

    def __str__(self) -> str:
        """Permite mostrar la reserva como texto legible."""
        return self.resumen()  # Usa el resumen como representación textual.


# ======================================================
# 8. GESTOR DEL SISTEMA CON LISTAS INTERNAS
# ======================================================

class GestorReservas:
    """Administra clientes, servicios y reservas sin utilizar base de datos."""

    def __init__(self) -> None:
        """Inicializa las listas internas del sistema."""
        self.clientes: list[Cliente] = []  # Lista interna para almacenar clientes registrados.
        self.servicios: list[Servicio] = []  # Lista interna para almacenar servicios creados.
        self.reservas: list[Reserva] = []  # Lista interna para almacenar reservas creadas.

    def registrar_cliente(self, nombre: str, correo: str, telefono: str) -> Cliente:
        """Registra un cliente validando los datos de entrada."""
        try:  # Intenta crear y registrar el cliente.
            cliente = Cliente(nombre, correo, telefono)  # Crea el objeto Cliente con validaciones.
            self.clientes.append(cliente)  # Agrega el cliente a la lista interna.
        except SistemaReservaError as error:  # Captura errores personalizados del registro.
            logger.error("Error registrando cliente: %s", error)  # Guarda el error en el log.
            raise  # Propaga el error para que sea mostrado o controlado externamente.
        else:  # Se ejecuta cuando el registro fue correcto.
            logger.info("Cliente registrado: %s", cliente.resumen())  # Registra el evento exitoso.
            return cliente  # Retorna el cliente creado.
        finally:  # Se ejecuta siempre al terminar la operación.
            logger.info("Operación registrar_cliente finalizada.")  # Registra finalización.

    def crear_servicio(self, tipo: str, parametro: str) -> Servicio:
        """Crea un servicio según el tipo y parámetro seleccionados."""
        try:  # Intenta crear el servicio solicitado.
            if not tipo:  # Verifica que el tipo no esté vacío.
                raise ParametroFaltanteError("Debe seleccionar un tipo de servicio.")  # Error controlado.
            tipo_normalizado = tipo.strip().lower()  # Limpia y normaliza el tipo de servicio.
            mapa_servicios = {  # Diccionario que relaciona texto de entrada con clases concretas.
                "reserva sala": ReservaSala,  # Asocia reserva de sala con su clase.
                "alquiler equipo": AlquilerEquipo,  # Asocia alquiler de equipo con su clase.
                "asesoria especializada": AsesoriaEspecializada,  # Asocia asesoría con su clase.
            }
            clase_servicio = mapa_servicios.get(tipo_normalizado)  # Busca la clase correspondiente al tipo.
            if clase_servicio is None:  # Verifica si el tipo solicitado existe.
                raise DatosInvalidosError("Tipo de servicio desconocido. Use: reserva sala, alquiler equipo o asesoria especializada.")  # Error.
            servicio = clase_servicio(parametro)  # Crea el servicio usando polimorfismo de clases.
            self.servicios.append(servicio)  # Agrega el servicio a la lista interna.
        except TypeError as error:  # Captura errores de parámetros incorrectos.
            logger.error("Parámetro incorrecto al crear servicio.", exc_info=True)  # Registra información técnica.
            raise DatosInvalidosError("Parámetro incorrecto para crear el servicio.") from error  # Encadena excepción.
        except SistemaReservaError as error:  # Captura errores personalizados del servicio.
            logger.error("Error creando servicio: %s", error)  # Guarda el error en el log.
            raise  # Propaga el error.
        else:  # Se ejecuta si el servicio fue creado correctamente.
            logger.info("Servicio creado: %s", servicio.resumen())  # Registra evento exitoso.
            return servicio  # Retorna el servicio creado.
        finally:  # Se ejecuta siempre al finalizar la operación.
            logger.info("Operación crear_servicio finalizada.")  # Registra finalización.

    def crear_reserva(self, cliente: Cliente, servicio: Servicio, duracion: int) -> Reserva:
        """Crea una reserva con cliente, servicio y duración."""
        try:  # Intenta crear la reserva.
            reserva = Reserva(cliente, servicio, duracion)  # Crea la reserva aplicando validaciones.
            self.reservas.append(reserva)  # Agrega la reserva a la lista interna.
        except SistemaReservaError as error:  # Captura errores personalizados de reserva.
            logger.error("Error creando reserva: %s", error)  # Registra el error.
            raise  # Propaga el error.
        else:  # Se ejecuta cuando la reserva fue creada correctamente.
            logger.info("Reserva creada: %s", reserva.resumen())  # Registra éxito.
            return reserva  # Retorna la reserva creada.
        finally:  # Se ejecuta siempre al finalizar la operación.
            logger.info("Operación crear_reserva finalizada.")  # Registra cierre.

    def simular_operaciones(self) -> list[str]:
        """Simula más de 10 operaciones válidas e inválidas para demostrar robustez."""
        resultados: list[str] = []  # Lista donde se guardan los resultados de la simulación.
        operaciones = [  # Lista de funciones anónimas para ejecutar operaciones secuenciales.
            lambda: self.registrar_cliente("Ana Gómez", "ana@email.com", "3001234567"),  # Cliente válido.
            lambda: self.registrar_cliente("Li", "correo_invalido", "12"),  # Cliente inválido.
            lambda: self.registrar_cliente("Carlos Ruiz", "carlos@email.com", "3109876543"),  # Cliente válido.
            lambda: self.crear_servicio("reserva sala", "grande"),  # Servicio válido.
            lambda: self.crear_servicio("reserva sala", "gigante"),  # Servicio inválido.
            lambda: self.crear_servicio("alquiler equipo", "portatil"),  # Servicio válido.
            lambda: self.crear_servicio("asesoria especializada", "seguridad"),  # Servicio válido.
            lambda: self.crear_reserva(self.clientes[0], self.servicios[0], 2),  # Reserva válida.
            lambda: self.crear_reserva("cliente falso", self.servicios[0], 1),  # Reserva con cliente inválido.
            lambda: self.crear_reserva(self.clientes[1], self.servicios[1], -3),  # Reserva con duración inválida.
            lambda: self.crear_servicio("hotel", "premium"),  # Tipo de servicio inexistente.
            lambda: self.registrar_cliente("María López", "maria@email.com", "3215558888"),  # Cliente válido.
        ]
        for indice, operacion in enumerate(operaciones, start=1):  # Recorre cada operación con número consecutivo.
            try:  # Intenta ejecutar la operación actual.
                resultado = operacion()  # Ejecuta la función anónima seleccionada.
            except Exception as error:  # Captura cualquier error para que el programa no se detenga.
                logger.exception("Operación %s fallida y controlada.", indice)  # Registra error completo.
                resultados.append(f"Operación {indice}: ERROR CONTROLADO -> {error}")  # Guarda resultado fallido.
            else:  # Se ejecuta si la operación no generó error.
                resultados.append(f"Operación {indice}: OK -> {resultado}")  # Guarda resultado exitoso.
        for reserva in self.reservas:  # Recorre las reservas creadas correctamente.
            try:  # Intenta confirmar y procesar cada reserva.
                reserva.confirmar()  # Confirma la reserva pendiente.
                total = reserva.procesar()  # Procesa la reserva y calcula el total.
            except Exception as error:  # Captura errores durante el procesamiento.
                logger.exception("Error controlado procesando reserva durante simulación.")  # Registra error.
                resultados.append(f"Procesamiento fallido controlado: {error}")  # Guarda resultado fallido.
            else:  # Se ejecuta si la reserva fue procesada correctamente.
                resultados.append(f"Reserva procesada: {reserva.resumen()} | Total final: ${total:,.0f}")  # Guarda éxito.
        return resultados  # Retorna todos los resultados de la simulación.


# ======================================================
# 9. INTERFAZ GRÁFICA DEL SISTEMA
# ======================================================

@dataclass(frozen=True)
class TemaVisual:
    """Almacena los colores principales de la interfaz gráfica."""
    fondo: str = "#F4F6F8"  # Color de fondo general.
    panel: str = "#FFFFFF"  # Color de los paneles de contenido.
    primario: str = "#1F6FEB"  # Color principal del encabezado y botones.
    secundario: str = "#344054"  # Color secundario para textos y botones.
    texto: str = "#101828"  # Color principal de texto.


class AppReservas:
    """Ventana principal para gestionar clientes, servicios y reservas."""

    def __init__(self, root: tk.Tk) -> None:
        """Inicializa la ventana, el tema y el gestor del sistema."""
        self.root = root  # Guarda la ventana principal de Tkinter.
        self.root.title("Software FJ - Gestión de Clientes, Servicios y Reservas")  # Define el título de la ventana.
        self.root.geometry("1365x760")  # Define un tamaño amplio para visualizar toda la interfaz.
        self.root.minsize(1180, 680)  # Define un tamaño mínimo amplio para evitar cortes visuales.
        try:  # Intenta maximizar la ventana en Windows para mostrar toda la información.
            self.root.state("zoomed")  # Maximiza la ventana principal automáticamente.
        except tk.TclError:  # Si el sistema no permite maximizar, continúa con el tamaño definido.
            pass  # Mantiene la ventana con la geometría configurada anteriormente.
        self.tema = TemaVisual()  # Crea la configuración visual de colores.
        self.gestor = GestorReservas()  # Crea el gestor lógico de clientes, servicios y reservas.
        self.root.configure(bg=self.tema.fondo)  # Aplica el color de fondo a la ventana.
        self._configurar_estilos()  # Configura estilos visuales de widgets ttk.
        self._crear_interfaz()  # Construye todos los elementos de la interfaz.

    def _configurar_estilos(self) -> None:
        """Configura los estilos visuales de los widgets ttk."""
        style = ttk.Style()  # Crea el objeto de estilos de Tkinter.
        style.theme_use("clam")  # Usa un tema compatible y modificable.
        style.configure("TLabel", background=self.tema.panel, foreground=self.tema.texto, font=("Segoe UI", 10))  # Etiquetas.
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)  # Botones generales.
        style.configure("Primary.TButton", background=self.tema.primario, foreground="white")  # Botón principal.
        style.configure("Secondary.TButton", background=self.tema.secundario, foreground="white")  # Botón secundario.
        style.configure("TCombobox", padding=4)  # Lista desplegable.

    def _crear_interfaz(self) -> None:
        """Crea la estructura principal de la interfaz gráfica."""
        encabezado = tk.Frame(self.root, bg=self.tema.primario, height=70)  # Crea una franja superior más compacta.
        encabezado.pack(fill="x")  # Hace que el encabezado ocupe todo el ancho.
        encabezado.pack_propagate(False)  # Mantiene la altura configurada.
        tk.Label(encabezado, text="Software FJ", bg=self.tema.primario, fg="white", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=24, pady=(8, 0))  # Título.
        tk.Label(encabezado, text="Sistema integral de gestión de clientes, servicios y reservas", bg=self.tema.primario, fg="white", font=("Segoe UI", 10)).pack(anchor="w", padx=26)  # Subtítulo.
        contenedor = tk.Frame(self.root, bg=self.tema.fondo)  # Crea contenedor general inferior.
        contenedor.pack(fill="both", expand=True, padx=14, pady=10)  # Reduce márgenes para aprovechar mejor la pantalla.
        panel_izquierdo = tk.Frame(contenedor, bg=self.tema.panel, relief="solid", bd=1, width=300)  # Panel izquierdo compacto.
        panel_izquierdo.pack(side="left", fill="y")  # Ubica el panel izquierdo.
        panel_izquierdo.pack_propagate(False)  # Conserva el ancho establecido del panel.
        canvas_formulario = tk.Canvas(panel_izquierdo, bg=self.tema.panel, highlightthickness=0, width=278)  # Área desplazable para formularios.
        barra_formulario = ttk.Scrollbar(panel_izquierdo, orient="vertical", command=canvas_formulario.yview)  # Barra vertical del formulario.
        panel_formulario = tk.Frame(canvas_formulario, bg=self.tema.panel, padx=14, pady=12)  # Contenido interno del formulario.
        panel_formulario.bind("<Configure>", lambda evento: canvas_formulario.configure(scrollregion=canvas_formulario.bbox("all")))  # Actualiza región visible.
        canvas_formulario.create_window((0, 0), window=panel_formulario, anchor="nw", width=278)  # Inserta el formulario dentro del canvas.
        canvas_formulario.configure(yscrollcommand=barra_formulario.set)  # Conecta el canvas con la barra de desplazamiento.
        canvas_formulario.pack(side="left", fill="both", expand=True)  # Ubica el formulario desplazable.
        barra_formulario.pack(side="right", fill="y")  # Ubica la barra de desplazamiento.
        panel_salida = tk.Frame(contenedor, bg=self.tema.panel, padx=12, pady=12, relief="solid", bd=1)  # Panel derecho.
        panel_salida.pack(side="right", fill="both", expand=True, padx=(14, 0))  # Ubica salida a la derecha.
        self._crear_formulario_cliente(panel_formulario)  # Agrega sección de clientes.
        self._crear_formulario_servicio(panel_formulario)  # Agrega sección de servicios.
        self._crear_formulario_reserva(panel_formulario)  # Agrega sección de reservas.
        self._crear_salida(panel_salida)  # Agrega consola de resultados.

    def _crear_formulario_cliente(self, padre: tk.Frame) -> None:
        """Crea los campos para registrar clientes."""
        tk.Label(padre, text="Registro de cliente", bg=self.tema.panel, fg=self.tema.texto, font=("Segoe UI", 13, "bold")).pack(anchor="w")  # Título.
        self.nombre_entry = self._crear_campo(padre, "Nombre")  # Campo para nombre.
        self.correo_entry = self._crear_campo(padre, "Correo")  # Campo para correo.
        self.telefono_entry = self._crear_campo(padre, "Teléfono")  # Campo para teléfono.
        ttk.Button(padre, text="Registrar cliente", style="Primary.TButton", command=self.registrar_cliente_ui).pack(fill="x", pady=(6, 12))  # Botón.

    def _crear_formulario_servicio(self, padre: tk.Frame) -> None:
        """Crea los campos para crear servicios."""
        tk.Label(padre, text="Creación de servicio", bg=self.tema.panel, fg=self.tema.texto, font=("Segoe UI", 13, "bold")).pack(anchor="w")  # Título.
        tk.Label(padre, text="Tipo de servicio", bg=self.tema.panel).pack(anchor="w", pady=(8, 2))  # Etiqueta del selector.
        self.tipo_servicio = ttk.Combobox(padre, values=["reserva sala", "alquiler equipo", "asesoria especializada"], state="readonly")  # Selector.
        self.tipo_servicio.pack(fill="x")  # Ubica el selector.
        self.tipo_servicio.set("reserva sala")  # Define opción inicial.
        self.parametro_entry = self._crear_campo(padre, "Parámetro")  # Campo para parámetro específico.
        self.parametro_entry.insert(0, "grande")  # Valor inicial sugerido.
        ttk.Button(padre, text="Crear servicio", style="Primary.TButton", command=self.crear_servicio_ui).pack(fill="x", pady=(6, 10))  # Botón.
        ayuda = "Parámetros permitidos:\n• reserva sala: pequena, mediana, grande\n• alquiler equipo: portatil, proyector, sonido\n• asesoria especializada: software, redes, seguridad"  # Texto de ayuda.
        tk.Label(padre, text=ayuda, bg=self.tema.panel, fg=self.tema.secundario, justify="left", font=("Segoe UI", 8)).pack(anchor="w", pady=(0, 8))  # Muestra ayuda.

    def _crear_formulario_reserva(self, padre: tk.Frame) -> None:
        """Crea los controles para generar y simular reservas."""
        tk.Label(padre, text="Reserva", bg=self.tema.panel, fg=self.tema.texto, font=("Segoe UI", 13, "bold")).pack(anchor="w")  # Título.
        self.duracion_entry = self._crear_campo(padre, "Duración en horas")  # Campo de duración.
        self.duracion_entry.insert(0, "2")  # Valor inicial sugerido.
        ttk.Button(padre, text="Crear, confirmar y procesar reserva", style="Secondary.TButton", command=self.crear_reserva_ui).pack(fill="x", pady=(8, 8))  # Botón reserva.
        ttk.Button(padre, text="Ejecutar simulación 10+ operaciones", command=self.simular_ui).pack(fill="x", pady=(0, 8))  # Botón simulación.
        ttk.Button(padre, text="Limpiar salida", command=self.limpiar_salida).pack(fill="x")  # Botón limpiar.

    def _crear_campo(self, padre: tk.Frame, etiqueta: str) -> tk.Entry:
        """Crea una etiqueta y una caja de texto reutilizable."""
        tk.Label(padre, text=etiqueta, bg=self.tema.panel).pack(anchor="w", pady=(8, 2))  # Crea etiqueta.
        entrada = tk.Entry(padre, font=("Segoe UI", 10), relief="solid", bd=1)  # Crea caja de texto.
        entrada.pack(fill="x", ipady=4)  # Ubica la caja de texto con altura compacta.
        return entrada  # Retorna la caja para usarla después.

    def _crear_salida(self, padre: tk.Frame) -> None:
        """Crea el área donde se muestran los resultados."""
        tk.Label(padre, text="Resultados de ejecución", bg=self.tema.panel, fg=self.tema.texto, font=("Segoe UI", 13, "bold")).pack(anchor="w")  # Título.
        self.salida = tk.Text(padre, height=28, bg="#0B1220", fg="#E6EDF3", insertbackground="white", font=("Consolas", 10), wrap="word")  # Consola visual amplia.
        self.salida.pack(fill="both", expand=True, pady=(8, 0))  # Ubica consola.
        self.escribir("Sistema iniciado correctamente. Registre clientes, cree servicios o ejecute la simulación.")  # Mensaje inicial.

    def escribir(self, texto: str) -> None:
        """Escribe una línea de texto en el panel de resultados."""
        self.salida.insert(tk.END, texto + "\n")  # Inserta texto al final del panel.
        self.salida.see(tk.END)  # Desplaza la vista hasta la última línea.

    def limpiar_salida(self) -> None:
        """Limpia el panel de resultados."""
        self.salida.delete("1.0", tk.END)  # Elimina todo el contenido del panel.

    def registrar_cliente_ui(self) -> None:
        """Registra un cliente desde la interfaz gráfica."""
        try:  # Intenta registrar el cliente con los datos escritos por el usuario.
            cliente = self.gestor.registrar_cliente(self.nombre_entry.get(), self.correo_entry.get(), self.telefono_entry.get())  # Registra.
        except SistemaReservaError as error:  # Captura errores controlados.
            messagebox.showerror("Error controlado", str(error))  # Muestra ventana de error.
            self.escribir(f"ERROR: {error}")  # Escribe error en el panel.
        else:  # Se ejecuta si el registro fue correcto.
            self.escribir(f"Cliente registrado: {cliente.resumen()}")  # Escribe confirmación.

    def crear_servicio_ui(self) -> None:
        """Crea un servicio desde la interfaz gráfica."""
        try:  # Intenta crear el servicio.
            servicio = self.gestor.crear_servicio(self.tipo_servicio.get(), self.parametro_entry.get())  # Crea servicio.
        except SistemaReservaError as error:  # Captura errores controlados.
            messagebox.showerror("Error controlado", str(error))  # Muestra ventana de error.
            self.escribir(f"ERROR: {error}")  # Escribe error en consola.
        else:  # Se ejecuta si el servicio fue creado.
            self.escribir(f"Servicio creado: {servicio.resumen()} | {servicio.describir()}")  # Escribe confirmación.

    def crear_reserva_ui(self) -> None:
        """Crea, confirma y procesa una reserva desde la interfaz."""
        try:  # Intenta ejecutar el flujo completo de reserva.
            if not self.gestor.clientes:  # Verifica que exista al menos un cliente.
                raise ReservaInvalidaError("Debe registrar al menos un cliente antes de reservar.")  # Error controlado.
            if not self.gestor.servicios:  # Verifica que exista al menos un servicio.
                raise ReservaInvalidaError("Debe crear al menos un servicio antes de reservar.")  # Error controlado.
            duracion = int(self.duracion_entry.get())  # Convierte la duración escrita a número entero.
            reserva = self.gestor.crear_reserva(self.gestor.clientes[-1], self.gestor.servicios[-1], duracion)  # Crea reserva.
            reserva.confirmar()  # Confirma la reserva.
            reserva.procesar()  # Procesa la reserva.
        except ValueError as error:  # Captura error si la duración no es numérica.
            logger.error("Duración no numérica.", exc_info=True)  # Registra error técnico.
            messagebox.showerror("Error", "La duración debe ser un número entero.")  # Muestra aviso.
            self.escribir("ERROR: La duración debe ser un número entero.")  # Escribe error.
        except SistemaReservaError as error:  # Captura errores personalizados del sistema.
            messagebox.showerror("Error controlado", str(error))  # Muestra aviso.
            self.escribir(f"ERROR: {error}")  # Escribe error.
        else:  # Se ejecuta si la reserva fue exitosa.
            self.escribir(f"Reserva exitosa: {reserva.resumen()}")  # Escribe confirmación.
        finally:  # Se ejecuta siempre al finalizar el intento.
            logger.info("Operación crear_reserva_ui finalizada.")  # Registra cierre.

    def simular_ui(self) -> None:
        """Ejecuta la simulación de operaciones válidas e inválidas."""
        self.escribir("\n===== SIMULACIÓN INICIADA =====")  # Muestra inicio de simulación.
        resultados = self.gestor.simular_operaciones()  # Ejecuta las operaciones de prueba.
        for resultado in resultados:  # Recorre los resultados obtenidos.
            self.escribir(resultado)  # Muestra cada resultado en el panel.
        self.escribir("===== SIMULACIÓN FINALIZADA =====")  # Muestra fin de simulación.
        self.escribir(f"Logs registrados en: {LOG_FILE}\n")  # Informa ubicación del log.


# ======================================================
# 10. FUNCIÓN PRINCIPAL
# ======================================================

def main() -> None:
    """Punto de entrada principal de la aplicación."""
    try:  # Intenta iniciar la aplicación.
        logger.info("Aplicación iniciada.")  # Registra inicio del programa.
        root = tk.Tk()  # Crea la ventana principal de Tkinter.
        AppReservas(root)  # Crea la aplicación con su interfaz y lógica.
        root.mainloop()  # Mantiene la ventana abierta esperando interacción del usuario.
    except Exception as error:  # Captura errores críticos no controlados.
        logger.critical("Error crítico en la aplicación: %s", error, exc_info=True)  # Registra detalle crítico.
        raise  # Propaga el error para no ocultar fallas graves durante desarrollo.
    finally:  # Se ejecuta al cerrar o fallar la aplicación.
        logger.info("Aplicación finalizada.")  # Registra finalización del programa.


if __name__ == "__main__":  # Verifica que el archivo se esté ejecutando directamente.
    main()  # Ejecuta la función principal del sistema.
