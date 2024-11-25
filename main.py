from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Lista de IDs e seus valores correspondentes
items = [
    {"ID": "148", "VALUE": "Geovanna Emanuelly"},
    {"ID": "154", "VALUE": "Gustavo Inácio"},
    {"ID": "158", "VALUE": "Felipe Marchezine"},
    {"ID": "34874", "VALUE": "Taynara Francine"},
    {"ID": "43180", "VALUE": "Sabrina Emanuelle"},
    {"ID": "48604", "VALUE": "Ian Henrique"},
    {"ID": "48618", "VALUE": "Tiago Martins"},
    {"ID": "48674", "VALUE": "Caio Sales"},
    {"ID": "49718", "VALUE": "Italo Almeida"},
    {"ID": "48678", "VALUE": "Jéssica Hellen"},
    {"ID": "49722", "VALUE": "Laisa Reis"},
    {"ID": "34794", "VALUE": "Treinamento 01"},
    {"ID": "48596", "VALUE": "Treinamento 02"},
    {"ID": "48610", "VALUE": "Treinamento 03"},
    {"ID": "48612", "VALUE": "Treinamento 04"}
]

# Webhook do Bitrix24
webhook_url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"

# Função para atualizar o card no Bitrix24
def update_deal(deal_id, value):
    url = f"{webhook_url}crm.deal.update.json"
    data = {
        "ID": deal_id,
        "FIELDS": {
            "UF_CRM_1732282217": value
        }
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return {"status": "success", "message": f"Card {deal_id} atualizado com sucesso!"}
    else:
        return {"status": "error", "message": f"Erro ao atualizar o card {deal_id}: {response.status_code}"}

# Função para verificar o ID e atualizar o campo
def check_and_update_card(deal_id, uf_value):
    # Verificar se o valor de UF_CRM_1699475211222 corresponde a um dos valores da lista
    for item in items:
        if item["ID"] == uf_value:
            return update_deal(deal_id, item["VALUE"])
    return {"status": "error", "message": "ID não encontrado na lista de valores."}

# Endpoint da API que recebe o ID do card e o valor de UF_CRM_1699475211222
@app.route('/update_card', methods=['POST'])
def update_card():
    # Receber dados do JSON enviado na requisição
    data = request.get_json()
    
    # Validar os campos
    if 'deal_id' not in data or 'uf_value' not in data:
        return jsonify({"status": "error", "message": "Parâmetros 'deal_id' e 'uf_value' são obrigatórios."}), 400

    deal_id = data['deal_id']
    uf_value = str(data['uf_value'])  # Garantir que o valor seja uma string

    # Chamar a função de verificação e atualização
    result = check_and_update_card(deal_id, uf_value)
    
    return jsonify(result)

# Rodar o servidor Flask
if __name__ == "__main__":
    app.run(port=8858, host ='0.0.0.0')
