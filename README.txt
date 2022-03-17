# g2p_spanish
### A grapheme to phoneme (G2P) tool for Spanish

---

To use it, simply:

1. Just for one time: `cd g2p_spanish && chmod -R 744 ./*`
3. Create a UTF-8 file with **one word per line**: `nano original.txt`
4. `./doPron.sh original.txt lexicon 1`

The final file will be encoded in UTF-8 **lexicon.pron**.
*Note*: the third parameter takes into account the differences in áéíóúÁÉÍÓÚ for the phonemes (value=1). Otherwise you can just keep value=0.


---

### Requires
Python2, Linux


### Credits
1. Transcriptor ortofonético: Andres Marzal, Maria Jose Castro, Salvador España and Ismael Salvador
2. Source codebase: César González Ferreras


### Contact
Cristian Tejedor-García
Email: cristian [dot] tejedorgarcia [at] ru [dot] nl
