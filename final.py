# -*- coding: utf-8 -*-

# Generates a UTF-8 file with <word> <phones>

import sys

if len(sys.argv) < 3:
  sys.exit(0)

f=open(sys.argv[2],"r")
lines=f.readlines()
f.close()
all_words = []
for word in lines:
   all_words.append(word.strip()) 

phones = []
f=open(sys.argv[1],"r")
lines=f.readlines()
f.close()
for line in lines:
   phones.append(line.strip().split('\t')[1]) 

f=open(sys.argv[1],"w")
for k,v in sorted(dict(zip(all_words,phones)).items()):
   f.write(k+'\t'+v+'\n')
f.close()