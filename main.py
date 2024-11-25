from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Função que atualiza o campo de um negócio no Bitrix24
def update_bitrix24_deal(deal_id, responsable_value):
    url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"
    
    # Parâmetros para a requisição para o Bitrix24
    data = {
        "ID": deal_id,
        "fields": {
            "UF_CRM_1732282217": responsable_value
        }
    }
    
    # Fazendo a requisição POST para o webhook do Bitrix24
    response = requests.post(url, json=data)
    
    return response

@app.route('/copy-field', methods=['GET'])
def copy_field():
    # Recebe o ID do negócio e o valor do responsável pela venda da URL
    deal_id = request.args.get('deal_id')
    responsable_value = request.args.get('responsable_value')
    
    # Valida se os parâmetros necessários foram passados
    if not deal_id or not responsable_value:
        return jsonify({"error": "Missing parameters. 'deal_id' and 'responsable_value' are required."}), 400
    
    # Chama a função para atualizar o campo no Bitrix24
    response = update_bitrix24_deal(deal_id, responsable_value)
    
    if response.status_code == 200:
        return jsonify({"success": "Field updated successfully!"}), 200
    else:
        return jsonify({"error": "Failed to update field", "details": response.json()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8858)
