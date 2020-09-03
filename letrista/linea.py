import re


class Linea:
    """
    Esta clase es utilizada para representar una línea del borrador (es decir,
    una línea que pertenece a la letra, no instrucciones especiales ni ayudas
    durante la edición).

    Una línea del borrador puede contener los siguientes símbolos:
    - Una letra inicial para el esquema de rima
    - Un guión en la segunda posición para marcar como eliminada.
    - El conteo silábico en posiciones 3 y 4
    - El resto del texto del carácter 5 en adelante.
    - Sombreritos (^) para señalar una rima fuera del final de línea.
    - Además puede ser una de las siguientes categorías:
          + Línea de instrucción de sección.
          + Espacio en blanco entre secciones.
          + Línea de fin de letra.

    Además, contiene las siguientes propiedades adicionales:
    - cantidadDePalabras
    """

    # Constantes para tipo de línea.
    TIPO_SILABAS = 1     # "X ## letra" -- Incluye el conteo de sílabas
    TIPO_RIMA = 2        # "X letra"    -- Incluye el tipo de rima
    TIPO_SALTO = 3       # "\n"         -- Es un salto de línea
    TIPO_TEXTO = 4       # "letra"      -- Es solo el texto de la letra
    TIPO_INSTRUCCION = 5 # "["          -- Línea que empieza con corchetes.

    def __init__(self, texto):
        """Establece el texto completo, con indicadores, de la línea."""
        self._texto_original = texto

    @property
    def texto(self):
        """
        Elimina, en primera instancia, los caracteres relativos al conteo
        silábico y al esquema de rima.
        Además, elimina las anotaciones sobre rima intera.
        """
        if self.tipo == self.TIPO_SILABAS:
            self._texto = self._texto_original[5:]
        elif self.tipo == self.TIPO_RIMA:
            self._texto = self._texto_original[2:]
        else:
            self._texto = self._texto_original.strip()

        # Eliminar notas de rima interna mediante expresiones regulares.
        self._texto = re.sub('\^[0-9]+', '', self._texto)

        return self._texto

    @property
    def texto_con_rima_y_silabas(self):
        tipo = self.tipo

        # Si la línea ya tiene conteo silábico, no es necesario hacer nada.
        if tipo == self.TIPO_SILABAS:
            self._texto_con_rima_silabas = self._texto_original
        # Si es instrucción o salto de línea, tampoco hacemos nada.
        elif tipo == self.TIPO_SALTO or tipo == self.TIPO_INSTRUCCION:
            self._texto_con_rima_silabas = self._texto_original
        # Si solamente tiene la rima, agregamos el conteo silábico
        elif tipo == self.TIPO_RIMA:
            self._texto_con_rima_silabas = self._texto_original[0] + " 00 " + self._texto_original[2:]
        # Si no tiene ninguna de las anteriores, agregamos rima y sílabas.
        else:
            self._texto_con_rima_silabas = "X 00 " + self._texto_original

        return self._texto_con_rima_silabas

    @property
    def tipo(self):
        """
        Define el tipo de línea entre cuatro posibles, cuyo estilo está
        definido en las constantes de la clase.
        """
        if self.__tieneConteoSilabico():
            self._tipo = self.TIPO_SILABAS
        elif self.__tieneEsquemaDeRima():
            self._tipo = self.TIPO_RIMA
        elif self.__esSaltoDeLinea():
            self._tipo = self.TIPO_SALTO
        elif self.__esInstruccion():
            self._tipo = self.TIPO_INSTRUCCION
        else:
            self._tipo = self.TIPO_TEXTO

        return self._tipo

    @property
    def esquema_de_rima(self):
        """
        Regresa el esquema de rima en base al tipo de línea (solo las líneas
        de tipo TIPO_RIMA y TIPO_SILABAS lo tienen disponible).
        Si no tiene esquema, se asigna el esquema indefinido ("X")
        """
        # Esquema predefinido, si no hay alguno.
        self._esquema_de_rima = 'X'
        # Obtener el esquema dependiendo del tipo de línea.
        if self.tipo in [self.TIPO_SILABAS, self.TIPO_RIMA]:
            self._esquema_de_rima = self._texto_original[0]

        return self._esquema_de_rima

    @property
    def silabas(self):
        """
        Regresa el texto correspondiente a la cantidad de sílabas como texto.
        Aquí no se utilzia la cnatidad como dígito, dado el padding, dado que
        es una cuestión más estilística que operacional.
        Por lo mismo, en caso de no tener conteo silábico, se usa la cadena "__"
        para marcar un número indefinido.
        """
        self._silabas = "__"
        if self.tipo == self.TIPO_SILABAS:
            this._silabas = self._texto_original[2:3]

        return self._silabas

    @property
    def cantidad_de_palabras(self):
        tipo = self.tipo

        if tipo in [self.TIPO_SILABAS, self.TIPO_RIMA, self.TIPO_TEXTO]:
            self._cantidad_de_palabras = len(self.texto.split())
        else:
            # Tipo debe ser salto o instrucción, así que regresamos 0
            self._cantidad_de_palabras = 0

        return self._cantidad_de_palabras

    def __tieneConteoSilabico(self):
        """
        Determina si una línea contiene el conteo silábico
        en las posiciones 3 y 4. Es decir, si la línea cumple con:
        - X 00 cadena    <- cumple
        - X __ cadena    <- cumple
        - Una oración    <- no cumple
        """
        # Si hay menos de cuatro caracteres, no hay conteo silábico.
        if len(self._texto_original) < 4:
            return False

        # Si tiene el placeholder "__" o en esas posiciones hay dígitos, sí.
        if self._texto_original[2:3] == "__" or self._texto_original[2:3].isdigit():
            return True

        # Si llegamos hasta acá, no hay conteo silábico ni placeholder.
        return False

    def __tieneEsquemaDeRima(self):
        """
        Determina si una línea contiene el esquema de rima en la primer posición
        basado en las primeras dos posiciones. La condición es una letra inicial seguida
        de un espacio, como se muestra:
        - X 00 cadena    <- cumple
        - A __ cadena    <- cumple
        - Hola, mundo    <- no cumple
        """
        # Necesitamos al menos dos caracteres para esta comprobación.
        if len(self._texto_original) < 2:
            return False

        # Si el segundo dígito es espacio, y el primero una letra, tiene esquema.
        if self._texto_original[1] == " " and self._texto_original[0].isalpha():
            return True

        # No hay esquema.
        return False

    def __esSaltoDeLinea(self):
        """
        Determina si una línea contiene solo espacios y nada de texto.
        """
        if self._texto_original.strip() == '':
            return True

        return False

    def __esInstruccion(self):
        """
        Determina si una línea es instrucción
        """
        if len(self._texto_original) < 1:
            return False

        if self._texto_original[0] == '[':
            return True

        return False