#!/usr/bin/python
# -*- coding: latin-1 -*-
# $Id: mod_ort2fon.py,v 1.1 2013/09/24 10:00:59 cesargf Exp $
######################################################################
# TRANSCRIPTOR ORTOFONETICO
# OCTUBRE-2000
# AUTORES: Andres Marzal
#          Maria Jose Castro
#          Salvador España
#          Ismael Salvador
######################################################################

######################################################################
# IMPORTACION DE LIBRERIAS
######################################################################
from string import *
import re
sub = re.sub
match = re.match
import sys

######################################################################
# VERSION
######################################################################
version = '1.1'

######################################################################
# variables globales, booleanas:
######################################################################
por_palabras = 0
multiple = 0
relajacion = 0

######################################################################
# algunas transformaciones previas
######################################################################

# las vocales acentuadas se denotan utilizando mayusculas
tabla_tildes = maketrans('áéíóúÁÉÍÓÚ',
                         'AEIOUAEIOU')

# Los signos de puntuacion finales y otras pausas son pausas (.)
tabla_signos = maketrans('?!,;:><_',
                         '.....   ')

# la funcion lower no funciona con los simbolos 'Ñ' y 'Ü'
tabla_lower = maketrans('ÑÜ',
                        'ñü')

def trans_normort(linea):
    # es suficiente una sola sentencia si se amplia tabla_lower
    linea = lower(linea)
    linea = translate(linea,tabla_lower)

    linea = replace(linea,'~n','ñ')
    linea = translate(linea,tabla_tildes)
    linea = translate(linea,tabla_signos)
    # Las pausas son palabras
    linea = replace(linea,'.',' . ')
    # Fundir cadenas de blancos
    linea = sub('(\s)+',' ',' '+linea+' ')
    return linea



######################################################################
#
#                         A C E N T U A D O R
#
######################################################################

#subrutina que cuenta vocales
def esvocal(letra):
    return letra in 'aeiouAEIOU'

def numVocales(texto):
    return len(filter(esvocal,texto))

def yaLlevaAcento(texto):
    for letra in texto:
        if (letra in 'AEIOU'):
            return 1
    return 0

def acento_pos(palabra,pos):
    i = len(palabra)-1
    p = pos
    while (i >= 0):
        if (palabra[i] in 'aeiou'):
            # caso vocal fuerte + vocal debil, cuenta la fuerte
            if ((i > 0) and (palabra[i] in 'iu') and (palabra[i-1] in 'aeo')):
                # nos saltamos la ultima, que es la fuerte
                i = i-1
            if (p == 1):
                return palabra[0:i]+capitalize(palabra[i])+palabra[i+1:]
            else:
                p = p-1
                # caso vocal debil seguida de otra vocal cualquiera sea
                # esta debil o fuerte, ambos casos son diptongo
                if ((i>0) and palabra[i-1] in 'iu'):
                    i = i-1
        i = i-1
    return palabra

# Eliminar acentos
quita_acentos = maketrans('AEIOU','aeiou')

def acentua_rec(palabra):
    palabra = strip(palabra)
    # las monosílabas se acentuan acusticamente?
    if (numVocales(palabra) <= 1):
        return translate(palabra,quita_acentos)

    # las palabras que terminan por "mente" se acentuan sin
    # considerar ese sufijo
    er = match('(.+)mente$',palabra)
    if (er != None):
        return acentua_rec(er.group(1))+'mEnte'

    # si lleva acento me la paso
    if yaLlevaAcento(palabra):
        return palabra

    # acentuo agudas que no acaben en vocal, n, s
    if not(palabra[-1] in 'aeiouns'):
        return acento_pos(palabra,1)

    #acentuo llanas
    return acento_pos(palabra,2)

def pon_cosas(palabra):
    palabra = replace(palabra,'que','Qe')
    palabra = replace(palabra,'qui','Qi')
    palabra = replace(palabra,'gue','Ge')
    palabra = replace(palabra,'gui','Gi')
    return palabra

def quita_cosas(palabra):
    palabra = replace(palabra,'Q','qu')
    palabra = replace(palabra,'G','gu')
    return palabra

def acentua(palabra):
    #quito la consonante artificial
    return quita_cosas(acentua_rec(pon_cosas(palabra)))

