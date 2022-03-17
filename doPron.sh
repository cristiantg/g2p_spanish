#!/bin/bash
#
# $Id: doPron.sh,v 1.3 2013/09/30 12:21:24 cesargf Exp $

#
# BE CAREFUL: INPUT FILE MUST BE ENCODED IN LATIN-1
#

if [ $# -lt 3 ]; 
then
  echo "$0 input_file_utf8 output_file remove_tildes(1:YES 0:NO)"
  echo "Example: $0 original_input_utf8.txt lexicon_output 1"
else 

  ORIG=$1
  AUX=$1.aux
  VOCAB=$2
  OUT=$2.pron
  TILDES=$3

  file -i $ORIG
  python2 prepare_accents.py $ORIG $AUX $TILDES

  iconv -f UTF-8 -t ISO-8859-1 $AUX > $VOCAB
  
  sed -f filtro.sed $VOCAB > tmp0.txt
  python2 mod_ort2fon.py -p < tmp0.txt > tmp1.txt;
  
  # Conversion to 23 phonemes
  sed -f conversion_new.sed tmp1.txt > tmp2.txt
    
  paste $VOCAB tmp2.txt > $OUT
  python2 final.py $OUT $ORIG
  file -i $OUT
  # Optional, comment if you want to keep the following files
  rm -f $VOCAB $AUX tmp0.txt tmp1.txt tmp2.txt
  
fi 


