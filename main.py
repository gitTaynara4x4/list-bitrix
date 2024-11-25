from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Função para obter os dados do campo 'UF_CRM_1699475211222'
def get_responsaveis():
    url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.fields"
    response = requests.get(url)
    data = response.json()

    # Extrai os valores (nomes) do campo 'UF_CRM_1699475211222'
    campo_lista = data['result']['UF_CRM_1699475211222']['items']
    nomes = [item['VALUE'] for item in campo_lista]
    
    return nomes

# Função para atualizar o campo 'UF_CRM_1732282217' de um negócio específico
def update_deal_field(deal_id, nomes):
    # URL para atualizar o campo do negócio
    update_url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.update"

    update_data = {
        "id": deal_id,
        "fields": {
            "UF_CRM_1732282217": nomes  # Atualizando com os nomes extraídos
        }
    }

    # Faz a requisição POST para atualizar o campo
    response_update = requests.post(update_url, data=update_data)
    return response_update.json()

# Rota para pegar e atualizar os dados
@app.route('/atualizar-responsaveis', methods=['POST'])
def atualizar_responsaveis():
    # Obtém os dados enviados na requisição
    data = request.json
    deal_id = data.get('deal_id')

    if not deal_id:
        return jsonify({"error": "deal_id é necessário"}), 400

    try:
        # Pega os responsáveis do campo 'UF_CRM_1699475211222'
        nomes = get_responsaveis()

        # Atualiza o campo 'UF_CRM_1732282217' do negócio
        result = update_deal_field(deal_id, nomes)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota principal (para testar se a API está funcionando)
@app.route('/')
def index():
    return jsonify({"message": "API para atualizar campos do Bitrix24."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)