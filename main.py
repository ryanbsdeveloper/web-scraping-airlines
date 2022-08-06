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
        inputs = request.form.to_dict()['form_data']
        preco = inputs[43:47]
        origem = inputs[79:82]
        destino = inputs[115:118]
        data_ida = inputs[147:157]
        data_volta = inputs[188:198]
        if '&#' in data_ida:
            data_ida = data_volta
            data_volta = False

        print(preco, origem, destino, data_ida, data_volta)
        try:
            webscraping.Scraping(origem, destino, data_ida, data_volta)
        except:
            passagens_achadas = 'false'
            
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
            passagens_achadas = 'true'
            initial = [data, origem, origem_estado, destino, destino_estado]

            for value in file.readlines():
                value = value.replace('\n', '')
                if value == '-':
                    passagens_achadas = 'false'
                    break
                if value == '+1':
                    continue
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
                'passagens_achadas': passagens_achadas,
                'ida_e_volta': data_volta, 
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
