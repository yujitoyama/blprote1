from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/')
def hello():
    name = "yuji"
    return render_template('top.html', title='TOP画面', name=name)

#
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        res = request.args.get('get_value')
    elif request.method == 'POST':
        res = request.form['post_value']

    return res

if __name__ == "__main__":
    app.run(debug=True)