# APORTE 1 - Jesus Villadiego
# Sección: configuración, logs, excepciones, clase abstracta general y clase Cliente.
# Este fragmento corresponde al inicio del sistema Software FJ.

"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Empresa: Software FJ.
Curso: Programación 213023 - UNAD.
Grupo: 213023_36.
Fase 4 - Prácticas simuladas.
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


