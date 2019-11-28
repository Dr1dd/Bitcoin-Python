
from bitcoin.rpc import RawProxy
import hashlib
import binascii

i = 0
def swap(c):
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

block = p.getblock(blockhash)
versionHex = block['versionHex']
previousblockhash =block['previousblockhash']
merkleroot = block['merkleroot']
time = hex(block['time'])[-8:]
bits = block['bits']
nonce = block['nonce']
nonce = hex(int(0x100000000)+nonce)[-8:]

versionHex = str.encode(swap(versionHex)[::-1])
previousblockhash = str.encode(swap(previousblockhash)[::-1])
merkleroot = str.encode(swap(merkleroot)[::-1])
time = str.encode(swap(time)[::-1])
bits = str.encode(swap(bits)[::-1])
nonce = str.encode(swap(nonce)[::-1])

header_hex = versionHex+previousblockhash+merkleroot+time+bits+nonce
header = binascii.unhexlify(header_hex)
hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
hash = binascii.hexlify(hash)
hash = binascii.hexlify(binascii.unhexlify(hash)[::-1])
hash = hash.decode('utf-8')

blockheightNext = 277317

blockhashNext = p.getblockhash(blockheightNext)

blockNext = p.getblock(blockhashNext)

if(blockNext['previousblockhash'] == hash):
    print("Hash'ai sutampa !")
    print("Hash: "+hash)
else:
    print("Hash'ai nesutampa")
