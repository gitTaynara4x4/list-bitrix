from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Função para pegar os responsáveis
def get_responsaveis():
    url = 'https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.fields'
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Requisição GET para pegar os responsáveis (UF_CRM_1699475211222)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        responsaveis_field = data.get('result', {}).get('UF_CRM_1699475211222', {}).get('items', [])
        
        # Extraindo os nomes dos responsáveis
        nomes = [item['VALUE'] for item in responsaveis_field]
        return nomes
    else:
        raise Exception(f"Erro ao buscar responsáveis: {response.status_code} - {response.text}")

# Função para atualizar o campo do negócio
def update_deal_field(deal_id, nomes):
    url = f'https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.update.json'
    
    # Dados para atualizar o campo 'UF_CRM_1732282217' com os nomes dos responsáveis
    data = {
        'ID': deal_id,
        'FIELDS': {
            'UF_CRM_1732282217': ', '.join(nomes)
        }
    }
    
    # Requisição POST para atualizar o negócio
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao atualizar o negócio: {response.status_code} - {response.text}")

@app.route('/atualizar-responsaveis', methods=['POST'])
def atualizar_responsaveis():
    # Pegando o parâmetro deal_id da query string
    deal_id = request.args.get('deal_id')
    
    # Verificar se o deal_id foi passado na URL
    if not deal_id:
        return jsonify({"error": "deal_id é necessário"}), 400
    
    try:
        # Pega os responsáveis
        nomes = get_responsaveis()

        # Atualiza o campo 'UF_CRM_1732282217' do negócio
        result = update_deal_field(deal_id, nomes)

        return jsonify(result)
    except Exception as e:
        # Caso ocorra algum erro nas funções de buscar ou atualizar, retorna o erro
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8858)
