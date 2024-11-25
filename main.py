from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Função que atualiza o campo de um negócio no Bitrix24
def update_bitrix24_deal(deal_id, responsable_value):
    url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"
    
    # Dados para enviar para o Bitrix24
    data = {
        "ID": deal_id,
        "fields": {
            "UF_CRM_1732282217": responsable_value
        }
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Response from Bitrix24: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            return response.json()
        else:
            return None, response.status_code, response.text
    
    except Exception as e:
        return None, 500, str(e)

@app.route('/copy-field', methods=['POST'])
def copy_field():
    # Obtém o ID do negócio e o valor do responsável do corpo da requisição POST
    data = request.get_json()
    
    deal_id = data.get('deal_id')
    responsable_value = data.get('responsable_value')
    
    # Verifica se os parâmetros estão presentes no corpo da requisição
    if not deal_id or not responsable_value:
        return jsonify({"error": "Missing parameters. 'deal_id' and 'responsable_value' are required."}), 400
    
    # Chama a função para atualizar o campo no Bitrix24
    updated_data, status_code, error_message = update_bitrix24_deal(deal_id, responsable_value)
    
    if updated_data:
        return jsonify({"success": "Field updated successfully!"}), 200
    else:
        return jsonify({"error": f"Failed to update field. Status code: {status_code}", "details": error_message}), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8858)
