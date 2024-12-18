from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)


load_dotenv()
CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')
CODIGO_BITRIX_STR = os.getenv('CODIGO_BITRIX_STR')
PROFILE = os.getenv('PROFILE')
BASE_URL_API_BITRIX = os.getenv('BASE_URL_API_BITRIX')



WEBHOOK_URL = f"{BASE_URL_API_BITRIX}/{PROFILE}/{CODIGO_BITRIX}"

@app.route('/transferir', methods=['POST'])
def transferir_dados():
    # Obter o ID_REGISTRO tanto do corpo JSON quanto da query string
    id_registro = request.json.get('ID_REGISTRO') if request.json else request.args.get('ID_REGISTRO')

    # Verificar se o ID_REGISTRO foi enviado
    if not id_registro:
        return jsonify({"erro": "Campo 'ID_REGISTRO' não encontrado"}), 400

    # 1. Buscar o valor do campo 'UF_CRM_1732303914' do deal
    url_busca = f"{WEBHOOK_URL}/crm.deal.get.json"
    params_busca = {"ID": id_registro}

    try:
        resposta_busca = requests.get(url_busca, params=params_busca)
        resposta_busca.raise_for_status()  # Levanta um erro em caso de falha
    except requests.RequestException as e:
        return jsonify({"erro": f"Erro ao buscar dados do deal: {str(e)}"}), 500

    dados_deal = resposta_busca.json()

    # Verificar se o campo 'UF_CRM_1699475211222' existe no deal
    if 'result' not in dados_deal or 'UF_CRM_1699475211222' not in dados_deal['result']:
        return jsonify({"erro": "Campo 'UF_CRM_1699475211222' não encontrado no deal"}), 400

    valor = dados_deal['result']['UF_CRM_1699475211222']

    # Substituir valores conforme o mapeamento
    valores_map = {
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
    }

    valor = valores_map.get(valor, valor)  # Substitui se o valor estiver no mapeamento

    # 2. Atualizar o campo 'UF_CRM_1732282217' no mesmo deal
    url_atualiza = f"{WEBHOOK_URL}/crm.deal.update.json"
    params_atualiza = {
        "ID": id_registro,
        "fields": {
            "UF_CRM_1732282217": valor
        }
    }

    try:
        resposta_atualiza = requests.post(url_atualiza, json=params_atualiza)
        resposta_atualiza.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"erro": f"Erro ao atualizar o campo do deal: {str(e)}"}), 500

    return jsonify({"sucesso": "Dados transferidos com sucesso"}), 200


@app.route('/transferir-bko', methods=['POST'])
def transferir_dados_bko():
    id_deal = request.json.get('ID_DEAL') if request.json else request.args.get('ID_DEAL')

    if not id_deal:
        return jsonify({"erro": "Campo 'ID_DEAL' não encontrado"}), 400
    
    url_busca = f"{WEBHOOK_URL}/crm.deal.get.json"
    params_busca = {"ID": id_deal}

    try: 
        resposta_busca = requests.get(url_busca, params=params_busca)
        resposta_busca.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"erro": f"Erro ao buscar dados do deal:{str(e)}"}), 500
    
    dados_deal = resposta_busca.json()

    if 'result' not in dados_deal or 'UF_CRM_1700663313965' not in dados_deal['result']:
        return jsonify({"erro":"Campo 'Bko - Responsavél pela venda' não encontrado"}), 400
    
    valor = dados_deal['result']['UF_CRM_1700663313965']

    valores_map = {
        "222": "Rafael dos Santos",
        "226": "Rafael Bruce",
        "326": "Juan Cesar",
        "34884": "Taynara Francine",
        "40868": "Mariah Victoria",
        "48670": "Barbara Virginia",
        "48686": "João Fontes"
    }

    valor = valores_map.get(valor, valor)
    url_atualiza = f"{WEBHOOK_URL}/crm.deal.update.json"
    params_atualiza = {
        "ID": id_deal,
        "fields": {
            "UF_CRM_1732303914": valor
        }
    }

    try:
        resposta_atualiza = requests.post(url_atualiza, json=params_atualiza)
        resposta_atualiza.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"erro": f"Erro ao atualizar o campo do deal: {str(e)}"}), 500

    return jsonify({"sucesso": "Dados transferidos com sucesso"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8858, debug=True)
