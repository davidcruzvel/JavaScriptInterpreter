from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk() # vetana principal
compiler.title('JS Interpreter') # titulo de la ventana
file_path = '' # ruta del archivo

def set_file_path(path): # metodo para asignar la ruta del archivo de manera global
    global file_path
    file_path = path

def open_file(): # abrir un archivo
    path = askopenfilename(filetypes=[('JavaScript Files', '*.js')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

def save_as(): # guardar un archivo, si no existe pide guardarlo si no solo lo actualiza
    if file_path == '':
        path = asksaveasfilename(filetypes=[('JavaScript Files', '*.js')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def run(): # ejecutar el codigo
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please, save your code')
        text.pack()
        return
    command = f'python repl.py {file_path}' # comando para ejecutar el codigo
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)

menu_bar = Menu(compiler) # añadir la barra de menu

file_menu = Menu(menu_bar, tearoff=0) # eliminar una serie de puntos que aparecen hasta arriba
file_menu.add_command(label='Open', command=open_file) # añadir la opcion de abrir 
file_menu.add_command(label='Save', command=save_as) # añadir la opcion de guardar
file_menu.add_command(label='Save As', command=save_as) # añadir la opcion de guardar como
file_menu.add_command(label='Exit', command=exit) # añadir la opcion de salir
menu_bar.add_cascade(label='File', menu=file_menu) # añadiendo la opcion File y su submenu con las opciones declaradas arriba

menu_bar.add_cascade(label='Run', command=run) # añadiendo la opcion "Run" para ejecutar el codigo

compiler.config(menu=menu_bar) # añadiendo el menu a la ventana

editor = Text(height=35, width=120) # primer cuadro de la ventana, donde se editar el codigo
editor.pack()

code_output = Text(height=10, width=120) # segundo cuadro de la ventana, donde se muestran los resultados
code_output.pack()

compiler.mainloop() # ejecucion en loop
