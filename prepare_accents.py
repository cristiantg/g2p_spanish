# -*- coding: utf-8 -*-

# Replaces all Spanish "tildes" from a UTF-8 file by: 'vowel

import sys, io

if len(sys.argv) < 4:
    print 'original_input_utf8.txt output_utf8.txt remove_tildes(1:YES 0:NO)'
    sys.exit(0)

remove_tildes = int(sys.argv[3])==1

tildes = {"á".decode('utf-8'):"'a", "é".decode('utf-8'):"'e", "í".decode('utf-8'):"'i", "ó".decode('utf-8'):"'o", "ú".decode('utf-8'):"'u", "Á".decode('utf-8'):"'A", "É".decode('utf-8'):"'E", "Í".decode('utf-8'):"'I", "Ó".decode('utf-8'):"'O", "Ú".decode('utf-8'):"'U"}

f=io.open(sys.argv[1],"r", encoding='utf-8')
lines=f.readlines()
f.close()

f=io.open(sys.argv[2],"w", encoding='utf-8')
for word in lines:
    aux = ''
    for symbol in word.strip():
        if remove_tildes and (symbol in tildes):
            aux=aux+tildes[symbol]
        else:
            aux=aux+symbol
    f.write(aux+'\n')
f.close()
