from flask import Flask, render_template, request,session
from pymongo import MongoClient
import datetime

app = Flask(__name__)
app.secret_key = 'session'

@app.route('/')
def hello():
    name = "yuji"
    return render_template('top.html', title='TOP画面', name=name)

@app.route('/oview', methods=['POST'])
def oview():
    #top画面で選択したrisk種別を選択
    risklabel = request.form['risks']

    #セッションに選択したrisk種別を保存
    session['risks'] = risklabel

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

@app.route('/dview', methods=['POST'])
def dview():
    #oview画面で選択したクラス名を選択
    classs = request.form['classs']
    risklabel = session.get('risks')

    #mongoDBへ接続
    client = MongoClient('localhost', 27017)
    db = client.bldatadb

    #top画面で選択したrisk種別の場合の、クラスごとのリスク度を算出
    pipe = [{'$match':{'risklabel':risklabel,'classs':classs}},{'$group':{'_id':'$codelabel','count': { '$sum': 1}}}]    
    agg = db.bldata.aggregate(pipeline = pipe)
    node = {} 
    for r in agg:
        node[r['_id']] = r['count']
    node1 = node["node1"]
    node2 = node["node2"]
    node3 = node["node3"]
    return render_template('dview.html', title='リスク詳細画面',node1 = node1,node2 = node2,node3 = node3)

if __name__ == "__main__":
    app.run(debug=True)