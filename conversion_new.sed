#
# Convertir la salida de ort2fon a nuestro formato SAMPA
#
# $Id: conversion_new2.sed,v 1.2 2007/01/20 20:02:52 cesargf Exp $

1,$ s/\([A-Za-z@]\)/\1 /g

# vocales tonicas
1,$ s/A/a/g
1,$ s/E/e/g
1,$ s/I/i/g
1,$ s/O/o/g
1,$ s/U/u/g

# semivocales

#1,$ s/j/i/g
#1,$ s/w/u/g


# cuidado --> ordenar bien
1,$ s/z/T/g
1,$ s/@/rr/g
1,$ s/h/J/g
#1,$ s/H/jj/g
1,$ s/H/L/g
1,$ s/c/tS/g
1,$ s/y/jj/g

# nf --> mf
# parece que es la conversion correcta
#1,$ s/n f/m f/g

# q --> k
# palabras en otro idioma
1,$ s/q/k/g




