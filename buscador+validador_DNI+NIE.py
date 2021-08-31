#! python3
'''
Este programa busca DNI y NIE en un archivo de texto y los analiza para ver si el digito de control
es el que corresponde para las cifras precedentes.
Informacion sobre la comprobacion de validez:
http://www.interior.gob.es/web/servicios-al-ciudadano/dni/calculo-del-digito-de-control-del-nif-nie

Uso en linea de comandos:
py buscador+validador_DNI+NIE.py archivo.txt
Donde "archivo.txt" es el archivo en el que se desea buscar DNI/NIE
'''

import re
import sys

                    #BUSCAR

#Abrir el archivo
textfile = open(sys.argv[1])
text = textfile.read() #read: text file to string

#Crear los patrones
DNIpattern = re.compile(r'\b\d{8}[\- ]{0,1}[A-Za-z]\b')
NIEpattern = re.compile(r'\b[YXZyxz]\d{7}[\- ]{0,1}[A-Za-z]\b')

#Obtener lista de los matches
DNImatches = DNIpattern.findall(text)
NIEmatches = NIEpattern.findall(text)


                    #VALIDAR

#Diccionario con las letras del NIF y el resto al que corresponden
#Los DNI no tienen I, O, U para evitar confusiones (con 1, 0, V)
diccioletrasNIF = {0:'T', 6:'Y', 12:'N', 18:'H',
1:'R', 7:'F', 13:'J', 19:'L',
2:'W', 8:'P', 14:'Z', 20:'C',
3:'A', 9:'D', 15:'S', 21:'K',
4:'G', 10:'X', 16:'Q', 22:'E',
5:'M', 11:'B', 17:'V'}

#Funcion da validacion
def validarNIF(nif):
    letraNIFpattern = re.compile(r'[A-Za-z]$')#Letra del final
    letraNIF = letraNIFpattern.search(nif).group() #group: search object to found object
    
    cifrasNIFpattern = re.compile(r'\d{7,8}')
    cifrasNIF = cifrasNIFpattern.search(nif).group()
    if len(cifrasNIF) == 7: #Esto es un NIE
        pincipioNIEpattern = re.compile(r'\b[YXZyxz]')
        principioNIE = pincipioNIEpattern.search(nif).group()
        if principioNIE.upper() == 'X':
            cifrasNIF = '0' + cifrasNIF
        if principioNIE.upper() == 'Y':
            cifrasNIF = '1' + cifrasNIF
        if principioNIE.upper() == 'Z':
            cifrasNIF = '2' + cifrasNIF
    
    resto = int(cifrasNIF)%23 
    
    if diccioletrasNIF[resto] == letraNIF.upper(): return print('\t\t' + nif + ': correcto')
    else: return print('\t\t' + nif + ': incorrecto')



                    #OUTPUT
print('\n')
print('\t** NIF encontrados y validez **')

print('\n')
if len(DNImatches) > 1: print('\tSe han encontrado estos DNI:')
if len(DNImatches) == 1: print('\tSe ha encontrado este DNI:')
if len(DNImatches) == 0: print('\tNo se han encontrado DNI:')
for DNI in DNImatches: validarNIF(DNI)

print('\n')
if len(NIEmatches) > 1: print('\tSe han encontrado estos NIE:')
if len(NIEmatches) == 1: print('\tSe ha encontrado este NIE:')
if len(NIEmatches) == 0: print('\tNo se han encontrado NIE:')
for NIE in NIEmatches: validarNIF(NIE)


    
