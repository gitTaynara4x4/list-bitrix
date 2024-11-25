from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Webhook URL do Bitrix24
webhook_url = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg/"

# Mapeamento de IDs para valores
id_value_mapping = {
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

# Função para obter e atualizar o card
def atualizar_card(deal_id):
    # Log para depuração
    app.logger.info(f"Buscando dados para o deal_id: {deal_id}")

    # Buscar o valor do campo UF_CRM_1699475211222 para o deal_id
    response = requests.post(f"{webhook_url}crm.deal.get.json", data={"ID": deal_id})
    
    if response.status_code == 200:
        data = response.json()
        # Verifica se o campo UF_CRM_1699475211222 existe no retorno
        uf_crm_value = data.get('result', {}).get('UF_CRM_1699475211222', None)
        
        if uf_crm_value:
            # Verifica se o ID encontrado está na lista
            if str(uf_crm_value) in id_value_mapping:
                nome = id_value_mapping[str(uf_crm_value)]
                
                # Atualizar o campo UF_CRM_1732282217 com o nome correspondente
                update_data = {
                    "ID": deal_id,
                    "fields": {
                        "UF_CRM_1732282217": nome
                    }
                }
                
                update_response = requests.post(f"{webhook_url}crm.deal.update.json", data=update_data)
                
                if update_response.status_code == 200:
                    app.logger.info(f"Campo atualizado com sucesso para o deal_id: {deal_id}")
                    return {"message": "Campo atualizado com sucesso!", "status": "success"}
                else:
                    app.logger.error(f"Erro ao atualizar o card com deal_id: {deal_id}")
                    return {"message": "Erro ao atualizar o card.", "status": "error"}
            else:
                app.logger.warning(f"O ID {uf_crm_value} não está na lista para o deal_id: {deal_id}")
                return {"message": f"O ID {uf_crm_value} não está na lista.", "status": "error"}
        else:
            app.logger.warning(f"Campo UF_CRM_1699475211222 não encontrado no card com deal_id: {deal_id}")
            return {"message": "Campo UF_CRM_1699475211222 não encontrado no card.", "status": "error"}
    else:
        app.logger.error(f"Erro ao buscar o card com deal_id: {deal_id}")
        return {"message": "Erro ao buscar o card.", "status": "error"}

# Endpoint para a API
@app.route('/atualizar-responsaveis', methods=['GET'])
def api_atualizar_card():
    # Obter o 'deal_id' da query string
    deal_id = request.args.get('deal_id')

    app.logger.info(f"Recebendo requisição para deal_id: {deal_id}")

    if not deal_id:
        app.logger.error("Parâmetro 'deal_id' ausente na requisição.")
        return jsonify({"message": "Parâmetro 'deal_id' é obrigatório.", "status": "error"}), 400
    
    result = atualizar_card(deal_id)
    return jsonify(result)

# Iniciar o servidor na porta 8858
if __name__ == '__main__':
    app.run(debug=True, port=8858)
