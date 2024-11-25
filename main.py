import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Função para buscar os responsáveis do campo UF_CRM_1699475211222 de um deal
def get_responsaveis(deal_id):
    try:
        # URL para obter os campos do CRM
        url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.fields"
        
        # Fazendo a requisição para pegar os dados do campo UF_CRM_1699475211222
        response = requests.get(url)
        data = response.json()

        # Verifica se o campo UF_CRM_1699475211222 existe na resposta
        if "result" in data and "UF_CRM_1699475211222" in data["result"]:
            responsaveis = data["result"]["UF_CRM_1699475211222"].get("items", [])
        else:
            print("Campo UF_CRM_1699475211222 não encontrado na resposta")
            return []

        # Buscar os valores do campo UF_CRM_1699475211222 para o deal_id
        deal_url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.get"
        deal_params = {"ID": deal_id}
        deal_response = requests.get(deal_url, params=deal_params)
        deal_data = deal_response.json()

        # Pegando os responsáveis do campo UF_CRM_1699475211222 do negócio
        responsaveis_selecionados = deal_data.get("result", {}).get("UF_CRM_1699475211222", [])

        # Filtra os valores que estão selecionados para o deal_id
        nomes_selecionados = [
            responsavel["VALUE"] 
            for responsavel in responsaveis 
            if responsavel["ID"] in responsaveis_selecionados
        ]
        
        return nomes_selecionados
    except Exception as e:
        print("Erro ao obter responsáveis:", e)
        return []

# Função para atualizar o campo UF_CRM_1732282217 com os nomes dos responsáveis
def update_deal_field(deal_id, nomes):
    try:
        # URL para atualizar o campo
        update_url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.update"
        
        # Dados para a atualização
        update_data = {
            "ID": deal_id,
            "UF_CRM_1732282217": ", ".join(nomes)  # Juntando os nomes selecionados em uma string
        }

        # Debug: Exibe os dados que serão enviados para atualizar o deal
        print("Atualizando deal com dados:", update_data)
        
        # Fazendo a requisição para atualizar o deal
        response = requests.post(update_url, data=update_data)

        if response.status_code == 200:
            return response.json()
        else:
            print("Erro ao atualizar o deal:", response.text)
            return {"error": "Erro ao atualizar o deal"}
    except Exception as e:
        print("Erro ao atualizar o campo:", e)
        return {"error": "Erro ao atualizar o campo"}

# Rota para atualizar os responsáveis de um deal
@app.route('/atualizar-responsaveis', methods=['POST'])
def atualizar_responsaveis():
    deal_id = request.args.get('deal_id')
    
    if not deal_id:
        return jsonify({"error": "deal_id é necessário"}), 400
    
    try:
        # Pega os responsáveis do campo UF_CRM_1699475211222 para o deal específico
        nomes = get_responsaveis(deal_id)

        # Se não houver nomes, retorna um erro
        if not nomes:
            return jsonify({"error": "Nenhum responsável encontrado para o deal"}), 404

        # Atualiza o campo 'UF_CRM_1732282217' do negócio com os nomes dos responsáveis
        result = update_deal_field(deal_id, nomes)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8858)
