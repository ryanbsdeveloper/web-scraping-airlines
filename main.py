from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        limite = request.form['preco']
        origem = request.form['origem']
        destino = request.form['destino']
        ida = request.form['ida']
        volta = False
        try:
            somente_ida = request.form['somenteIda']
        except:
            somente_ida = False
            volta = request.form['volta']
        else:
            somente_ida = True

        if not origem or not destino or not ida or not somente_ida and not volta:
            return render_template('index.html', erro='Campos obrigatorios não definidos.')
            
        print(limite, origem, destino, somente_ida, ida, volta)
        return render_template('return.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

