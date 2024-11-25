import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de IDs e valores que queremos verificar
responsaveis_validos = {
    "148": "Geovanna Emanuelly",
    "154": "Gustavo Inácio",
    "158": "Felipe Marchezine",
    "34874": "Taynara Francine",
    "43180": "Sabrina Emanuelle",
    "48604": "Ian Henrique",
    "48618": "Tiago Martins",
    "48674": "Caio Sales",
    "49718": "Italo Almeida",
    "48678": "Jéssica Hellen",
    "49722": "Laisa Reis",
    "34794": "Treinamento 01",
    "48596": "Treinamento 02",
    "48610": "Treinamento 03",
    "48612": "Treinamento 04"
}

# Função para pegar o campo UF_CRM_1699475211222 do deal
def get_responsaveis(deal_id):
    try:
        # URL para pegar os detalhes do deal
        deal_url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.get"
        deal_params = {"ID": deal_id}
        deal_response = requests.get(deal_url, params=deal_params)
        deal_data = deal_response.json()

        # Pega os IDs do campo UF_CRM_1699475211222 no deal
        responsaveis_selecionados = deal_data.get("result", {}).get("UF_CRM_1699475211222", [])

        # Filtra os responsáveis válidos (IDs que estão na lista de responsáveis válidos)
        nomes_selecionados = [
            responsaveis_validos[str(id_)] 
            for id_ in responsaveis_selecionados 
            if str(id_) in responsaveis_validos
        ]
        
        return nomes_selecionados
    except Exception as e:
        print("Erro ao obter responsáveis:", e)
        return []

# Função para atualizar o campo UF_CRM_1732282217 com os nomes dos responsáveis
def update_deal_field(deal_id, nomes):
    try:
        # URL para atualizar o campo no deal
        update_url = f"https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/crm.deal.update"
        
        # Dados para atualizar o campo UF_CRM_1732282217
        update_data = {
            "ID": deal_id,
            "UF_CRM_1732282217": ", ".join(nomes)  # Junta os nomes em uma string separada por vírgulas
        }

        # Debug: Exibe os dados que serão enviados para atualizar o deal
        print("Atualizando deal com dados:", update_data)
        
        # Faz a requisição para atualizar o deal
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
            return jsonify({"error": "Nenhum responsável válido encontrado para o deal"}), 404

        # Atualiza o campo 'UF_CRM_1732282217' do negócio com os nomes dos responsáveis
        result = update_deal_field(deal_id, nomes)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8858)
