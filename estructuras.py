# Lista enlazada
class Nodo:
  def __init__(self, dato=None, sgte=None):  # None = NULL
    self.dato = dato
    self.sgte = sgte

# Creamos la clase Lista


class Lista:

  def __init__(self): #DepartamentoEscuela
    self.cbza = None

  # Método para agregar elementos en el frente de la lista enlazada

  def agregar_frente(self, dato):
    self.cbza = Nodo(dato=dato, sgte=self.cbza)

  # Método para agregar elementos al final de la lista enlazada
  def agregar_final(self, dato):
    if not self.cbza:
      self.cbza = Nodo(dato=dato)
      return

    actual = self.cbza
    while actual.sgte:
      actual = actual.sgte

    actual.sgte = Nodo(dato=dato)

  # Método para imprimir la lista enlazada

  def retornar_datos(self):

    nodo = self.cbza
    datos = []

    while nodo is not None:
      datos.append(nodo.dato)
      nodo = nodo.sgte

    return datos

# Pilas


class Pila:

  def __init__(self):
    self.superior = None

  def apilar(self, dato):

    # Si no hay datos, agregamos el valor en el elemento superior y regresamos
    if self.superior is None:
      self.superior = Nodo(dato)
      return

    nuevo_nodo = Nodo(dato)
    nuevo_nodo.sgte = self.superior
    self.superior = nuevo_nodo

  def retornar_datos(self):

    # Recorrer la pila e imprimir valores
    nodo_temporal = self.superior
    datos = []

    while nodo_temporal is not None:
      datos.append(nodo_temporal.dato)
      nodo_temporal = nodo_temporal.sgte

    return datos
