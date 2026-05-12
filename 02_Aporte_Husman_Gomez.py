# APORTE 2 - Husman Gomez
# Sección: clase abstracta Servicio y servicios derivados.
# Este fragmento depende del Aporte 1, donde se encuentran imports, logs, excepciones y Cliente.

class Servicio(EntidadSistema, ABC):

    # Constructor común para todos los servicios.
    def __init__(self, nombre, precio_base, disponible=True):
        # Llama al constructor de EntidadSistema.
        super().__init__()

        # Valida que el servicio tenga nombre.
        if not nombre:
            raise ParametroFaltanteError("El servicio necesita un nombre.")

        # Valida que el precio sea positivo.
        if precio_base <= 0:
            raise DatosInvalidosError("El precio base debe ser mayor que cero.")

        # Guarda datos comunes del servicio.
        self.nombre = nombre
        self.precio_base = float(precio_base)
        self.disponible = disponible

    # Método abstracto para calcular costo.
    # Cada servicio hijo lo implementa de forma diferente.
    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    # Método abstracto para describir el servicio.
    @abstractmethod
    def describir(self):
        pass

    # Método abstracto para validar parámetros propios del servicio.
    @abstractmethod
    def validar_parametros(self):
        pass

    # Método sobrecargado base.
    # Si recibe un tipo no soportado, lanza error.
    @singledispatchmethod
    def calcular_total(self, valor):
        raise CalculoInconsistenteError("Tipo de dato no soportado para calcular total.")

    # Primera variante sobrecargada: recibe duración como entero.
    @calcular_total.register
    def _(self, duracion: int):
        return self.calcular_costo(duracion)

    # Segunda variante sobrecargada: recibe tupla con duración, impuesto y descuento.
    @calcular_total.register
    def _(self, datos: tuple):
        try:
            # Se intenta desempaquetar la tupla.
            duracion, impuesto, descuento = datos

            # Se calcula el subtotal usando polimorfismo.
            subtotal = self.calcular_costo(duracion)

            # Se calcula el total aplicando impuesto y descuento.
            total = subtotal + (subtotal * impuesto) - descuento

            # El total no puede ser negativo.
            if total < 0:
                raise CalculoInconsistenteError("El total no puede ser negativo.")

            # Se retorna el total redondeado.
            return round(total, 2)

        # Captura error si la tupla no tiene tres elementos.
        except ValueError as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise CalculoInconsistenteError(
                "La tupla debe tener duración, impuesto y descuento."
            ) from error

    # Resumen general de cualquier servicio.
    def resumen(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio #{self.id}: {self.nombre} | Base: ${self.precio_base:.2f} | {estado}"

    # Representación textual del servicio.
    def __str__(self):
        return self.resumen()


# ======================================================
# 6. SERVICIOS DERIVADOS CON POLIMORFISMO
# ======================================================

# ServicioSpa hereda de Servicio.
class ServicioSpa(Servicio):

    # Constructor específico para spa.
    def __init__(self, aromaterapia=True):
        # Llama al constructor de Servicio con nombre y precio base.
        super().__init__("Spa Relajante", 60000)

        # Guarda si incluye aromaterapia.
        self.aromaterapia = aromaterapia

        # Valida el parámetro específico.
        self.validar_parametros()

    # Sobrescribe calcular_costo.
    def calcular_costo(self, duracion):
        # Valida duración positiva.
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración del spa debe ser positiva.")

        # Si hay aromaterapia, se cobra extra.
        extra = 15000 if self.aromaterapia else 0

        # Retorna costo total.
        return round((self.precio_base * duracion) + extra, 2)

    # Sobrescribe describir.
    def describir(self):
        return "Servicio de spa con opción de aromaterapia."

    # Sobrescribe validar_parametros.
    def validar_parametros(self):
        # Aromaterapia debe ser booleano.
        if not isinstance(self.aromaterapia, bool):
            raise DatosInvalidosError("Aromaterapia debe ser True o False.")


# ServicioEntrenamiento hereda de Servicio.
class ServicioEntrenamiento(Servicio):

    # Constructor específico para entrenamiento.
    def __init__(self, nivel):
        # Define nombre y precio base.
        super().__init__("Entrenamiento Personal", 45000)

        # Guarda nivel.
        self.nivel = nivel

        # Valida nivel.
        self.validar_parametros()

    # Calcula costo según el nivel.
    def calcular_costo(self, duracion):
        # Valida duración.
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración del entrenamiento debe ser positiva.")

        # Diccionario de multiplicadores por nivel.
        multiplicador = {
            "basico": 1,
            "intermedio": 1.25,
            "avanzado": 1.5
        }[self.nivel]

        # Retorna costo total.
        return round(self.precio_base * duracion * multiplicador, 2)

    # Describe el servicio.
    def describir(self):
        return f"Entrenamiento físico de nivel {self.nivel}."

    # Valida el nivel recibido.
    def validar_parametros(self):
        if self.nivel not in ["basico", "intermedio", "avanzado"]:
            raise DatosInvalidosError("Nivel inválido. Use: basico, intermedio o avanzado.")


# ServicioConsultoria hereda de Servicio.
class ServicioConsultoria(Servicio):

    # Constructor específico para consultoría.
    def __init__(self, modalidad):
        # Define nombre y precio base.
        super().__init__("Consultoría Profesional", 90000)

        # Guarda modalidad.
        self.modalidad = modalidad

        # Valida modalidad.
        self.validar_parametros()

    # Calcula costo según duración y modalidad.
    def calcular_costo(self, duracion):
        # Valida duración.
        if duracion <= 0:
            raise CalculoInconsistenteError("La duración de la consultoría debe ser positiva.")

        # Si es presencial, se cobra recargo.
        recargo = 20000 if self.modalidad == "presencial" else 0

        # Retorna total.
        return round((self.precio_base * duracion) + recargo, 2)

    # Describe el servicio.
    def describir(self):
        return f"Consultoría en modalidad {self.modalidad}."

    # Valida modalidad.
    def validar_parametros(self):
        if self.modalidad not in ["virtual", "presencial"]:
            raise DatosInvalidosError("Modalidad inválida. Use: virtual o presencial.")


