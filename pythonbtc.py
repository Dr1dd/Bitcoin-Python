# `pc_transaction.py` example
from bitcoin.rpc import RawProxy

p = RawProxy()

# Alice's transaction ID
txid = input("Įveskite transakcijos id: ")
# First, retrieve the raw transaction in hex
raw_tx = p.getrawtransaction(txid)

# Decode the transaction hex into a JSON object
decoded_tx = p.decoderawtransaction(raw_tx)

# Retrieve each of the outputs from the transaction
sumIn = 0
sumOut = 0
for output in decoded_tx['vin']:
    vinTxId = output['txid']
    raw_vintx = p.getrawtransaction(vinTxId)
    decoded_vintx = p.decoderawtransaction(raw_vintx)
    vin_vout = output['vout']
    for out in decoded_vintx['vout']:
        if(out['n'] == vin_vout):
            sumIn+=out['value']
        
for output in decoded_tx['vout']:
    sumOut+=output['value']

tx_fee = sumIn - sumOut
print("Transakcijos: ", txid, "\nmokestis:")
print(tx_fee, "BTC")