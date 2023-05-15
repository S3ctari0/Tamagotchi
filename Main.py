import tkinter as tk
from PIL import ImageTk, Image
from CamelCase import Tamagotchi,Perro,Gato,Conejo

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
client = MongoClient("mongodb+srv://Admin:T4dw3mMEaIuBZpro@tamagotchi.qdnxchy.mongodb.net/tamagochi?retryWrites=true&w=majority")
db = client.tamagotchi
collection = db.mascotas

list_tamagotchi = ["Conejo", "Perro", "Gato"]
animal_imagenes = {
    "Conejo": "Conejo.png",
    "Perro": "Perro.png",
    "Gato": "Gato.png"
}

def animal_root(animal=None):
    
    """
    Función que crea la ventana principal para interactuar con la mascota.

    Args:
        animal (dict): Diccionario que contiene la información de la mascota.

    """

    animal["name"] = nombre_mascota.get()
    nombre = animal["especie"]
    name = animal["name"]

    if nombre == "Perro":
        mascota = Perro(animal)
    elif nombre == "Conejo":
        mascota = Conejo(animal)
    elif nombre == "Gato":
        mascota = Gato(animal)

    if animal["is_load"]:
        mascota.cargar_mascota(animal)

    new_root = tk.Toplevel()
    new_root.geometry("500x600")
    new_root.configure(bg="purple4")
    new_root.title(nombre)
    label_name = tk.Label(new_root, text=f"Felicidades tienes una nueva mascota :D\n\n{name}",
                        font=("Calibri 14"), bg="purple4", fg="white")
    label_name.grid(row=0, column=0, columnspan=4, padx=90, pady=8)

    nombre_imagen = animal_imagenes[nombre]
    imagen = Image.open(nombre_imagen)
    imagen = imagen.resize((300, 300))
    imagen_tk = ImageTk.PhotoImage(imagen)
    etiqueta = tk.Label(new_root, image=imagen_tk)
    etiqueta.place(x=90, y=90)
    etiqueta.image = imagen_tk

    list_acciones = ["Alimentar", "Dormir", "Jugar", "Envejecer"]

    def salir():
        new_root.destroy()

    button_quit = tk.Button(new_root, text= "Salir", cursor="hand2", command=lambda: salir(), activebackground="SlateBlue3", bg="medium purple", fg="white")
    button_quit.place(x=450,y=550)

    def alimentar():
        mascota.feed()
        actualizar_estadisticas()

    def dormir():
        mascota.sleep()
        actualizar_estadisticas()

    def jugar():
        mascota.play()
        actualizar_estadisticas()

    def envejecer():
        mascota.age_up()
        actualizar_estadisticas()

    actions = [alimentar, dormir, jugar, envejecer]

    for i, accion in enumerate(list_acciones):
        button_action = tk.Button(new_root, text=accion, cursor="hand2", activebackground="SlateBlue3",
                                bg="medium purple", fg="white", command=actions[i])
        button_action.grid(row=3, column=i, padx=10, pady=350)

        label_stats = tk.Label(new_root, text="", font=("Calibri 14"), bg="purple4", fg="white")
        label_stats.place(x=70,y=500)

    def actualizar_estadisticas():
        stats = f"Hambre: {mascota.hunger} | Energía: {mascota.energy} | Felicidad: {mascota.happiness}"
        label_stats.config(text=stats)

        if mascota.is_dead():
            new_root.destroy()
            muerte = tk.Toplevel()
            muerte.config(bg="cornflower blue")
            muerte.geometry("250x100")
            text = tk.Label(muerte, text="Tu mascota ha muerto :c", font=("Calibri 14"),bg="cornflower blue")
            text.grid(row=0, column=0, padx=20, pady=8)
            button_quit = tk.Button(muerte, text= "Salir", cursor="hand2", command=lambda: root.destroy(), activebackground="light sky blue", bg="sky blue")
            button_quit.place(x=100,y=60)
            muerte.mainloop()

    actualizar_estadisticas()

    new_root.mainloop()

root = tk.Tk()
root.geometry("450x200")
root.title("Inicio")
root.configure(bg="cornflower blue")
text = tk.Label(root, text="Ingrese un nombre para su mascota", font=("Calibri 14"), bg="cornflower blue")
text.grid(row=0, column=0, columnspan=3, padx=20, pady=8)
nombre_mascota = tk.StringVar()
name = tk.Label(root, text="\nElija un animal para que sea su mascota", font=("Calibri 14"), bg="cornflower blue")
name.grid(row=4, column=0, columnspan=3, padx=20, pady=15)
name_tamagotchi = tk.Entry(root, textvariable=nombre_mascota, width=25, bg="sky blue")
name_tamagotchi.place(x="100", y="40")
mascota = {}

def cargar_mascota():
    mascota = collection.find_one({"name":nombre_mascota.get()})
    mascota["is_load"] = True
    animal_root(mascota)
    
cargar = tk.Button(root,text="Cargar",command= lambda: cargar_mascota(),cursor="hand2", activebackground="light sky blue", bg="sky blue")
cargar.place(x=380,y=45)
crear = tk.Button(root,text="Crear",cursor="hand2", command= lambda mascota=mascota:animal_root(mascota),activebackground="light sky blue", bg="sky blue")
crear.place(x=380,y=90)

def update_mascota(nombre):
    mascota["especie"] = nombre
    mascota["is_load"] = False

for i, nombre in enumerate(list_tamagotchi):
    boton = tk.Button(root, text=nombre, command=lambda nombre=nombre: update_mascota(nombre), cursor="hand2", activebackground="light sky blue", bg="sky blue")
    boton.grid(row=5, column=i, padx=10, pady=5)

root.mainloop()