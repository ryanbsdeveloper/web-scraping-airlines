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


    if request.method == 'POST':
        input_volta = '2022-08-20'
        webscraping.Scraping('CNF', 'GRU', '2022-08-05', input_volta)
        with open('aires.txt', 'r') as file:
            precos = []
            temp = []
            global dados
            dados = []

            data = linecache.getline('aires.txt', 2).replace('\n','')
            data_volta = ''
            origem = linecache.getline('aires.txt', 3).replace('\n','')
            origem_estado = linecache.getline('aires.txt', 4).replace('\n','')
            destino = linecache.getline('aires.txt', 5).replace('\n','')
            destino_estado = linecache.getline('aires.txt', 6).replace('\n','')
            initial = [data, origem, origem_estado, destino, destino_estado]

            for value in file.readlines():
                if value == '+1':
                    continue
                value = value.replace('\n', '')
                if value not in initial:
                    if '***' not in value:
                        if 'R$' in value:
                            precos.append(value.replace('R$', ''))
                        else:
                            if '.' in value:
                                data_volta = value
                            temp.append(value)
                    else:
                        temp.append(precos.copy())
                        dados.append(temp.copy())
                        temp.clear()
                        precos.clear()

            global dados_passagem
            dados_passagem = {
                'ida_e_volta': input_volta, 
                'data_volta': data_volta,
                'data': data,
                'origem': origem,
                'origem_estado': origem_estado,
                'destino': destino,
                'destino_estado': destino_estado,
                'passagens': dados
            }
        return render_template('tickets.html')

    elif request.method == 'GET':
        return render_template('tickets.html', dados=dados_passagem, passagens=dados)

if __name__ == '__main__':
    app.run(debug=True)
