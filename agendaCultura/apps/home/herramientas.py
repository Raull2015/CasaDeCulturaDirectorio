# -*- coding: utf-8 -*-
import os
from PIL import Image

def reescalar_imagen(img,output,height=300,width=400,ext='.png'):
    archivo_in, old_ext = os.path.splitext(img)
    archivo_out, new_ext = os.path.splitext(output)
    imagen = Image.open(img)


    old_width, old_height = imagen.size
    #width = int((1.0 * old_width)/old_height * height)
    new_img = imagen.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter

    if new_ext == None:
        new_ext = ext

    new_img.save(archivo_out + new_ext)

    print "Imagen rescalada a ", height , " * ", width

def renombrar_archivo(currentName,newName="archivo"):
    archivo, old_ext = os.path.splitext(currentName)
    return newName + old_ext

def validar_password(username, password, password_confirm):

    car_prohibidos = {'-','_','@',':'}
    for c in car_prohibidos:
        if username.find(c) != -1:
            return False, 'El nombre de usuario no puede tener el caracter' + c

    if len(username) < 4:
        return False, 'El nombre de usuario debe tener almenos 4 caracteres'
    if password != password_confirm:
        return False, 'Las contraseñas no coinciden'
    if len(password) < 8:
        return False, 'La contraseña debe tener almenos 8 caracteres'

    return True, None
