# Lista enlazada
class Nodo:
  def __init__(self, dato=None, sgte=None):  # None = NULL
    self.dato = dato
    self.sgte = sgte


# Creamos la clase Lista


class Lista:

  def __init__(self):
    self.cbza = None

  # Método para agregar elementos en el frente de la lista enlazada

  def agregar_frente(self, dato):
    self.cbza = Nodo(dato=dato, sgte=self.cbza)

  # Método para verificar si la lista enlazada esta vacia

  def esta_vacia(self):
    return self.cbza is None

  # Método para agregar elementos al final de la lista enlazada
  def agregar_final(self, dato):
    if not self.cbza:
      self.cbza = Nodo(dato=dato)
      return

    actual = self.cbza
    while actual.sgte:
      actual = actual.sgte

    actual.sgte = Nodo(dato=dato)

  # Método para eliminar nodos
  def borrar_nodo(self, key):

    actual = self.cbza
    prev = None

    while actual and actual.dato != key:
      prev = actual
      actual = actual.sgte

    if prev is None:
      self.cbza = actual.sgte
    elif actual:
      prev.sgte = actual.sgte
      actual.sgte = None

  # Método para obtener el ultimo nodo

  def obtener_ultimo_nodo(self):
    temp = self.cbza
    while temp.sgte is not None:
      temp = temp.sgte
    return temp.dato

  # Método para imprimir la lista enlazada

  def print_list(self):

    nodo = self.cbza
    while nodo is not None:
      print(nodo.dato, end=" => ")
      nodo = nodo.sgte


# Pilas

class Pila:

  def __init__(self):
    self.superior = None

  def apilar(self, dato):
    print(f"Agregando {dato} en la cima de la pila")

    # Si no hay datos, agregamos el valor en el elemento superior y regresamos
    if self.superior is None:
      self.superior = Nodo(dato)
      return

    nuevo_nodo = Nodo(dato)
    nuevo_nodo.siguiente = self.superior
    self.superior = nuevo_nodo

  def desapilar(self):
    # Si no hay datos en el nodo superior, regresamos

    if self.superior is None:
      print("No hay ningún elemento en la pila para desapilar")
      return

    print(f"Desapilar {self.superior.dato}")
    self.superior = self.superior.siguiente

  def imprimir(self):
    print("Imprimiendo pila:")

    # Recorrer la pila e imprimir valores
    nodo_temporal = self.superior

    while nodo_temporal is not None:
      print(f"{nodo_temporal.dato}", end=",")
      nodo_temporal = nodo_temporal.siguiente

    print("")
