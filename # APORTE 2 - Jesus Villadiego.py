# APORTE 2 - Jesus Villadiego
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
from __future__ import annotations


# ======================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ======================================================

# Archivo donde se almacenarán eventos y errores
LOG_FILE = Path("sistema_software_fj.log")

# Creación del logger principal del sistema
logger = logging.getLogger("SoftwareFJ")

# Nivel mínimo de eventos que se guardarán
logger.setLevel(logging.INFO)

# Evita duplicación de mensajes
logger.propagate = False


# Verifica si ya existen manejadores
if not logger.handlers:

    # Configuración de rotación automática del archivo
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=300_000,
        backupCount=3,
        encoding="utf-8"
    )

    # Formato del registro de eventos
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Asignación del formato al handler
    handler.setFormatter(formatter)

    # Agrega el manejador al logger
    logger.addHandler(handler)


# ======================================================
# EXCEPCIONES PERSONALIZADAS
# ======================================================

class SistemaReservaError(Exception):
    """
    Excepción base para errores controlados del sistema.
    """
    pass


class DatosInvalidosError(SistemaReservaError):
    """
    Error generado cuando los datos ingresados
    no cumplen las validaciones establecidas.
    """
    pass


class ParametroFaltanteError(SistemaReservaError):
    """
    Error generado cuando falta información obligatoria.
    """
    pass


class OperacionNoPermitidaError(SistemaReservaError):
    """
    Error generado cuando se intenta realizar
    una operación no permitida.
    """
    pass


class ServicioNoDisponibleError(SistemaReservaError):
    """
    Error generado cuando un servicio no se encuentra disponible.
    """
    pass


class ReservaInvalidaError(SistemaReservaError):
    """
    Error generado cuando la reserva posee datos incorrectos.
    """
    pass


class CalculoInconsistenteError(SistemaReservaError):
    """
    Error generado cuando ocurre un fallo
    en el cálculo de costos.
    """
    pass


# ======================================================
# CLASE ABSTRACTA GENERAL
# ======================================================

class EntidadSistema(ABC):
    """
    Clase abstracta principal del sistema.
    Representa cualquier entidad general.
    """

    # Contador global automático
    _contador_global = 1

    def __init__(self):

        # Identificador único
        self._id = EntidadSistema._contador_global

        # Incrementa el contador
        EntidadSistema._contador_global += 1

        # Fecha de creación
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        """
        Retorna el identificador de la entidad.
        """
        return self._id

    @property
    def fecha_creacion(self):
        """
        Retorna la fecha de creación.
        """
        return self._fecha_creacion

    @abstractmethod
    def resumen(self):
        """
        Método obligatorio para clases hijas.
        """
        pass


# ======================================================
# CLASE CLIENTE
# ======================================================

class Cliente(EntidadSistema):
    """
    Clase encargada de representar los clientes
    registrados en Software FJ.
    """

    # Patrón de validación de correo electrónico
    PATRON_CORREO = re.compile(
        r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w{2,}$"
    )

    def __init__(self, nombre, correo, telefono):

        # Ejecuta constructor padre
        super().__init__()

        # Atributos encapsulados
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""

        # Uso de setters con validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ==================================================
    # GETTERS Y SETTERS
    # ==================================================

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        if not valor:
            raise ParametroFaltanteError(
                "El nombre es obligatorio."
            )

        valor = valor.strip()

        if len(valor) < 3:
            raise DatosInvalidosError(
                "El nombre debe tener mínimo 3 caracteres."
            )

        self.__nombre = valor.title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):

        if not valor:
            raise ParametroFaltanteError(
                "El correo es obligatorio."
            )

        valor = valor.strip().lower()

        if not self.PATRON_CORREO.match(valor):
            raise DatosInvalidosError(
                "Formato de correo inválido."
            )

        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):

        if not valor:
            raise ParametroFaltanteError(
                "El teléfono es obligatorio."
            )

        valor = str(valor).strip()

        if not valor.isdigit():
            raise DatosInvalidosError(
                "El teléfono debe contener solo números."
            )

        if len(valor) < 7 or len(valor) > 10:
            raise DatosInvalidosError(
                "El teléfono debe tener entre 7 y 10 dígitos."
            )

        self.__telefono = valor

    # ==================================================
    # MÉTODOS
    # ==================================================

    def resumen(self):
        """
        Retorna información resumida del cliente.
        """

        return (
            f"Cliente #{self.id} | "
            f"{self.nombre} | "
            f"{self.correo} | "
            f"{self.telefono}"
        )

    def __str__(self):
        """
        Representación textual del cliente.
        """
        return self.resumen()