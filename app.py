from flask import Flask, render_template, request
from pymongo import MongoClient
import datetime


app = Flask(__name__)

@app.route('/')
def hello():
    name = "yuji"
    return render_template('top.html', title='TOP画面', name=name)

@app.route('/oview', methods=['POST'])
def test():
    '''
    if request.method == 'GET':
        res = request.args.get('get_value')
    elif request.method == 'POST':
        res = request.form['post_value']
    '''

    #top画面で選択したrisk種別を選択
    risklabel = request.form['risks']

    #mongoDBへ接続
    client = MongoClient('localhost', 27017)
    db = client.bldatadb

    #top画面で選択したrisk種別の場合の、クラスごとのリスク度を算出
    pipe = [{'$match':{'risklabel':risklabel}},{'$group':{'_id':'$classs','total': { '$sum': '$value'}}}]    
    agg = db.bldata.aggregate(pipeline = pipe)
    riskvalues = {}
    for r in agg:
        riskvalues[r['_id']] = r['total']
    riskA = riskvalues["A"]
    riskB = riskvalues["B"]
    riskC = riskvalues["C"]
    return render_template('oview.html', title='リスク概要画面',riskA = riskA,riskB = riskB,riskC = riskC)

if __name__ == "__main__":
    app.run(debug=True)