######################################################################
#
# T R A N S C R I P T O R
#
# REFERENCIA: A. Quilis y J.A. Fernandez
#             "Curso de fonetica y fonologia españolas
#             para estudiantes angloamericanos"
#             Ed. Consejo superior de investigaciones cientificas
#             instituto "Miguel de Cervantes"
#             Madrid 1979
######################################################################
def trans_ort2phon(linea):
    # x en posicion intervocalica se pronuncia como 'ks' (Q79:8.6.1)
    # en cualquier otro caso, como 's'
    linea = sub('([aeiouAEIOU])x([aeiouAEIOU])','\g<1>ks\g<2>',linea)
    if multiple:
        # en caso de pronunciacion multiple consideramos sobrepronunciacion
        # si no lo ponemos aqui, no podemos recuperar la informacion
        linea = replace(linea,'x','[k]s')
    else:
        linea = replace(linea,'x','s')
    # a partir de este punto podemos utilizar la 'x' para representar el fonema

    # La 'j' siempre se pronuncia como el fonema 'x' (Q79:8.9.1)
    linea = replace(linea,'j','x')

    # Cuando la 'g' aparece como 'ge' o 'gi' se pronuncia como la letra jota ('x')
    # (Q79:7.6.2,Q79:8.9.1)
    linea = replace(linea,'ge','xe')
    linea = replace(linea,'gE','xE')
    linea = replace(linea,'gi','xi')
    linea = replace(linea,'gI','xI')

    # y los grupos 'gue,gui' no pronuncian la 'u'...
    linea = replace(linea,'gue','ge')
    linea = replace(linea,'guE','gE')
    linea = replace(linea,'gui','gi')
    linea = replace(linea,'guI','gI')

    # ...excepto si hay dieresis
    linea = replace(linea,'ü','u')

    # si en el diptongo 'ue' la 'u' es el primer fonema prenuclear de la silaba,
    # aparece siempre delante el sonido 'g' (Q79:8.9.2)
    linea = replace(linea,'hue','gue')
    linea = replace(linea,'huE','guE')
    linea = replace(linea,' ue',' gue')
    linea = replace(linea,' uE',' guE')

    # La 'w' se pronuncia como 'gu'
    linea = replace(linea,'w','gu')

    # La grafia 'qu' se pronuncia como 'k' (Q79:7.6.1)
    linea = replace(linea,'que','ke')
    linea = replace(linea,'quE','kE')
    linea = replace(linea,'qui','ki')
    linea = replace(linea,'quI','kI')

    # La grafia 'hi' en posicion inicial de palabra se pronuncia 'y' (Q79:8.8)
    linea = sub('( hi)([aeiouAEIOU])',' y\g<2>',linea)

    # ahora que ya nos hemos ocupado de los grafemas 'w' y 'j' podemos utilizarlos
    # para denotar las semiconsonantes.
    # En los diptongos crecientes, la vocal mas cerrada
    # recibe el nombre de semiconsonantes (Q79:6.2.1)
    linea = sub('i([aeouAEOU])','j\g<1>',linea)
    linea = sub('u([aeioAEIO])','w\g<1>',linea)

    # y al aparecer al final de palabra se realiza como 'i' (Q79:6.2)
    # Tambien como conjuncion se pronuncia como 'i'
    linea = replace(linea,'y ','i ')

    # Entre consonantes o tras consonante al final de palabras se suele leer i
    # (anglicismos como 'curry')
    linea = sub('([^aeiouAEIOUjw])(y)([^aeiouAEIOUjw])','\g<1>i\g<3>',linea)

    # La 'c' delante de 'e' e 'i' se pronuncia 'z' (Q79:8.5.1)
    linea = replace(linea,'ce','ze')
    linea = replace(linea,'cE','zE')
    linea = replace(linea,'ci','zi')
    linea = replace(linea,'cI','zI')
    linea = replace(linea,'cj','zj')

    # La 'c'cuando no es 'ch', es una 'k'(Q79:7.6.1)
    linea = sub('(c)([^h])','k\g<2>',linea)

    # La 'ch' es representada foneticamente por 'c' (Q79:9.3)
    linea = replace(linea,'ch','c')

    # La 'h' en castellano es muda. Su aparicion en otros contexto (huevo, che)
    # es tratada en otras reglas anteriores
    linea = replace(linea,'h','')

    # La "ll" pronuncia como el fonema 'H' (Q79:11.2.2)
    linea = replace(linea,'ll','H')

    # Antes de 'b' o 'v' se pronuncia 'm' (Q79:7.3.2)
    linea = sub('n( ?[bv])','m\g<1>',linea)

    # La 'ñ' siempre se pronuncia como el fonema 'h' (Q79:10.6)
    linea = replace(linea,'ñ','h')

    # La particula 'ps' a principio de palabra se pronuncia 's'
    # pero tambien se puede pronunciar 'ps', lo ponemos opcional
    if multiple:
        linea = replace(linea,' ps',' [p]s')
    else:
        linea = replace(linea,' ps',' s')

    # La doble 'r' es una vibrante multiple '@'
    linea = replace(linea,'rr','@')

    # A principio de palabra, la 'r' se pronuncia como si fuera doble ('@')
    # Tras 'n', 'l' o 's', tambien se pronuncia como 'r' doble (Q79:11.3.3)
    # (Q79:11.3.3)
    linea = sub('([ nls])(r)','\g<1>@',linea)

    # En castellano la 'v' se pronuncia siempre como 'b' (Q79:7.3.2)
    linea = replace(linea,'v','b')

    return linea

