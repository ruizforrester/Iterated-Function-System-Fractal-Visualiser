#Imports

import tkinter as tk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
import os
import numpy as np
from algoritmos import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import shutil

#Init

root = tk.Tk() # Crear la ventana principal
#Damos nombre a la ventana
root.title("Ilustrador de Sistemas de Funciones Iteradas")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
listaSFI = [] # Lista de SFIs
probManual = tk.BooleanVar()
figuraInicial = tk.StringVar()
aristaInicial = tk.DoubleVar()
rotacionInicial = tk.DoubleVar()
coordenadaXInicial = tk.DoubleVar()
coordenadaYInicial = tk.DoubleVar()
#Leemos del archivo cfg
try:
    with open("config.cfg", "r") as f:
        lineas = f.readlines()
        ITERACIONES_DETERMINISTA = int(lineas[1].split("=")[1])
        ITERACIONES_ALEATORIO = int(lineas[2].split("=")[1])
        TAMANHO_HISTORIAL = int(lineas[3].split("=")[1])
        if lineas[4].split("=")[1].strip() == "True":
            probManual.set(True)
        else:
            probManual.set(False)
        COLOR0 = lineas[5].split("=")[1].strip()    
        COLOR1 = lineas[6].split("=")[1].strip()
        COLOR2 = lineas[7].split("=")[1].strip()
        COLOR3 = lineas[8].split("=")[1].strip()
        COLOR4 = lineas[9].split("=")[1].strip()
        figuraInicial.set(lineas[10].split("=")[1].strip())
        aristaInicial.set(float(lineas[11].split("=")[1].strip()))
        rotacionInicial.set(float(lineas[12].split("=")[1].strip()))
        coordenadaXInicial.set(float(lineas[13].split("=")[1].strip()))
        coordenadaYInicial.set(float(lineas[14].split("=")[1].strip()))
        
        
except:
    ITERACIONES_DETERMINISTA = 5 # Iteraciones para el algoritmo determinista
    ITERACIONES_ALEATORIO = 5000 # Iteraciones para el algoritmo aleatorio
    TAMANHO_HISTORIAL = 10 # Tamaño del historial de SFIs
    COLOR0 = '#00BFBF' #fractales
    COLOR1 = "#263D42" #ventana
    COLOR2 = "#262626" #frames
    COLOR3 = "cyan"  #botones
    COLOR4 = "white" #texto
    probManual.set(False)
    figuraInicial.set("Triangulo") 
    aristaInicial.set(1.0)
    rotacionInicial.set(0.0)
    coordenadaXInicial.set(0.0)
    coordenadaYInicial.set(0.0)
    with open("config.cfg", "w") as f:
        f.write("//Este es un archivo de configuración. Su formato es importante, por lo que no se debe modificar, excepto los valores.\n")
        f.write("ITERACIONES_DETERMINISTA="+str(ITERACIONES_DETERMINISTA)+"\n")
        f.write("ITERACIONES_ALEATORIO="+str(ITERACIONES_ALEATORIO)+"\n")
        f.write("TAMANHO_HISTORIAL="+str(TAMANHO_HISTORIAL)+"\n")
        f.write("PROBABILIDADES_MANUALES="+str(probManual.get())+"\n")
        f.write("COLOR0="+COLOR0+"\n")
        f.write("COLOR1="+COLOR1+"\n")
        f.write("COLOR2="+COLOR2+"\n")
        f.write("COLOR3="+COLOR3+"\n")
        f.write("COLOR4="+COLOR4+"\n")
        f.write("FIGURA_INICIAL="+figuraInicial.get()+"\n")
        f.write("ARISTA_INICIAL="+str(aristaInicial.get())+"\n")
        f.write("ROTACION_INICIAL="+str(rotacionInicial.get())+"\n")
        f.write("COORDENADA_X_INICIAL="+str(coordenadaXInicial.get())+"\n")
        f.write("COORDENADA_Y_INICIAL="+str(coordenadaYInicial.get())+"\n")

np.set_printoptions(linewidth=np.inf)

