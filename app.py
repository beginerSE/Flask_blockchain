from flask import Flask, jsonify, request
from hashlib import sha256
import requests

#genesis_blockの雛形を作ります。計算が必要はハッシュ値などは後述
genesis_block = {'no' : 0, 'transaction' : ['this is genesis block, from paiza'], 'nonce' : '', \
                 'prev_hash' : 'NONE', 'hash' : '', 'diff' : 2, 'unixtime' : 1537247368} 

#blockの情報のうちhash値を計算するために使う値を文字列結合します。
genesis_block_str = str(genesis_block['no']) \
                     + ",".join(genesis_block['transaction']) \
                     + str(genesis_block['nonce']) \
                     + genesis_block['prev_hash'] \
                     + str(genesis_block['unixtime'])

#ハッシュ値化
genesis_block_byte = genesis_block_str.encode('utf-8')
genesis_block_hash = sha256(genesis_block_byte).hexdigest()
genesis_block['hash'] = genesis_block_hash

app = Flask(__name__)
block_chain = []
block_chain.append(genesis_block)
nodes = []
pool = []

@app.route('/add_transaction', methods=['GET'])
def add_transaction():
    transaction = request.args.get('transaction')
    pool.append(transaction)
    return jsonify(pool)

@app.route('/get_pool', methods=['GET'])
def get_pool():
    return jsonify(pool)

@app.route('/remove_pool', methods=['GET'])
def remove_pool():
    transaction = request.args.get('transaction')
    pool.remove(transaction)
    return jsonify(pool)

@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify(block_chain[-1])

@app.route('/get_block', methods=['GET'])
def get_block():
    no = request.args.get('no')
    if no and len(block_chain) > int(no):
        block = block_chain[int(no)]
    else:
        block = {}
    return jsonify(block)