def concurrencias_intrapal(linea):
    # Si concurren dos nasales lingualveolares, se pronuncia solo una (Q79:13.4.2)
    linea = sub('(n+)','n',linea)

    # Concurrencia de vocales en una misma palabra
    linea = sub('(a+)','a',linea)
    linea = sub('((aA)|(AA)|(Aa))','A',linea)
    linea = sub('(e+)','e',linea)
    linea = sub('((eE)|(EE)|(Ee))','E',linea)
    linea = sub('(i+)','i',linea)
    linea = sub('((iI)|(II)|(Ii))','I',linea)
    linea = sub('(o+)','o',linea)
    linea = sub('((oO)|(OO)|(Oo))','O',linea)
    linea = sub('(u+)','u',linea)
    linea = sub('((uU)|(UU)|(Uu))','U',linea)
    return linea

# expresion regular para tratar la concurrencia de vocales entre palabras
concurrvoc = re.compile(
    '(?P<prim>.*?)(?P<vocs>'+
    '([aA] [aA])|([eE] [eE])|([iI] [iI])|([oO] [oO])|([uU] [uU]))'+
    '(?P<ult>.*)$')

def concurrencias_interpal(linea):
    # Concurrencia de vocales en palabras distintas
    if multiple:
        er = concurrvoc.match(linea)
        while (er != None):
            voc1 = er.group('vocs')[0]
            voc2 = er.group('vocs')[2]
            if voc1 == lower(voc1): # si es minuscula
                # ej casos 'a a' -> [a,]a y 'a A' -> [a,]A
                trozo = '[%c,]%c' % (voc1,voc2)
            else:
                # ej casos 'A a' -> A[,a] y 'A A' -> A[,A]
                trozo = '%c[,%c]' % (voc1,voc2)
            linea = er.group('prim') + trozo + er.group('ult')
            er = concurrvoc.match(linea)
    else:
        er = concurrvoc.match(linea)
        while (er != None):
            voc1 = er.group('vocs')[0]
            voc2 = er.group('vocs')[2]
            if (voc1 == upper(voc1)) or (voc2 == upper(voc2)):
                trozo = upper(voc1)
            else:
                trozo = voc1
            linea = er.group('prim') + trozo + er.group('ult')
            er = concurrvoc.match(linea)

    # Si concurren dos nasales lingualveolares, se pronuncia solo una (Q79:13.4.2)
    if multiple:
        linea = replace(linea,'n n','n[,n]')
    else:
        linea = replace(linea,'n n','n')

    # Si concurren dos laterales linguoalveolares, solo se pronuncia una lateral
    # (Q79:13.4.2)
    if multiple:
        linea = replace(linea,'l l','l[,l]')
    else:
        linea = replace(linea,'l l','l')

    # Si concurre la 'd' con otra linguodental, se pronuncia solo una (Q79:13.4.2)
    if multiple:
        linea = replace(linea,'d d','d[,d]')
    else:
        linea = replace(linea,'d d','d')

    # Si concurre una 'r' con una vibrante multiple, se pronuncia solo esta ultima
    # (Q79:13.4.2)
    if multiple:
        linea = replace(linea,'r @','[r,]@')
    else:
        linea = replace(linea,'r @','@')

    # Si concurren dos fricativas linguoalveolares sordas, se pronuncia solo una
    # (Q79:13.4.2)
    if multiple:
        linea = replace(linea,'s s','s[,s]')
    else:
        linea = replace(linea,'s s','s')

    return linea