#Ventana Opciones
def abrirMenuOpciones():
    global probManual
    global figuraInicial
    global aristaInicial
    global rotacionInicial
    #Abrimos una nueva ventana
    ventanaOpciones = tk.Toplevel(root)
    ventanaOpciones.lift()
    #Le damos un titulo y un tamaño
    ventanaOpciones.title("Opciones")
    
    window_width = 525
    window_height = 250
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    ventanaOpciones.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    #Cambiamos el color del fondo
    ventanaOpciones.config(bg=COLOR1)
    #Creamos un campo de texto para introducir el numero de resultados que se almacenan en el historial
    frameTamanhoHistorial = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameTamanhoHistorial.pack(padx=10, pady=(3, 0))
    labelTamanhoHistorial = tk.Label(frameTamanhoHistorial, text="Tamaño del historial: ", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelTamanhoHistorial.pack(side=tk.LEFT)
    numeroTamanhoHistorial = tk.Entry(frameTamanhoHistorial, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=30)
    numeroTamanhoHistorial.insert(0, str(TAMANHO_HISTORIAL))
    numeroTamanhoHistorial.pack(side=tk.RIGHT, fill="x")

    #Creamos una linea para separar el resto de opciones
    frameLinea = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameLinea.pack(padx=10, pady=(3, 0))
    canvas = tk.Canvas(frameLinea, height=1, width=300, bg=COLOR1, highlightthickness=0)    
    canvas.create_line(0, 0, 300, 0, fill=COLOR4)
    canvas.pack(padx=10, pady=(3, 0))

    # Creamos un dropdown para escoger la figura inicial
    frameFiguraInicial = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameFiguraInicial.pack(padx=10, pady=(3, 0))
    labelFiguraInicial = tk.Label(frameFiguraInicial, text="Figura inicial para el Algoritmo Determinista: ", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelFiguraInicial.pack(side=tk.LEFT)
    dropdownFiguraInicial = tk.OptionMenu(frameFiguraInicial, figuraInicial, "Triangulo", "Cuadrado", "Pentagono", "Hexagono")
    dropdownFiguraInicial.config(bg=COLOR2, fg=COLOR4, activebackground=COLOR2, activeforeground=COLOR4, highlightbackground=COLOR1,font=("Arial", 12))
    dropdownFiguraInicial.pack(side=tk.RIGHT, fill="x") 
    # Creamos un campo de texto para escoger el tamanho del lado de la figura inicial
    frameTamanhoFiguraInicial = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameTamanhoFiguraInicial.pack(padx=10, pady=(3, 0))
    labelTamanhoFiguraInicial = tk.Label(frameTamanhoFiguraInicial, text="Tamaño de su arista: ", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelTamanhoFiguraInicial.pack(side=tk.LEFT)
    tamanhoFiguraInicial = tk.Entry(frameTamanhoFiguraInicial, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=30)
    tamanhoFiguraInicial.insert(0, str(aristaInicial.get()))
    tamanhoFiguraInicial.pack(side=tk.RIGHT, fill="x")
    # Creamos un campo de texto para escoger la rotacion de la figura inicial
    frameRotacionFiguraInicial = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameRotacionFiguraInicial.pack(padx=10, pady=(3, 0))
    labelRotacionFiguraInicial = tk.Label(frameRotacionFiguraInicial, text="Rotación de la figura (en grados): ", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelRotacionFiguraInicial.pack(side=tk.LEFT)
    rotacionFiguraInicial = tk.Entry(frameRotacionFiguraInicial, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=30)
    rotacionFiguraInicial.insert(0, str(rotacionInicial.get()))
    rotacionFiguraInicial.pack(side=tk.RIGHT, fill="x")
    # Creamos un campo de texto para escoger el punto origen de la figura inicial con sus dos coordenadas
    frameOrigenFiguraInicial = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameOrigenFiguraInicial.pack(padx=10, pady=(3, 0))
    labelOrigenFiguraInicial = tk.Label(frameOrigenFiguraInicial, text="Coordenadas iniciales de la figura: ", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelOrigenFiguraInicial.pack(side=tk.LEFT)
    labelXFiguraInicial = tk.Label(frameOrigenFiguraInicial, text="x =", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelXFiguraInicial.pack(side=tk.LEFT)
    coordenadaXFiguraInicial = tk.Entry(frameOrigenFiguraInicial, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=15)
    coordenadaXFiguraInicial.insert(0, str(coordenadaXInicial.get()))
    coordenadaXFiguraInicial.pack(side=tk.LEFT, fill="x")
    labelYFiguraInicial = tk.Label(frameOrigenFiguraInicial, text="y =", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelYFiguraInicial.pack(side=tk.LEFT)
    coordenadaYFiguraInicial = tk.Entry(frameOrigenFiguraInicial, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=15)
    coordenadaYFiguraInicial.insert(0, str(coordenadaYInicial.get()))
    coordenadaYFiguraInicial.pack(side=tk.LEFT, fill="x")

    #Creamos una linea para separar el resto de opciones
    frameLinea = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameLinea.pack(padx=10, pady=(3, 0))
    canvas = tk.Canvas(frameLinea, height=1, width=300, bg=COLOR1, highlightthickness=0)    
    canvas.create_line(0, 0, 300, 0, fill=COLOR4)
    canvas.pack(padx=10, pady=(3, 0), fill="x")
    #Creamos un boton para indicar si calcular manualmente las probabilidades o no
    frameManual = tk.Frame(ventanaOpciones, bg=COLOR1)
    frameManual.pack(padx=10, pady=(3, 0))
    labelManual = tk.Label(frameManual, text="Insertar probabilidades del Algoritmo Aleatorio manualmente", bg=COLOR1, fg=COLOR4, font=("Arial", 12)) 
    labelManual.pack(side=tk.LEFT)
    c1 = tk.Checkbutton(frameManual, text='', variable=probManual, onvalue=1, offvalue=0,
                        bg=COLOR1, fg=COLOR4, activebackground=COLOR1, activeforeground=COLOR4, selectcolor=COLOR1, font=("Arial", 12))
    c1.pack(side=tk.LEFT)
    #Hacemos que al clickar el texto se active o desactive el boton
    labelManual.bind("<Button-1>", lambda e: c1.invoke())

    #Creamos un boton para guardar los cambios
    botonGuardar = tk.Button(ventanaOpciones, text="Guardar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, 
                             command=lambda: guardarCambios(ventanaOpciones, numeroTamanhoHistorial, tamanhoFiguraInicial, 
                            rotacionFiguraInicial, coordenadaXFiguraInicial, coordenadaYFiguraInicial), font=("Arial", 12))
    botonGuardar.pack(side=tk.BOTTOM, pady=10)

def guardarCambios(ventanaOpciones, numeroTamanhoHistorial, tamanhoFiguraInicial, rotacionFiguraInicial, coordenadaXFiguraInicial, coordenadaYFiguraInicial):
    global TAMANHO_HISTORIAL
    global probManual
    global aristaInicial
    global rotacionInicial
    global coordenadaXInicial
    global coordenadaYInicial
    
    #Guardamos los cambios
    #Si numeroTamanhoHistorial.get() es distinto de cero hacemos el cambio
    if numeroTamanhoHistorial.get() != "":
        TAMANHO_HISTORIAL = int(numeroTamanhoHistorial.get())
    #Si aristaInicial.get() es distinto de cero hacemos el cambio
    if tamanhoFiguraInicial.get() != "":
        aristaInicial.set(float(tamanhoFiguraInicial.get()))
    #Si rotacionInicial.get() es distinto de cero hacemos el cambio
    if rotacionFiguraInicial.get() != "":
        rotacionInicial.set(float(rotacionFiguraInicial.get()))
    #Si coordenadaXInicial.get() es distinto de cero hacemos el cambio
    if coordenadaXFiguraInicial.get() != "":
        coordenadaXInicial.set(float(coordenadaXFiguraInicial.get()))
    #Si coordenadaYInicial.get() es distinto de cero hacemos el cambio
    if coordenadaYFiguraInicial.get() != "":
        coordenadaYInicial.set(float(coordenadaYFiguraInicial.get()))
    #Guardamos los cambios en el archivo cfg
    with open("config.cfg", "w") as f:
        f.write("//Este es un archivo de configuración. Su formato es importante, por lo que no se debe modificar, excepto los valores.\n")
        f.write("ITERACIONES_DETERMINISTA="+str(ITERACIONES_DETERMINISTA)+"\n")
        f.write("ITERACIONES_ALEATORIO="+str(ITERACIONES_ALEATORIO)+"\n")
        f.write("TAMANHO_HISTORIAL="+str(TAMANHO_HISTORIAL)+"\n")
        f.write("PROBABILIDADES_MANUALES="+str(probManual.get())+"\n")
        f.write("COLOR0="+COLOR0+"\n")
        f.write("COLOR1="+COLOR1+"\n")
        f.write("COLOR2="+COLOR2+"\n")
        f.write("COLOR3="+COLOR3+"\n")
        f.write("COLOR4="+COLOR4+"\n")
        f.write("FIGURA_INICIAL="+figuraInicial.get()+"\n")
        f.write("ARISTA_INICIAL="+str(aristaInicial.get())+"\n")
        f.write("ROTACION_INICIAL="+str(rotacionInicial.get())+"\n")
        f.write("COORDENADA_X_INICIAL="+str(coordenadaXInicial.get())+"\n")
        f.write("COORDENADA_Y_INICIAL="+str(coordenadaYInicial.get())+"\n")

    ventanaOpciones.destroy()
    messagebox.showinfo("Información", "Cambios guardados correctamente")

#Ventana Favoritos
def abrirFavoritos():
    def displaySFIFavoritos(frameLabels):
        with open("favoritos.txt", "r") as f:
            lines = f.readlines()
            #Creamos un label para la linea actual
            if len(lines) == 0:
                return 0
            numLineas = len(lines)
            linea = (lines[abrirFavoritos.lineaActual])
            lineaDividida = linea.split(']')
            primeraDivision = lineaDividida[0].split('[')
            iters = primeraDivision[0][2:]
            match linea[0]:
                case "D":
                    titulo = "Favorito "+str(numLineas-abrirFavoritos.lineaActual)
                    sfi = "Algoritmo Determinista, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = ""
                case "A":
                    titulo = "Favorito "+str(numLineas-abrirFavoritos.lineaActual)
                    sfi = "Algoritmo Aleatorio, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = ""
                case "P":
                    titulo = "Favorito "+str(numLineas-abrirFavoritos.lineaActual)
                    sfi = "Algoritmo Aleatorio, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = "Probabilidades: " + str(np.fromstring(lineaDividida[1][2:], sep= ' '))
                case "_":
                    print("Error! En el formato del archivo")
            if lineaDividida[-1] != "\n":
                rutaYTitulo = lineaDividida[-1][:-1].split(r" %%% ")
                ruta = rutaYTitulo[0]
                if len(rutaYTitulo) > 1:
                    titulo = rutaYTitulo[1]

            labelLineaActual = tk.Label(frameLabels, text=titulo, bg=COLOR1, fg=COLOR4, font=("Courier", 14, "bold", "underline"))
            labelLineaActual.pack(side=tk.TOP, fill="x", padx=10, pady=8)
            
            labelSFIActual = tk.Label(frameLabels, text=sfi+"\n"+psfi, bg=COLOR1, fg=COLOR4, font=("Arial", 12))
            labelSFIActual.pack(side=tk.TOP, fill="x")
            return len(lines)


    #Comprobamos si history.txt existe y si no existe lo creamos
    if not os.path.exists(r"favoritos.txt"):
        with open("favoritos.txt", "w") as f:
            print("Creando Archivo de Favoritos")
            pass
    with open("favoritos.txt", "r") as f: 
        numLineas = len(f.readlines())
        abrirFavoritos.lineaActual = numLineas-1
    if numLineas == 0:
        messagebox.showinfo("Favoritos", "¡No hay favoritos guardados! Abre el Historial de resultados y añade alguno a Favoritos")
    else:
        #Abrimos una nueva ventana
        ventanaFavoritos = tk.Toplevel(root)
        #Le damos un titulo y un tamaño
        ventanaFavoritos.title("Favoritos")
        
        window_width = 550
        window_height = 340
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        ventanaFavoritos.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        #Cambiamos el color del fondo
        ventanaFavoritos.config(bg=COLOR1)
        ventanaFavoritos.lift()

        #Creamos botones para movernos entre SFIs:        
        frameBotones = tk.Frame(ventanaFavoritos, bg=COLOR1)
        frameBotones.pack(side=tk.BOTTOM)
        botonAnterior = tk.Button(frameBotones, text="Anterior", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: anteriorSFI(), font=("Montserrat", 12))
        botonAnterior.pack(side=tk.LEFT, padx=10, pady=10)
        botonSiguiente = tk.Button(frameBotones, text="Siguiente", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: siguienteSFI(), font=("Montserrat", 12), state=tk.DISABLED)
        botonSiguiente.pack(side=tk.LEFT, padx=10, pady=10)
        botonRenombrar = tk.Button(frameBotones, text="Renombrar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: renombrarFavorito(), font=("Montserrat", 12))
        botonRenombrar.pack(side=tk.LEFT, padx=10, pady=10)
        botonMostrar = tk.Button(frameBotones, text="Mostrar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: mostrarSFI(), font=("Montserrat", 12))
        botonMostrar.pack(side=tk.LEFT, padx=10, pady=10)
        botonEliminar = tk.Button(frameBotones, text="Eliminar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: eliminarFavorito(), font=("Montserrat", 12))
        botonEliminar.pack(side=tk.LEFT, padx=10, pady=10)
        #Creamos un frame para los labels
        frameLabels = tk.Frame(ventanaFavoritos, bg=COLOR1)
        frameLabels.pack(side=tk.TOP, fill="x")
        numFavoritos = displaySFIFavoritos(frameLabels)
        if numFavoritos == 1:
            botonAnterior.config(state=tk.DISABLED)


    def renombrarFavorito():
        
        def guardarCambiosRenombrar(ventanaRenombrar, nombreFavorito):
            nombre = nombreFavorito.get()
            with open("favoritos.txt", "r") as f1:
                lines = f1.readlines()
            with open("favoritos.txt", "w") as f2:
                for indice, linea in enumerate(lines):
                    if indice != abrirFavoritos.lineaActual:
                        f2.write(linea)
                    else:
                        if nombre != "":
                            f2.write(linea[:-1])
                            f2.write(r" %%% "+nombre+"\n")
                            messagebox.showinfo("Información", "Cambios guardados correctamente", parent=ventanaFavoritos)
                        else:
                            messagebox.showinfo("Información", "No se ha introducido ningún nombre", parent=ventanaFavoritos)
            ventanaRenombrar.destroy()
            # Destruimos y volvemos a mostrar el texto
            frameLabels = ventanaFavoritos.winfo_children()[1]
            labelLineaActual = frameLabels.winfo_children()[0]
            labelSFIActual = frameLabels.winfo_children()[1]
            labelLineaActual.destroy()
            labelSFIActual.destroy()

            displaySFIFavoritos(frameLabels)



        #Abrimos una nueva ventana
        ventanaRenombrar = tk.Toplevel(ventanaFavoritos)
        ventanaRenombrar.title("Renombrar Favorito")
        ventanaRenombrar.config(bg=COLOR1)
        ventanaRenombrar.geometry(f"+575+475")
        ventanaRenombrar.lift()

        #Creamos un campo de texto para introducir el nombre del favorito
        frameNombreFavorito = tk.Frame(ventanaRenombrar, bg=COLOR1)
        frameNombreFavorito.pack(padx=10, pady=(3, 0))
        labelNombreFavorito = tk.Label(frameNombreFavorito, text="Nombre del favorito: ", bg=COLOR1, fg=COLOR4, font=("Courier", 12))
        labelNombreFavorito.pack(side=tk.LEFT)
        nombreFavorito = tk.Entry(frameNombreFavorito, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4, width=30)
        nombreFavorito.pack(side=tk.RIGHT, fill="x")

        #Creamos un boton para guardar los cambios
        botonRenombrar = tk.Button(ventanaRenombrar, text="Renombrar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, 
                                    command=lambda: guardarCambiosRenombrar(ventanaRenombrar, nombreFavorito), font=("Montserrat", 12))
        botonRenombrar.pack(side=tk.BOTTOM, pady=10)


    def eliminarFavorito():
        with open("favoritos.txt", "r") as f1:
            lines = f1.readlines()
            numFavoritos = len(lines)-1
        with open("favoritos.txt", "w") as f2:
            for indice, linea in enumerate(lines):
                if indice != abrirFavoritos.lineaActual:
                    f2.write(linea)
                else:
                    lineaDividida = linea.split(']')
                    if lineaDividida[-1] != "\n":
                        rutaYTitulo = lineaDividida[-1][:-1].split(r" %%% ")
                        ruta = rutaYTitulo[0]
                    os.remove(ruta)
        messagebox.showinfo("Favorito Eliminado", "Se ha eliminado el SFI actual de favoritos", parent=ventanaFavoritos)

        # Destruimos y volvemos a mostrar el texto
        frameLabels = ventanaFavoritos.winfo_children()[1]
        labelLineaActual = frameLabels.winfo_children()[0]
        labelSFIActual = frameLabels.winfo_children()[1]
        labelLineaActual.destroy()
        labelSFIActual.destroy()

        # Actualizamos los botones
        if numFavoritos >= 1:
            if abrirFavoritos.lineaActual == numFavoritos:
                abrirFavoritos.lineaActual -= 1
            numLineas = displaySFIFavoritos(frameLabels)
        else:
            ventanaFavoritos.destroy()

        if abrirFavoritos.lineaActual == numFavoritos-1:
            botonSiguiente.config(state=tk.DISABLED)
        else:            
            botonSiguiente.config(state=tk.NORMAL)
            
        if abrirFavoritos.lineaActual == 0:
            botonAnterior.config(state=tk.DISABLED)
        else:
            botonAnterior.config(state=tk.NORMAL)

    def mostrarSFI():
        with open("favoritos.txt", "r") as f:
            lines = f.readlines()
            linea = (lines[abrirFavoritos.lineaActual])
            lineaDividida = linea.split(']')
            if lineaDividida[-1] != "\n":
                    rutaYTitulo = lineaDividida[-1][:-1].split(r" %%% ")
                    ruta = rutaYTitulo[0]                
            #Ahora mostramos la imagen de ruta
            window = tk.Toplevel(root)
            window.lift()
            window_width = 800
            window_height = 600
            center_x = int(screen_width/2 - window_width / 2)
            center_y = int(screen_height/2 - window_height / 2)
            window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
            window.lift()
            
            img1 = Image.open(ruta)
            img2 = img1.resize((800, 600))
            img3 = ImageTk.PhotoImage(img2)
            canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
            canvas.create_image(0, 0, image=img3, anchor=tk.NW)
            canvas.pack(padx=10, pady=(3, 0), fill="both", expand="yes")
            window.mainloop()



    def siguienteSFI():
        abrirFavoritos.lineaActual += 1
        #Accedemos a frameBotones
        frameBotones = ventanaFavoritos.winfo_children()[0]
        botonAnterior = frameBotones.winfo_children()[0]
        botonSiguiente = frameBotones.winfo_children()[1]
        botonMostrar = frameBotones.winfo_children()[2]
        botonEliminar = frameBotones.winfo_children()[3]

        # Accedemos a frameLabels
        frameLabels = ventanaFavoritos.winfo_children()[1]
        labelLineaActual = frameLabels.winfo_children()[0]
        labelSFIActual = frameLabels.winfo_children()[1]
        
        labelLineaActual.destroy()
        labelSFIActual.destroy()
        numFavoritos = displaySFIFavoritos(frameLabels)

        if abrirFavoritos.lineaActual == numFavoritos-1:
            botonSiguiente.config(state=tk.DISABLED)
        else:
            botonSiguiente.config(state=tk.NORMAL)
        if abrirFavoritos.lineaActual == 0:
            botonAnterior.config(state=tk.DISABLED)
        else:
            botonAnterior.config(state=tk.NORMAL)

    def anteriorSFI():
        abrirFavoritos.lineaActual -= 1
        #Accedemos a frameBotones
        frameBotones = ventanaFavoritos.winfo_children()[0]
        botonAnterior = frameBotones.winfo_children()[0]
        botonSiguiente = frameBotones.winfo_children()[1]
        botonMostrar = frameBotones.winfo_children()[2]
        botonEliminar = frameBotones.winfo_children()[3]

        # Accedemos a frameLabels
        frameLabels = ventanaFavoritos.winfo_children()[1]
        labelLineaActual = frameLabels.winfo_children()[0]
        labelSFIActual = frameLabels.winfo_children()[1]
        
        labelLineaActual.destroy()
        labelSFIActual.destroy()
        numFavoritos = displaySFIFavoritos(frameLabels)

        if abrirFavoritos.lineaActual == numFavoritos-1:
            botonSiguiente.config(state=tk.DISABLED)
        else:
            botonSiguiente.config(state=tk.NORMAL)
        if abrirFavoritos.lineaActual == 0:
            botonAnterior.config(state=tk.DISABLED)
        else:
            botonAnterior.config(state=tk.NORMAL)

#Ventana Historial
def abrirHistorial():
    def displaySFIHistorial(frameLabels):
        with open("history.txt", "r") as f:
            lines = f.readlines()
            numLineas = len(lines)
            #Creamos un label para la linea actual
            linea = (lines[abrirHistorial.lineaActual])
            lineaDividida = linea.split(']')
            primeraDivision = lineaDividida[0].split('[')
            iters = primeraDivision[0][2:]
            match linea[0]:
                case "D":
                    titulo = "Resultado "+str(numLineas-abrirHistorial.lineaActual)
                    sfi = "Algoritmo Determinista, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = ""
                case "A":
                    titulo = "Resultado "+str(numLineas-abrirHistorial.lineaActual)
                    sfi = "Algoritmo Aleatorio, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = ""
                case "P":
                    titulo = "Resultado "+str(numLineas-abrirHistorial.lineaActual)
                    lineaDividida = linea.split(']')
                    sfi = "Algoritmo Aleatorio, " + iters + "iteraciones. " + "SFI:\n" + str(np.fromstring(primeraDivision[1], sep=' ').reshape(-1,6))
                    psfi = "Probabilidades: " + str(np.fromstring(lineaDividida[1][2:], sep= ' '))
                case "_":
                    print("Error! En el formato del historial")
            if lineaDividida[-1] != "\n":
                ruta = lineaDividida[-1][:-1]

            labelLineaActual = tk.Label(frameLabels, text=titulo, bg=COLOR1, fg=COLOR4, font=("Courier", 14, "bold", "underline"))
            labelLineaActual.pack(side=tk.TOP, padx=10, pady=8, fill="x")
            
            labelSFIActual = tk.Label(frameLabels, text=sfi+"\n"+psfi, bg=COLOR1, fg=COLOR4, font=("Arial", 12, ))
            labelSFIActual.pack(side=tk.TOP, fill="x")

    if not os.path.exists(r"history.txt"):
        with open("history.txt", "w") as f:
            print("Creando Archivo de Historial")
            pass
    with open("history.txt", "r") as f:
        numLineas = len(f.readlines())
        abrirHistorial.lineaActual = numLineas-1
    if numLineas == 0:
        messagebox.showinfo("Historial", "¡No hay resultados en el historial! Ejecuta algún algoritmo para que se añada automáticamente al historial")
    else:
        #Abrimos una nueva ventana
        ventanaHistorial = tk.Toplevel(root)
        #Le damos un titulo y un tamaño
        ventanaHistorial.title("Historial")
        window_width = 525
        window_height = 325
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        ventanaHistorial.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        #Cambiamos el color del fondo
        ventanaHistorial.config(bg=COLOR1)
        ventanaHistorial.lift(root)
        #ventanaHistorial.attributes("-topmost", True)
    
        #Creamos botones para movernos entre SFIs:
        frameBotones = tk.Frame(ventanaHistorial, bg=COLOR1)
        frameBotones.pack(side=tk.BOTTOM)
        botonAnterior = tk.Button(frameBotones, text="Anterior", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: anteriorSFI(), font=("Montserrat", 12))
        botonAnterior.pack(side=tk.LEFT, padx=10, pady=10)
        botonSiguiente = tk.Button(frameBotones, text="Siguiente", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: siguienteSFI(), font=("Montserrat", 12), state=tk.DISABLED)
        botonSiguiente.pack(side=tk.LEFT, padx=10, pady=10)
        botonMostrar = tk.Button(frameBotones, text="Mostrar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: mostrarSFI(), font=("Montserrat", 12))
        botonMostrar.pack(side=tk.LEFT, padx=10, pady=10)
        botonFavoritos = tk.Button(frameBotones, text="Favoritos", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: guardarFavorito(), font=("Montserrat", 12))
        botonFavoritos.pack(side=tk.LEFT, padx=10, pady=10)
        
        #Creamos un frame para los labels
        frameLabels = tk.Frame(ventanaHistorial, bg=COLOR1)
        frameLabels.pack(side=tk.TOP, fill="x")
        displaySFIHistorial(frameLabels)

        if numLineas == 1:
            botonAnterior.config(state=tk.DISABLED)

    

    def guardarFavorito():
        with open("history.txt", "r") as h:
            lines = h.readlines()
            linea = (lines[abrirHistorial.lineaActual])
            if not os.path.exists(r"Favoritos"):
                os.makedirs(r"Favoritos")
            #Contamos el numero de ficheros que ya hay en la carpeta de favoritos
            numFavoritos = len(os.listdir(r"Favoritos"))

            #Copiamos la imagen del fractal y la guardamos en la carpeta de favoritos
            lineaDividida = linea.split(']')
            if lineaDividida[-1] != "\n":
                ruta = lineaDividida[-1][:-1]
                rutaFavoritos = "Favoritos\\favorito"+str(numFavoritos)+".png"
                shutil.copyfile(ruta, rutaFavoritos)
            #Reescribimos la linea pero cambiando ruta por rutaFavoritos
            lineaDividida[-1] = rutaFavoritos+"\n"
            linea = "]".join(lineaDividida)
            lineaSinRuta = "]".join(lineaDividida[:-1])
            lineaSinTitulo = linea.split(r' %%% ')[0]
            
            #Si el archivo favoritos.txt no existe lo creamos
            if not os.path.exists(r"favoritos.txt"):
                with open("favoritos.txt", "w") as f:
                    pass
            with open("favoritos.txt", "r") as f:
                lines = f.readlines()
                for l in lines:
                    #l2 = l.split(r' %%% ')[0]+'\n'
                    l2 = "]".join(l.split(']')[:-1])
                    print(l2)
                    print(lineaSinRuta)
                    if l2 == lineaSinRuta:
                        messagebox.showinfo("Información", "Este SFI ya está guardado como favorito", parent=ventanaHistorial)
                        return
            with open("favoritos.txt", "a") as f:
                f.write(linea)
        messagebox.showinfo("Favorito", "Se ha guardado el SFI actual como favorito", parent=ventanaHistorial)
        
    def mostrarSFI():
        with open("history.txt", "r") as f:
            lines = f.readlines()
            linea = (lines[abrirHistorial.lineaActual])
            lineaDividida = linea.split(']')
            if lineaDividida[-1] != "\n":
                    ruta = lineaDividida[-1][:-1]
            #Ahora mostramos la imagen de ruta
            window = tk.Toplevel(root)
            window_width = 800
            window_height = 600
            center_x = int(screen_width/2 - window_width / 2)
            center_y = int(screen_height/2 - window_height / 2)
            window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
            window.lift()
            #window.attributes("-topmost", True)
            img1 = Image.open(ruta)
            img2 = img1.resize((800, 600))
            img3 = ImageTk.PhotoImage(img2)
            canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
            canvas.create_image(0, 0, image=img3, anchor=tk.NW)
            canvas.pack(padx=10, pady=(3, 0), fill="both", expand="yes")
            window.mainloop()
            

    def siguienteSFI():
        abrirHistorial.lineaActual += 1

        # Accedemos a frameLabels
        frameLabels = ventanaHistorial.winfo_children()[1]
        labelLineaActual = frameLabels.winfo_children()[0]
        labelSFIActual = frameLabels.winfo_children()[1]
        
        labelLineaActual.destroy()
        labelSFIActual.destroy()
        displaySFIHistorial(frameLabels)

        #Accedemos a frameBotones
        frameBotones = ventanaHistorial.winfo_children()[0]
        botonAnterior = frameBotones.winfo_children()[0]
        botonSiguiente = frameBotones.winfo_children()[1]

        if abrirHistorial.lineaActual == numLineas-1:
            botonSiguiente.config(state=tk.DISABLED)
        else:
            botonSiguiente.config(state=tk.NORMAL)
        if abrirHistorial.lineaActual == 0:
            botonAnterior.config(state=tk.DISABLED)
        else:
            botonAnterior.config(state=tk.NORMAL)

    def anteriorSFI():
        abrirHistorial.lineaActual -= 1

        # Accedemos a frameLabels
        frameLabels = ventanaHistorial.winfo_children()[1]
        labelLineaActual = frameLabels.winfo_children()[0]
        labelSFIActual = frameLabels.winfo_children()[1]
        
        labelLineaActual.destroy()
        labelSFIActual.destroy()
        displaySFIHistorial(frameLabels)

        #Accedemos a frameBotones
        frameBotones = ventanaHistorial.winfo_children()[0]
        botonAnterior = frameBotones.winfo_children()[0]
        botonSiguiente = frameBotones.winfo_children()[1]
        if abrirHistorial.lineaActual == numLineas-1:
            botonSiguiente.config(state=tk.DISABLED)
        else:
            botonSiguiente.config(state=tk.NORMAL)
        if abrirHistorial.lineaActual == 0:
            botonAnterior.config(state=tk.DISABLED)
        else:
            botonAnterior.config(state=tk.NORMAL)

#Ventana Ayuda
def abrirAyuda():
    #Abrimos una nueva ventana
    ventanaAyuda = tk.Toplevel(root)
    #Le damos un titulo y un tamaño
    ventanaAyuda.title("Ayuda")
    window_width = 800
    window_height = 625
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    ventanaAyuda.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    #Cambiamos el color del fondo
    ventanaAyuda.config(bg=COLOR1)
    ventanaAyuda.lift()
    #Creamos un frame para los labels
    frameLabels = tk.Frame(ventanaAyuda, bg=COLOR1)
    frameLabels.pack(side=tk.TOP, fill="x")
    labelAyuda = tk.Label(frameLabels, text="Ayuda", bg=COLOR1, fg=COLOR4, font=("Courier", 14, "bold", "underline"))
    labelAyuda.pack(side=tk.TOP, fill="x")
    text = '''¡Bienvenidx! Esta es la ventana de ayuda. Aquí podrás encontrar información sobre el funcionamiento de la aplicación.
Esta aplicación está diseñada para generar fractales a partir de un SFI (Sistema de Funciones Iteradas). \
Un SFI es un conjunto de funciones con la siguiente forma:'''
    labelAyuda2 = tk.Label(frameLabels, text=text, bg=COLOR1, fg=COLOR4, font=("Arial", 12), wraplength=775, justify=tk.LEFT)
    labelAyuda2.pack(side=tk.TOP, fill="x")
    imagenEcuacionCian = ImageTk.PhotoImage(Image.open("assets\\EcuacionCian.png"))
    label = tk.Label(frameLabels, image=imagenEcuacionCian, bg=COLOR1) # Crear un label
    label.image=imagenEcuacionCian
    label.pack(side=tk.TOP) # Empaquetar el label
    text2 = '''donde {a, b, c, d, e f} son coeficientes introducidos por el usuario, y {x, y} son las coordenadas de un punto del plano. \
Estos coeficientes deben corresponder a una función contractiva, es decir, que la norma de la función sea menor que 1.
Para introducir funciones, escribe los coeficientes en los campos de texto correspondientes y pulsa el botón "Añadir función". \
Verás que se muestran las funciones añadidas a la izquierda. 
Cuando tengas las que quieres, pulsa debajo el botón del algoritmo que quieras utilizar para calcular el fractal. \
Los dos algoritmos son el Algoritmo Determinista y el Algoritmo Aleatorio. Bajo cada botón, \
podrás elegir el número de iteraciones que se harán del algoritmo.
Por ejemplo, prueba a utilizar el Algoritmo Determinista con 0, 1, y 2 iteraciones sobre el siguiente SFI y observa los resultados:'''
    labelAyuda3 = tk.Label(frameLabels, text=text2, bg=COLOR1, fg=COLOR4, font=("Arial", 12), wraplength=775, justify=tk.LEFT)
    labelAyuda3.pack(side=tk.TOP, fill="x")
    imagenSFI = ImageTk.PhotoImage(Image.open("assets\\SFI.png"))
    label = tk.Label(frameLabels, image=imagenSFI, bg=COLOR1) # Crear un label
    label.image=imagenSFI
    label.pack(side=tk.TOP) # Empaquetar el label

    text3 = '''Finalmente, en la barra superior de la aplicación tienes disponibles varios botones que abren menús adicionales, \
como el que pulsaste para abrir esta ventana. En orden de derecha a izquierda, son: este menú de ayuda, el menú para escoger el color de \
los fractales, el menú de fractales guardados como favoritos, el historial de resultados anteriores (desde donde puedes añadir fractales a Favorios), y el menú de opciones.
En este menú de opciones, podrás escoger el tamaño del historial, los detalles de la figura inicial utilizada para el Algoritmo Determinista, y \
el método de cálculo para las probabilidades en el Algoritmo Aleatorio.'''
    labelAyuda4 = tk.Label(frameLabels, text=text3, bg=COLOR1, fg=COLOR4, font=("Arial", 12), wraplength=775, justify=tk.LEFT)
    labelAyuda4.pack(side=tk.TOP, fill="x")

#Ventana Colores
def abrirColores():
    #Abrimos una nueva ventana
    ventanaColores = tk.Toplevel(root)
    #Le damos un titulo y un tamaño
    ventanaColores.title("Colores")
    window_width = 400
    window_height = 50
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    ventanaColores.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    #Cambiamos el color del fondo
    ventanaColores.config(bg=COLOR1)
    ventanaColores.lift()
    #Creamos un frame para los labels
    frameLabels = tk.Frame(ventanaColores, bg=COLOR1)
    frameLabels.pack(side=tk.TOP, padx=10, pady=(0, 0))
    labelColor0 = tk.Label(frameLabels, text="Color de los Fractales", bg=COLOR1, fg=COLOR4, font=("Arial", 12))
    labelColor0.pack(side=tk.LEFT, padx=10, pady=(3, 0))
    #Añadimos un recuadro para que se vea el color actual
    frameColor0 = tk.Frame(frameLabels, bg=COLOR0, width=20, height=20)
    frameColor0.pack(side=tk.LEFT, padx=10, pady=(3, 0))
    botonColor0 = tk.Button(frameLabels, text="Cambiar", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: cambiarColor(0), font=("Montserrat", 12))
    botonColor0.pack(side=tk.LEFT, padx=10, pady=(3, 3))
    

    #COLOR0 = '#00BFBF' #fractales
    #COLOR1 = "#263D42" #ventana
    #COLOR2 = "#262626" #frames
    #COLOR3 = "cyan"  #botones
    #COLOR4 = "white" #texto

    def cambiarColor(n):
        color = askcolor(color=None, title="Elige un color", parent=ventanaColores)
        match n:
            case 0:
                global COLOR0
                COLOR0 = color[1]
                with open("config.cfg", "r") as f:
                    lineas = f.readlines()
                lineas[5] = "COLOR0="+COLOR0+"\n"
                with open("config.cfg", "w") as f:
                    f.writelines(lineas)
                frameColor0.config(bg=COLOR0)

#Añadir Funciones
def isContractiva(func):
    funcion = np.array(func)
    norma = np.linalg.norm((funcion[:4]).reshape(2,2), 2)
    if norma >= 1:
        return False
    else:
        return True
    
def addFunction():
    global listaSFI
   
    a = texta.get() or 0.000
    b = textb.get() or 0.000
    c = textc.get() or 0.000
    d = textd.get() or 0.000
    e = texte.get() or 0.000
    f = textf.get() or 0.000
    funcion = [float(a), float(b), float(c), float(d), float(e), float(f)]
    if(isContractiva(funcion) == False):
        print("No es contractiva")
        messagebox.showerror('Error', 'Error: La función introducida no es contractiva')
        return
    listaSFI.append(funcion)
    texto = "a = "+str(a)[:7]+"; b = "+str(b)[:7]+"; c = "+str(c)[:7]+"; d = "+str(d)[:7]+"; e = "+str(e)[:7]+"; f = "+str(f)[:7]
    frame = tk.Frame(frame1, bg=COLOR1) # Crear un frame
    if len(listaSFI) == 1:
        frame.pack(pady=(3,1))
    else:
        frame.pack(pady=1)    
    label = tk.Label(frame, text=texto, fg=COLOR4, bg=COLOR1) # Crear un label dentro de frame
    label.pack(side="left", fill="none")
    #Creamos botón para eliminar el label anterior 
    button = tk.Button(frame, fg=COLOR4, bg=COLOR2, activebackground=COLOR2, text="Eliminar", command=lambda: deleteFunction(funcion, frame), font=("Montserrat", 10))
    #button = tk.Button(frame, fg=COLOR4, bg=COLOR1, activebackground=COLOR1, activeforeground=COLOR4, text="Eliminar", command=lambda: deleteFunction(funcion, frame), font=("Montserrat", 10))
    button.pack(side="left")
    
def deleteFunction(funcion, frame):
    global listaSFI
    listaSFI.remove(funcion) # Eliminar el elemento de la lista
    frame.destroy() # Eliminar el frame

#Llamar Algoritmos

#Determinista
def algoritmoDeterminista():
    global figuraInicial
    global aristaInicial
    global rotacionInicial
    if numeroIteracionesDet.get() != "":
        ITERACIONES_DETERMINISTA = int(numeroIteracionesDet.get())
        #Leemos del archivo cfg
        with open("config.cfg", "r") as f:
            lineas = f.readlines()
        lineas[1] = "ITERACIONES_DETERMINISTA="+str(ITERACIONES_DETERMINISTA)+"\n"
        #Guardamos los cambios en el archivo cfg
        with open("config.cfg", "w") as f:   
            f.writelines(lineas)
    SFI = np.array(listaSFI)
    i = 0
    if not os.path.exists(r"Historial"):
        os.makedirs(r"Historial")
    ruta = r"Historial\result"
    while os.path.exists('{}{:d}.png'.format(ruta, i)):
        i += 1
    rutaFinal = '{}{:d}.png'.format(ruta, i)
    
    #Obtenemos la figura inicial y su arista
    match figuraInicial.get():
        case "Triangulo":
            lados = 3
        case "Cuadrado":
            lados = 4
        case "Pentagono":
            lados = 5
        case "Hexagono":
            lados = 6
        case _:
            lados = 3
            firstPoints = np.array([[0,0], [1,0], [0.5, 3**0.5/2]])
    angulo = (2*np.pi/lados)
    firstPoints = np.column_stack((np.cos(np.arange(lados-1)*angulo+float(rotacionInicial.get())*np.pi/180), np.sin(np.arange(lados-1)*angulo+float(rotacionInicial.get())*np.pi/180)))
    firstPoints = np.append([[0,0]], np.cumsum(firstPoints, axis=0), axis=0)
    arista = float(aristaInicial.get())
    firstPoints = firstPoints*arista
    firstPoints = firstPoints + [float(coordenadaXInicial.get()), float(coordenadaYInicial.get())]
    #Llamamos al algoritmo Determinista  
    fig = algDeterminista(SFI, ITERACIONES_DETERMINISTA, COLOR0, firstPoints)

    fig.savefig(rutaFinal, dpi=1200, transparent=True)
    try:
        with open("history.txt", "a") as f:
            f.write("D "+ str(ITERACIONES_DETERMINISTA) + " " + str(SFI.flatten())+rutaFinal+"\n")
    except FileNotFoundError:
        print("File not found")
        with open("history.txt", "w") as f:
            f.write("D "+ str(ITERACIONES_DETERMINISTA) + " " + str(SFI.flatten())+rutaFinal+"\n")
    #Contamos el número de líneas del historial y si hay más del maximo eliminamos las sobrantes
    num_lineas = sum(1 for line in open("history.txt"))
    if num_lineas > TAMANHO_HISTORIAL:
        with open("history.txt", "r") as fin:
            data = fin.read().splitlines(True)
            lineasSobrantes = data[:(num_lineas-TAMANHO_HISTORIAL)]
            for l in lineasSobrantes:
                lDividida = l.split(']')
                if lDividida[-1] != "\n":
                    os.remove(lDividida[-1][:-1])
        with open("history.txt", "w") as fout:
            fout.writelines(data[-TAMANHO_HISTORIAL:])

    #Hacemos que se abra en otra ventana
    window = tk.Toplevel(root)
    window.title("Algoritmo determinista")
    window_width = 800
    window_height = 600
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    window.lift()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

#Aleatorio
def algoritmoAleatorio():
    global ITERACIONES_ALEATORIO
    if numeroIteracionesAlea.get() != "":
        ITERACIONES_ALEATORIO = int(numeroIteracionesAlea.get())
        #Leemos del archivo cfg
        with open("config.cfg", "r") as f:
            lineas = f.readlines()
        lineas[2] = "ITERACIONES_ALEATORIO="+str(ITERACIONES_ALEATORIO)+"\n"
        #Guardamos los cambios en el archivo cfg
        with open("config.cfg", "w") as f:   
            f.writelines(lineas)
    SFI = np.array(listaSFI)
    if probManual.get():
        #Creamos una ventana para insertar las probabilidades
        ventanaProb = tk.Toplevel(root)
        ventanaProb.lift()
        ventanaProb.title("Probabilidades")
        window_width = 500
        window_height = 200
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        ventanaProb.geometry(f"+{center_x}+{center_y}")
        #Cambiamos el COLOR1 del fondo
        ventanaProb.config(bg=COLOR1)
        entry_values = []
        #Creamos un campo de texto para introducir la probabilidad de cada SFI
        frame1 = tk.Frame(ventanaProb, bg=COLOR1)
        frame1.pack()
        for i, sfi in enumerate(SFI):
            frame2 = tk.Frame(frame1, bg=COLOR1)
            frame2.pack()
            labelSFI = tk.Label(frame2, text="Funcion "+str(i+1)+": "+str(sfi), bg=COLOR1, fg=COLOR4, font=("Arial", 12))
            labelSFI.pack(side=tk.LEFT)
            numeroSFI = tk.Entry(frame2, bg=COLOR2, fg=COLOR4, font=("Arial", 12), insertbackground=COLOR4)
            numeroSFI.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=3)
            entry_values.append(numeroSFI)
        #Creamos un boton para llamar al algoritmo aleatorio
        botonLlamarAleatorio = tk.Button(ventanaProb, text="Llamar algoritmo aleatorio", fg=COLOR4, bg=COLOR2, activebackground=COLOR2, command=lambda: llamarAleatorio(entry_values, ventanaProb), font=("Montserrat", 12))
        botonLlamarAleatorio.pack(side=tk.BOTTOM, pady=10)
    else:
        
        fig = algAleatorio(None, SFI, ITERACIONES_ALEATORIO, COLOR0)
        i = 0
        if not os.path.exists(r"Historial"):
            os.makedirs(r"Historial")
        ruta = r"Historial\result"
        while os.path.exists('{}{:d}.png'.format(ruta, i)):
            i += 1
        rutaFinal = '{}{:d}.png'.format(ruta, i)

        fig.savefig(rutaFinal, dpi=300, transparent=True)

        try:
            with open("history.txt", "a") as f:
                f.write("A "+ str(ITERACIONES_ALEATORIO) + " " + str(SFI.flatten())+rutaFinal+"\n")
        except FileNotFoundError:
            print("File not found")
            with open("history.txt", "w") as f:
                f.write("A "+ str(ITERACIONES_ALEATORIO) + " " + str(SFI.flatten())+rutaFinal+"\n")
        #Contamos el número de líneas del fichero
        num_lineas = sum(1 for line in open("history.txt"))
        #Si hay más de N eliminamos la primera (no queremos un historial muy grande)
        if num_lineas > TAMANHO_HISTORIAL:
            with open("history.txt", "r") as fin:
                data = fin.read().splitlines(True)
                lineasSobrantes = data[:(num_lineas-TAMANHO_HISTORIAL)]
                for l in lineasSobrantes:
                    lDividida = l.split(']')
                    if lDividida[-1] != "\n":
                        os.remove(lDividida[-1][:-1])
            with open("history.txt", "w") as fout:
                fout.writelines(data[-TAMANHO_HISTORIAL:])
        window = tk.Toplevel(root)
        window.lift()
        window.title("Algoritmo aleatorio")
        window_width = 800
        window_height = 600
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

#Aleatorio con probabilidades
def llamarAleatorio(entry_values, ventanaProb):
    probSFI = np.array([float(entry.get()) for entry in entry_values])
    if probSFI.sum() != 1:
        messagebox.showerror('Error', 'Error: Las probabilidades deben sumar 1')
        return
    SFI = np.array(listaSFI)

    i = 0
    if not os.path.exists(r"Historial"):
        os.makedirs(r"Historial")
    ruta = r"Historial\result"
    while os.path.exists('{}{:d}.png'.format(ruta, i)):
        i += 1
    rutaFinal = '{}{:d}.png'.format(ruta, i)


    fig = algAleatorio(probSFI, SFI, ITERACIONES_ALEATORIO, COLOR0)

    try:
        with open("history.txt", "a") as f:
                f.write("P "+ str(ITERACIONES_ALEATORIO) + " " +str(SFI.flatten())+" "+str(probSFI)+rutaFinal+"\n")       
    except FileNotFoundError:
        print("File not found")
        with open("history.txt", "w") as f:
            f.write("P "+ str(ITERACIONES_ALEATORIO) + " " +str(SFI.flatten())+" "+str(probSFI)+rutaFinal+"\n")  
    #Contamos el número de líneas del fichero
    num_lineas = sum(1 for line in open("history.txt"))
    #Si hay más de diez eliminamos la primera (no queremos un historial muy grande)
    if num_lineas > TAMANHO_HISTORIAL:
        with open("history.txt", "r") as fin:
            data = fin.read().splitlines(True)
            lineasSobrantes = data[:(num_lineas-TAMANHO_HISTORIAL)]
            for l in lineasSobrantes:
                lDividida = l.split(']')
                if lDividida[-1] != "\n":
                    os.remove(lDividida[-1][:-1])
        with open("history.txt", "w") as fout:
            fout.writelines(data[-TAMANHO_HISTORIAL:])            

    fig.savefig(rutaFinal, dpi=300, transparent=True)

    ventanaProb.destroy()
    window = tk.Toplevel(root)
    window.lift()
    window.title("Algoritmo aleatorio")
    window_width = 800
    window_height = 600
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

#Ventana Principal
root.config(bg=COLOR1) # Cambiar el COLOR1 de fondo de la ventana
window_width = 1000
window_height = 620
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f"1000x620+{center_x}+{center_y}") # Cambiar el tamaño de la ventana

#Frames
#Frame para las funciones del SFI
frame1 = tk.Frame(root, bg=COLOR2) # Crear un frame
frame1.place(relwidth=0.40, relheight=0.50, relx=0.05, rely=0.15) # Posicionar el frame
#El Frame que tiene justo debajo para el botón
frame1b = tk.Frame(root, bg=COLOR2) # Crear un frame
frame1b.place(relwidth=0.40, relheight=0.30, relx=0.05, rely=0.65)
#Frame para añadir funciones al SFI
frame2 = tk.Frame(root, bg=COLOR2) # Crear un frame
frame2.place(relwidth=0.4, relheight=0.8, relx=0.55, rely=0.15) # Posicionar el frame
#Frame para los botones
frame3 = tk.Frame(root, bg=COLOR2) # Crear un frame
frame3.place(relwidth=1.0, relheight=0.0605, relx=0.00, rely=0.00) # Posicionar el frame
#Frame para el titulo
frame4 = tk.Frame(root, bg=COLOR1) # Crear un frame
frame4.place(relwidth=0.40, relheight=0.065, relx=0.05, rely=0.07) # Posicionar el frame
label = tk.Label(frame4, text="Sistema de Funciones Iteradas", justify="center", font=("Courier", 16, "bold"), fg=COLOR4, bg=COLOR1, pady=10) # Crear un label
label.pack() # Empaquetar el text
#Frame para el titulo
frame5 = tk.Frame(root, bg=COLOR1) # Crear un frame
frame5.place(relwidth=0.35, relheight=0.065, relx=0.58, rely=0.07) # Posicionar el frame
label = tk.Label(frame5, text="Añadir Funciones al SFI", justify='center', font=("Courier", 16, "bold"), fg=COLOR4, bg=COLOR1, pady=10) # Crear un label
label.pack() # Empaquetar el label
#Frame para la imagen de la ecuación
frame6 = tk.Frame(frame2, bg=COLOR2) # Crear un frame
frame6.place(relwidth=0.75, relheight=0.10, relx=0.125, rely=0.05) # Posicionar el frame
imagenEcuacion = ImageTk.PhotoImage(Image.open("assets\\EcuacionOscura.png")) #Imagen modo oscuro
label = tk.Label(frame6, image=imagenEcuacion, bg=COLOR2, font=("Courier", 14)) # Crear un label
label.image=imagenEcuacion
label.pack() # Empaquetar el label

#Parametros
#Campos de texto para los parametros de la ecuacion
labela = tk.Label(frame2, text="a =", fg=COLOR4, bg=COLOR2, font=('Cambria', 18, "italic")) # Crear un label
labelb = tk.Label(frame2, text="b =", fg=COLOR4, bg=COLOR2, font=("Cambria", 18, "italic")) # Crear un label
labelc = tk.Label(frame2, text="c =", fg=COLOR4, bg=COLOR2, font=("Cambria", 18, "italic")) # Crear un label
labeld = tk.Label(frame2, text="d =", fg=COLOR4, bg=COLOR2, font=("Cambria", 18, "italic")) # Crear un label
labele = tk.Label(frame2, text="e =", fg=COLOR4, bg=COLOR2, font=("Cambria", 18, "italic")) # Crear un label
labelf = tk.Label(frame2, text="f =", fg=COLOR4, bg=COLOR2, font=("Cambria", 18, "italic")) # Crear un label

labela.place(relwidth=0.1, relheight=0.05, relx=0.05, rely=0.20) # Posicionar el label
labelb.place(relwidth=0.1, relheight=0.05, relx=0.50, rely=0.20) # Posicionar el label
labelc.place(relwidth=0.1, relheight=0.05, relx=0.05, rely=0.30) # Posicionar el label
labeld.place(relwidth=0.1, relheight=0.05, relx=0.50, rely=0.30) # Posicionar el label
labele.place(relwidth=0.1, relheight=0.05, relx=0.05, rely=0.45) # Posicionar el label
labelf.place(relwidth=0.1, relheight=0.05, relx=0.50, rely=0.45) # Posicionar el label

#Creamos frames para los campos de texto
framea = tk.Frame(frame2, bg=COLOR2) # Crear un frame
framea.place(relwidth=0.3, relheight=0.05, relx=0.16, rely=0.2)
texta = tk.Entry(framea, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
#texta.insert(0, '0.500')
texta.pack()
frameb = tk.Frame(frame2, bg=COLOR2) # Crear un frame
frameb.place(relwidth=0.3, relheight=0.05, relx=0.61, rely=0.2)
textb = tk.Entry(frameb, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
textb.pack()
framec = tk.Frame(frame2, bg=COLOR2) # Crear un frame
framec.place(relwidth=0.3, relheight=0.05, relx=0.16, rely=0.3)
textc = tk.Entry(framec, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
textc.pack()
framed = tk.Frame(frame2, bg=COLOR2) # Crear un frame
framed.place(relwidth=0.3, relheight=0.05, relx=0.61, rely=0.3)
textd = tk.Entry(framed, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
#textd.insert(0, '0.500')
textd.pack()
framee = tk.Frame(frame2, bg=COLOR2) # Crear un frame
framee.place(relwidth=0.3, relheight=0.05, relx=0.16, rely=0.45)
texte = tk.Entry(framee, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
#texte.insert(0, '0.250')
texte.pack()
framef = tk.Frame(frame2, bg=COLOR2) # Crear un frame
framef.place(relwidth=0.3, relheight=0.05, relx=0.61, rely=0.45)
textf = tk.Entry(framef, bd=3, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4) # Crear un text
#textf.insert(0, '0.433')
textf.pack()

#Botones
#Creamos los botones
botonAnhadirFuncion = tk.Button(frame2, text="¡Añadir\nFunción!", font=("Montserrat", 16), padx=10, pady=5, fg=COLOR4, bg=COLOR1, activebackground=COLOR1, activeforeground=COLOR4, command=lambda: addFunction()) # Crear un botón
botonAnhadirFuncion.place(relwidth=0.7, relheight=0.35, relx=0.15, rely=0.575) # Posicionar el botón
#Creamos un botón para usar el algoritmo determinista
botonAlgoritmoDeterminista = tk.Button(frame1b, text="Algoritmo\nDeterminista", font=("Montserrat", 16), padx=10, pady=5, fg=COLOR4, bg=COLOR1, activebackground=COLOR1, activeforeground=COLOR4, command=lambda: algoritmoDeterminista()) # Crear un botón
botonAlgoritmoDeterminista.place(relwidth=0.40, relheight=0.50, relx=0.05, rely=0.05) # Posicionar el botón
#Creamos un botón para usar el algoritmo aleatorio
botonAlgoritmoAleatorio = tk.Button(frame1b, text="Algoritmo\nAleatorio", font=("Montserrat", 16), padx=10, pady=5, fg=COLOR4, bg=COLOR1, activebackground=COLOR1, activeforeground=COLOR4, command=lambda: algoritmoAleatorio()) # Crear un botón
botonAlgoritmoAleatorio.place(relwidth=0.40, relheight=0.50, relx=0.55, rely=0.05) # Posicionar el botón
#Creamos un campo de texto para introducir el numero de iteraciones para el algoritmo determinista
frameIteracionesDet = tk.Frame(frame1b, bg=COLOR1)
frameIteracionesDet.place(relwidth=0.40, relheight=0.20, relx=0.05, rely=0.60)
labelIteracionesDet = tk.Label(frameIteracionesDet, text="Iteraciones:", bg=COLOR1, fg=COLOR4, font=("Courier", 11))
labelIteracionesDet.pack(side=tk.LEFT)
numeroIteracionesDet = tk.Entry(frameIteracionesDet, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4)
numeroIteracionesDet.insert(0, str(ITERACIONES_DETERMINISTA))
numeroIteracionesDet.pack(side=tk.LEFT, fill="x", padx=3)
#Creamos un campo de texto para introducir el numero de iteraciones para el algoritmo aleatorio
frameIteracionesAlea = tk.Frame(frame1b, bg=COLOR1)
frameIteracionesAlea.place(relwidth=0.40, relheight=0.20, relx=0.55, rely=0.60)
labelIteracionesAlea = tk.Label(frameIteracionesAlea, text="Iteraciones:", bg=COLOR1, fg=COLOR4, font=("Courier", 11))
labelIteracionesAlea.pack(side=tk.LEFT)
numeroIteracionesAlea = tk.Entry(frameIteracionesAlea, fg=COLOR4, bg=COLOR2, insertbackground=COLOR4)
numeroIteracionesAlea.insert(0, str(ITERACIONES_ALEATORIO))
numeroIteracionesAlea.pack(side=tk.LEFT, fill="x", padx=3)
#Creamos un botón de ajustes
photo = (Image.open("assets\\gears.png"))
gears = ImageTk.PhotoImage(photo)
botonAjustes = tk.Button(frame3, image=gears, text="Ajustes", bg=COLOR3, command= lambda: abrirMenuOpciones()) # Crear un botón
botonAjustes.image=gears
botonAjustes.place(relwidth=0.03, relheight=0.8, relx=0.01, rely=0.1) # Posicionar el botón
#Creamos un botón de historial
photo = (Image.open("assets\\history.png"))
history = ImageTk.PhotoImage(photo)
botonHistorial = tk.Button(frame3, image=history, text="Historial", bg=COLOR3, command= lambda: abrirHistorial()) # Crear un botón
botonHistorial.image=history
botonHistorial.place(relwidth=0.03, relheight=0.8, relx=0.05, rely=0.1) # Posicionar el botón
#Creamos un botón de favoritos
photo = (Image.open("assets\\star.png"))
star = ImageTk.PhotoImage(photo)
botonFavoritos = tk.Button(frame3, image=star, text="Favoritos", bg=COLOR3, command= lambda: abrirFavoritos()) # Crear un botón
botonFavoritos.image=star
botonFavoritos.place(relwidth=0.03, relheight=0.8, relx=0.09, rely=0.1) # Posicionar el botón
#Creamos un botón de ayuda
photo = (Image.open("assets\\question.png"))
question = ImageTk.PhotoImage(photo)
botonAyuda = tk.Button(frame3, image=question, text="Ayuda", bg=COLOR3, command= lambda: abrirAyuda()) # Crear un botón
botonAyuda.image=question
botonAyuda.place(relwidth=0.03, relheight=0.8, relx=0.96, rely=0.1) # Posicionar el botón
#Creamos un botón de cambiar colores
photo = (Image.open("assets\\palette.png"))
palette = ImageTk.PhotoImage(photo)
botonColor = tk.Button(frame3, image=palette, text="Color", bg=COLOR3, command= lambda: abrirColores()) # Crear un botón
botonColor.image=palette
botonColor.place(relwidth=0.03, relheight=0.8, relx=0.92, rely=0.1) # Posicionar el botón

#Final
root.mainloop() # Ejecutar la ventana principal