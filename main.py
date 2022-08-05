import linecache
from time import sleep
from flask import Flask, request
from flask import render_template, make_response
from services import webscraping
app = Flask(__name__)

@app.route('/', methods=['POST'])
def loading():
    if request.method == 'POST':
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
            return render_template('index.html', erro='Campo obrigatorio não definido.')
        
        return render_template('return.html', form_data=request.form)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/passagens', methods=['GET', 'POST'])
def passagens():
    if request.method == 'GET':
        return render_template('tickets.html')

    webscraping.Scraping('GRU', 'SSA', '2022-08-05')
    with open('aires.txt', 'r') as file:
        voos = []
        precos = []
        dados = []
        temp = []

        ida_ou_volta = linecache.getline('aires.txt', 1).replace('\n','')
        data = linecache.getline('aires.txt', 2).replace('\n','')
        origem = linecache.getline('aires.txt', 3).replace('\n','')
        origem_estado = linecache.getline('aires.txt', 4).replace('\n','')
        destino = linecache.getline('aires.txt', 5).replace('\n','')
        destino_estado = linecache.getline('aires.txt', 6).replace('\n','')
        initial = [data, origem, origem_estado, destino, destino_estado]

        for c, value in enumerate(file.readlines()):
            value = value.replace('\n', '')
            if value not in initial:
                if '***' not in value:
                    temp.append(value)
                else:
                    dados.append(temp.copy())
                    temp.clear()

        for v in dados:
            print(v)     

    return render_template('tickets.html')

if __name__ == '__main__':
    app.run(debug=True)
