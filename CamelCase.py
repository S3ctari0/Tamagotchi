from abc import ABC, abstractmethod
import random

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Establecer conexión con la base de datos MongoDB
client = MongoClient("mongodb+srv://Admin:T4dw3mMEaIuBZpro@tamagotchi.qdnxchy.mongodb.net/tamagochi?retryWrites=true&w=majority")
db = client.tamagotchi
collection = db.mascotas

class Tamagotchi(ABC):
    @abstractmethod
    def __init__(self, mascota):
        """
        Constructor de la clase Tamagotchi.

        Args:
            mascota (dict): Diccionario con los datos de la mascota cargada desde la base de datos.
        """
        self.is_load = mascota["is_load"]
        self.name = mascota["name"]
        self.hunger = 50
        self.energy = 50
        self.happiness = 50

    def feed(self):
        """
        Alimenta al Tamagotchi, disminuyendo el nivel de hambre y aumentando la energía y felicidad.
        """
        self.hunger -= 20
        self.energy += 10
        self.happiness += 5
        self.guardar_mascota()

    def sleep(self):
        """
        Hace que el Tamagotchi duerma, aumentando el nivel de hambre y la energía.
        """
        self.hunger += 15
        self.energy += 40
        self.guardar_mascota()

    def play(self):
        """
        Hace que el Tamagotchi juegue, aumentando el nivel de hambre, disminuyendo la energía y aumentando la felicidad.
        """
        self.hunger += 10
        self.energy -= 10
        self.happiness += 20
        self.guardar_mascota()
    
    def guardar_mascota(self):
        """
        Guarda los datos del Tamagotchi en la base de datos.
        """
        mascota = {"name": self.name, "hunger": self.hunger, "energy": self.energy, "age": self.age, "happiness": self.happiness, "specie": self.specie}
        filter = {"name": self.name}

        if self.is_load:
            # Si la mascota ya está cargada, se reemplaza el documento en la base de datos
            collection.find_one_and_replace(filter, mascota)
        else:
            # Si es una nueva mascota, se inserta un nuevo documento en la base de datos
            collection.insert_one(mascota)
            self.is_load = True

    def cargar_mascota(self, mascota):
        """
        Carga los datos de una mascota desde la base de datos.

        Args:
            mascota (dict): Diccionario con los datos de la mascota.
        """
        self.name = mascota["name"]
        self.hunger = mascota["hunger"]
        self.energy = mascota["energy"]
        self.age = mascota["age"]
        self.happiness = mascota["happiness"]

    @abstractmethod
    def is_dead(self):
        """
        Verifica si el Tamagotchi ha muerto.

        Returns:
            bool: True si el Tamagotchi ha muerto, False en caso contrario.
        """
        pass

def is_happy(self):
    """
        Verifica si el Tamagotchi está feliz.    
    
        Return:
            bool: True si el Tamagotchi está feliz, False en caso contrario.
        """
    return self.happiness >= 50

class Perro(Tamagotchi):
    def __init__(self, name):
        """
        Constructor de la clase Perro.

        Args:
            name (str): Nombre del perro.
        """
        super().__init__(name)
        self.age = 0
        self.specie = "Perro"

    def age_up(self):
        """
        Incrementa la edad del perro y ajusta los niveles de hambre, energía y felicidad de forma aleatoria.
        """
        self.age += 1
        self.hunger += 10
        self.energy -= 10
        self.happiness += random.randint(0, 20)
        self.guardar_mascota()

    def is_dead(self):
        """
        Verifica si el perro ha muerto.

        Returns:
            bool: True si el perro ha muerto, False en caso contrario.
        """
        return self.hunger >= 100 or self.energy <= 0 or self.age >= 12

class Conejo(Tamagotchi):
    def __init__(self, name):
        """
        Constructor de la clase Conejo.

        Args:
            name (str): Nombre del conejo.
        """
        super().__init__(name)
        self.age = 0
        self.specie = "Conejo"

    def age_up(self):
        """
        Incrementa la edad del conejo y ajusta los niveles de hambre, energía y felicidad de forma aleatoria.
        """
        self.age += 1
        self.hunger += 10
        self.energy -= 10
        self.happiness += random.randint(0, 20)
        self.guardar_mascota()
    
    def is_dead(self):
        """
        Verifica si el conejo ha muerto.

        Returns:
            bool: True si el conejo ha muerto, False en caso contrario.
        """
        return self.energy <= 0 or self.hunger >= 100 or self.age >= 9

class Gato(Tamagotchi):
    def __init__(self, name):
        """
        Constructor de la clase Gato.

        Args:
            name (str): Nombre del gato.
        """
        super().__init__(name)
        self.age = 0
        self.specie = "Gato"

    def age_up(self):
        """
        Incrementa la edad del gato y ajusta los niveles de hambre, energía y felicidad de forma aleatoria.
        """
        self.age += 1
        self.hunger += 10
        self.energy -= 10
        self.happiness += random.randint(0, 20)
        self.guardar_mascota()

    def is_dead(self):
        """
        Verifica si el gato ha muerto.

        Returns:
            bool: True si el gato ha muerto, False en caso contrario.
        """
        return self.hunger >= 100 or self.energy <= 0 or self.age >= 14