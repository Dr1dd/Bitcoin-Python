# Bitcoin python programos, apskaičiuojančios transakcijos mokestį ir blokų hash'o tikrinimą.

## Transakcijos mokesčio apskaičiavimas:

Patobulinkite programą, kad ji gebėtų apskaičiuotų bet kurios įvestos Bitcoin transakcijos mokestį:

### Kaip gaunamas transakcijos mokestis:

Paimamos Vin viduje esantys txid ir vout elementų reikšmės.

![img](https://imgur.com/QT3kXQo.png)

Gaunama informacija Vin viduje esančios transakcijos, kurios id yra - txid. 
Susumuojamos visos tos txid transakcijos out value reikšmės, kurių n reikšmė sutampa su pradinės transakcijos vin->vout reikšme.

![img](https://imgur.com/fH7VfpZ.png)


### Programa

```
4410c8d14ff9f87ceeed1d65cb58e7c7b2422b2d7529afc675208ce2ce09ed7d
```
mokestis:

![img](https://imgur.com/Y6EpkFt.png)

Programos kodas:

```
from bitcoin.rpc import RawProxy

p = RawProxy()

txid = input("Įveskite transakcijos id: ")
raw_tx = p.getrawtransaction(txid)

decoded_tx = p.decoderawtransaction(raw_tx)

sumIn = 0
sumOut = 0
for output in decoded_tx['vin']: # Vin visos transakcijos
    vinTxId = output['txid']  #paimama input transakcijos id
    raw_vintx = p.getrawtransaction(vinTxId)
    decoded_vintx = p.decoderawtransaction(raw_vintx)
    vin_vout = output['vout'] #gaunama input vout reiksme n
    for out in decoded_vintx['vout']: # gaunamos visos input vout transakcijos
        if(out['n'] == vin_vout): #tikrinama ar gautos input-> output reikšmės n indeksas sutampa su input vout reikšmė
            sumIn+=out['value']
        
for output in decoded_tx['vout']: #sumuojamos output transakcijos
    sumOut+=output['value']

tx_fee = sumIn - sumOut
print("Transakcijos: ", txid, "\nmokestis:")
print(tx_fee, "BTC")
```

## Programa, tikrinanti ar bloko hash'as yra teisingas:

### Kaip tai veikia?

Sudedama visa header informacija į vieną ```string``` tipo kintamąjį.

![img](https://imgur.com/mPepY94.png)

Įvyksta kelios Little endian hex operacijos, kurios "suswappina" kas antrą teksto simbolį su prieš tai buvusiu.

Pats string tipo kintamasis suhash'inamas 2 kartus ```sha256``` tipo hash algoritmu.

Taip pat šis hash'as yra "reversinamas" (apsukamas) tam, kad gautume tinkamą bloko hash formatą (priekyje daug nulių).

Output:

![img](https://imgur.com/1hfPaZ7.png)

```

from bitcoin.rpc import RawProxy
import hashlib
import binascii

i = 0
def swap(c): #swap funkcija vietoj little/big endian
    c = list(c)
    x = 0
    while(x< len(c)-1):
        if(x != len(c)-1):
           c[x], c[x+1] = c[x+1], c[x]
           x += 2
    return ''.join(c)

p = RawProxy()

blockheight = 277316

blockhash = p.getblockhash(blockheight)

block = p.getblock(blockhash) #gaunama reikalinga bloko informacija:
versionHex = block['versionHex']
previousblockhash =block['previousblockhash']
merkleroot = block['merkleroot']
time = hex(block['time'])[-8:]
bits = block['bits']
nonce = block['nonce']
nonce = hex(int(0x100000000)+nonce)[-8:] #nonce paverčiamas į hex formatą atitinkamai

versionHex = str.encode(swap(versionHex)[::-1]) #swappinama ir reversina informaciją. Taip pat paverčia į bit'us. Paverčiama informacija į little endian formatą
previousblockhash = str.encode(swap(previousblockhash)[::-1])
merkleroot = str.encode(swap(merkleroot)[::-1])
time = str.encode(swap(time)[::-1])
bits = str.encode(swap(bits)[::-1])
nonce = str.encode(swap(nonce)[::-1])


header_hex = versionHex+previousblockhash+merkleroot+time+bits+nonce #sudedama bloko informacija
header = binascii.unhexlify(header_hex) #informacija paverčiama į dviejų simbolių hex
hash = hashlib.sha256(hashlib.sha256(header).digest()).digest() #du kartus užhashuojama sha256 formatu
hash = binascii.hexlify(hash) #iš hex 2 digit formato vėl paverčiama į bytes formatą (little endian swappina)
hash = binascii.hexlify(binascii.unhexlify(hash)[::-1]) #vėl pereinama per little endian pavertimą ir reversinamas hash'as
hash = hash.decode('utf-8')

blockheightNext = 277317

blockhashNext = p.getblockhash(blockheightNext)

blockNext = p.getblock(blockhashNext)

if(blockNext['previousblockhash'] == hash):
    print("Hash'ai sutampa !")
    print("Hash: "+hash)
else:
    print("Hash'ai nesutampa")

```