def trans_relajacion(linea):
    # Cuando el fonema r precede al s se suele perder (Q79:8.7) ej "israel"
    if multiple :
        linea = replace(linea,'s@','[s]@')
    else:
        linea = replace(linea,'s@','@')

    # (Q79:10.4.2) ej "conmover"
    if multiple :
        linea = replace(linea,'nm','[n]m')
    else:
        linea = replace(linea,'nm','m')

    # si el fonema 'n' aparece ante una consonante labiodental fricativa
    # sorda ('f') se relaja como 'm' (Q79:10.4.3) ej "confundir"
    if multiple :
        linea = replace(linea,'nf','(n|m)f')
    else:
        linea = replace(linea,'nf','mf')

    if multiple :
        linea = replace(linea,'ks','[(k|g)]s')
        linea = replace(linea,'[k]s','[(k|g)]s')

    # (Q79:7.8) Fonemas oclusivos en posicion silabica implosiva
    if multiple :
        linea = sub('([aeiouAEIOU])p([^rlaeiouAEIOUjw .])',
                    '\g<1>[(p|b)]\g<2>',linea)
        linea = sub('([aeiouAEIOU])t([^rlaeiouAEIOUjw .])',
                    '\g<1>[(t|d)]\g<2>',linea)
        linea = sub('([aeiouAEIOU])k([^rlaeiouAEIOUjw .])',
                    '\g<1>[(k|g)]\g<2>',linea)
        linea = sub('([aeiouAEIOU])b([^rlaeiouAEIOUjw .])',
                    '\g<1>[(b|p)]\g<2>',linea)
        linea = sub('([aeiouAEIOU])d([^raeiouAEIOUjw .])',
                    '\g<1>[(d|t)]\g<2>',linea)
        linea = sub('([aeiouAEIOU])g([^rlaeiouAEIOUjw .])',
                    '\g<1>[(g|k)]\g<2>',linea)

    # (Q79:11.3.4) ej "arpon"
    if multiple:
        linea = sub('([aeiouAEIOU])r([^aeiouAEIOUjw .])',
                    '\g<1>(r|@)\g<2>',linea)

    return linea

def pron_multiple(linea):
    # yeismo (Q79:11.2.2.2)
    linea = replace(linea,'H','(H|<1>y)')

    linea = replace(linea,' el a',' (el |l)a')
    linea = replace(linea,' el A',' (el |l)A')
    linea = replace(linea,'z','(z|<4>s)')
    linea = replace(linea,'Ado ','A[<3>d]o ')
    linea = replace(linea,'Ada ','A[<3>da] ')
    linea = replace(linea,'er ','e[<3>r] ')
    linea = replace(linea,'ar ','a[<3>r] ')
    linea = replace(linea,'Ar ','A[<3>r] ')
    linea = replace(linea,'Er ','E[<3>r] ')
    linea = sub('([AEOUjw])([iu])s([ .])','\g<1>\g<2>[<mr>s]\g<3>',linea)
    linea = sub('([AEIOU])d([ .])','\g<1>[(d|t|z)]\g<2>',linea)
    return linea

def tratar_pausas(linea,porpalabras):
    linea = strip(linea)
    if multiple:
        linea = sub(' *\.[ \.]*','.',linea)
        linea = replace(linea,'.','[<pe>.]')
        linea = replace(linea,' ','[.]')
        # linea = sub('\.+','.',linea)
        # linea = replace(linea,'.','[.]')
    else:
        if not porpalabras:
            linea = replace(linea,' ','')
        linea = sub('\.+','<pe>.',linea)
    linea = replace(linea,',','.')
    return linea

######################################################################
# NOMENCLATURA DE LAS ETIQUETAS
# se usan numeros para evitar que las reglas de sustitucion
# grafema-unidad fonetica actuen sobre las etiquetas
######################################################################
nom_etiquetas = {}
nom_etiquetas['1'] = 'yeismo' # yeismo
nom_etiquetas['2'] = 'pe' # pausa explicita
nom_etiquetas['3'] = 'mr' # mucha relajacion
nom_etiquetas['4'] = 'sso' # seseo

