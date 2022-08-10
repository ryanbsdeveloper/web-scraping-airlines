import linecache
from flask import Flask, request
from flask import render_template
from services import webscraping

application = Flask(__name__)

@application.route('/', methods=['POST'])
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


@application.route('/', methods=['GET', 'POST'])
def index():
    try:
        file = open('aires.txt', 'w')
    except Exception as e:
        assert f'Erro ao recriar arquivo.txt, {e}.'
    finally:
        file.close()

    return render_template('index.html')


@application.route('/passagens', methods=['GET', 'POST'])
def passagens():
    if request.method == 'POST':
        try:
            inputs = request.form.to_dict()['form_data']
            preco = inputs[43:47]
            origem = inputs[79:82]
            destino = inputs[115:118]
            data_ida = inputs[147:157]
            data_volta = inputs[188:198]
            if '&#' in data_ida:
                data_ida = data_volta
                data_volta = False
        except:
            passagens_achadas = 'false'

        try:
            webscraping.Scraping(origem, destino, data_ida, data_volta)
        except:
            passagens_achadas = 'false'

        with open('aires.txt', 'r') as file:
            precos = []
            temp = []
            global dados
            dados = []
            try:
                data = linecache.getline('aires.txt', 2).replace('\n','')
                data_volta = ''
                origem = linecache.getline('aires.txt', 3).replace('\n','')
                origem_estado = linecache.getline('aires.txt', 4).replace('\n','')
                destino = linecache.getline('aires.txt', 5).replace('\n','')
                destino_estado = linecache.getline('aires.txt', 6).replace('\n','')
                passagens_achadas = 'true'
                initial = [data, origem, origem_estado, destino, destino_estado]
            except:
                passagens_achadas = 'false'

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
                            valor = value.replace('R$', '').replace('.', '')
                            try:
                                if int(valor) <= int(preco):
                                    precos.append(valor)
                                else:
                                    precos.clear()
                                    temp.clear()
                                    continue
                            except:
                                passagens_achadas = 'false'
                                break
                        else:
                            if '.' in value:
                                data_volta = value
                            temp.append(value)
                    else:
                        temp.append(precos.copy())
                        dados.append(temp.copy())
                        temp.clear()
                        precos.clear()

            with open('aires.txt', 'r') as file:
                if not file.readline():
                    passagens_achadas = 'false'
                try:
                    if not dados[0][0]:
                        passagens_achadas = 'false'
                except:
                    pass
            
            global dados_passagem
            dados_passagem = {
                'passagens_achadas': passagens_achadas,
                'data_volta': data_volta,
                'data': data,
                'origem': origem,
                'origem_estado': origem_estado,
                'destino': destino,
                'destino_estado': destino_estado,
                'passagens': dados
            }

        return render_template('tickets.html', dados=dados_passagem)

    elif request.method == 'GET':
        return render_template('tickets.html', dados=dados_passagem, passagens=dados)


if __name__ == '__main__':
    application.debug = True
    application.run(port=8000)