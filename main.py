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
    
    try:
        # Fazendo a requisição POST para o webhook do Bitrix24
        response = requests.post(url, json=data)
        
        # Logando a resposta do Bitrix24 para depuração
        print(f"Response from Bitrix24: {response.status_code} - {response.text}")
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            return response.json()
        else:
            # Retorna erro se a resposta não for 200
            return None, response.status_code, response.text
    
    except Exception as e:
        # Em caso de erro na requisição
        return None, 500, str(e)

@app.route('/copy-field', methods=['GET'])
def copy_field():
    # Recebe o ID do negócio e o valor do responsável pela venda da URL
    deal_id = request.args.get('deal_id')
    responsable_value = request.args.get('responsable_value')
    
    # Valida se os parâmetros necessários foram passados
    if not deal_id or not responsable_value:
        return jsonify({"error": "Missing parameters. 'deal_id' and 'responsable_value' are required."}), 400
    
    # Chama a função para atualizar o campo no Bitrix24
    updated_data, status_code, error_message = update_bitrix24_deal(deal_id, responsable_value)
    
    if updated_data:
        return jsonify({"success": "Field updated successfully!"}), 200
    else:
        # Retorna o erro da requisição
        return jsonify({"error": f"Failed to update field. Status code: {status_code}", "details": error_message}), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8858)