def cambia_etiqueta(item):
    if nom_etiquetas.has_key(item):
        return nom_etiquetas[item]
    else:
        return item

# expresion regular para recuperar el contenido de una etiqueta
lee_etiqueta = re.compile('(?P<prim>.*?)<(?P<etiq>.*?)>(?P<ult>.*)$')

def pon_etiquetas(linea):
    er = lee_etiqueta.match(linea)
    if (er != None):
        etiqs = join(map(cambia_etiqueta,split(er.group('etiq'),':')),':')
        linea = '%s<%s>%s' % (er.group('prim'),etiqs,
                              pon_etiquetas(er.group('ult')))
    return linea

def quita_etiquetas(linea):
    linea = sub('<.*?>','',linea)
    return linea

######################################################################
#                          AYUDA Y VERSION
######################################################################
def muestra_version(nombre_programa):
    print 'Programa',nombre_programa
    print 'Version',version # variable global
    print 'Contacto:'
    print ' Andrés Marzal (e-mail: amarzal@inf.uji.es)'
    print ' María José Castro (e-mail: mcastro@dsic.upv.es)'
    print ' Salvador España (e-mail: sespana@dsic.upv.es)'
    print ' Ismael Salvador (e-mail: issalig@doctor.upv.es)'

def muestra_ayuda(nombre_programa):
    print '* Uso: '+nombre_programa+' [-hvpmrsa]'
    print '   - h muestra este mensaje de ayuda'
    print '   - v muestra informacion sobre la version'
    print '   - p transcripción palabra a palabra'
    print '   - m pronunciaciones múltiples'
    print '   - r relajación'
    print '   - e etiquetas'
    print '  Las opciones por defecto son frase a frase, sin pronunciaciones'
    print '  multiples, sin relajacion y sin etiquetas.'
    print '* Conjunto de unidades: .ptkbdgmnhfzsxyclHr@ieaouAEIOUjw'
    print '* Notación para las pronunciaciones múltiples:'
    print '   - Los corchetes "[]" denotan que el interior es opcional'
    print '     Ejemplo: abogA[da] -> abogAda, abogA'
    print '   - Las alternativas excluyentes se denotan "(op1|...|opn)"'
    print '     Ejemplo: (z|s)apato -> zapato, sapato'
    print '* Se ha intentado que la primera opción y la inclusión de la'
    print '  parte opcional den la pronunciación considerada estándar.'
    print '* Algunas relajaciones sólo aparecen con la opcion de'
    print '  pronunciaciones multiples.'
    print '* Notacion para las etiquetas: Vienen entre simbolos "<>"'
    print '  separadas por ":" si hay mas de una. Sirven para dar'
    print '  información complementaria sobre el simbolo que preceden.'
    print '  Ej. "no, he dicho que no" pasaria a "no[<pe>.]e[.]dIco[.]ke[.]no"'
    print '  donde <pe> indicaria "pausa explícita".'

######################################################################
#                           PROGRAMA PRINCIPAL
######################################################################

paramentrada = sys.argv
if len(sys.argv) > 1:
    opciones = sys.argv[1]
else:
    opciones = ''

if ('h' in opciones):
    muestra_ayuda(sys.argv[0])
    sys.exit()

if ('v' in opciones):
    muestra_version(sys.argv[0])
    sys.exit()

por_palabras = ('p' in opciones)
multiple = ('m' in opciones)
relajacion = ('r' in opciones)
etiquetas = ('e' in opciones)

# procesamos linea a linea la entrada estandar
# y lo enviamos a la salida estandar
fin = sys.stdin
fout = sys.stdout
l = fin.readline()
while l != '':
    # le quito el \n del final de la linea
    l = replace(l,'\n','')
    l = trans_normort(l)
    # acentuo palabra por palabra
    l = join(map(acentua,split(l)))

    l = trans_ort2phon(' '+l+' ')

    if relajacion:
        l = trans_relajacion(l)

    # concurrencias entre palabras
    if not por_palabras:
        l = concurrencias_interpal(l)

    if multiple:
        l = pron_multiple(l)

    # concurrencias en la misma palabra
    l = concurrencias_intrapal(l)

    # ponemos las pausas como toca:
    l = tratar_pausas(l,por_palabras)

    if etiquetas:
        l = pon_etiquetas(l)
    else:
        l = quita_etiquetas(l)

    fout.write('%s\n' % (strip(l),))
    l = fin.readline()

