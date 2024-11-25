from flask import Flask, request, jsonify

app = Flask(__name__)

# Dados simulados para os valores do campo UF_CRM_1699475211222
itens_responsaveis = {
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

@app.route('/atualizar-responsaveis', methods=['POST'])
def atualizar_responsaveis():
    # Pega o parâmetro 'deal_id' da URL
    deal_id = request.args.get('deal_id')
    
    if not deal_id:
        return jsonify({"error": "deal_id é necessário"}), 400
    
    # Aqui você faria a lógica para pegar os dados do negócio no Bitrix24 e verificar qual valor está no campo 'UF_CRM_1699475211222'
    # Vamos simular o comportamento, usando um ID de exemplo.
    
    # Exemplo de ID, no seu caso seria dinamicamente recuperado
    # Para testar você pode simular que o deal_id é 178096 e pegar um dos valores disponíveis
    # Aqui vou pegar um ID de exemplo (como 148)
    campo_responsavel = "148"  # Exemplo, você deverá substituir isso pela lógica de buscar o valor real do campo UF_CRM_1699475211222

    if campo_responsavel not in itens_responsaveis:
        return jsonify({"error": "ID do responsável não encontrado"}), 404

    # Pega o valor associado ao ID
    nome_responsavel = itens_responsaveis[campo_responsavel]

    # Agora você pode atualizar o campo 'UF_CRM_1732282217' com o nome do responsável
    # Simulação de atualização
    # Aqui você faria a chamada para a API do Bitrix24 para atualizar o campo.
    
    # Exemplo de resposta de sucesso
    return jsonify({
        "message": f"Responsável {nome_responsavel} atualizado com sucesso no campo UF_CRM_1732282217."
    }), 200

if __name__ == '__main__':
    # Rodando o servidor Flask na porta 5000
    app.run(debug=True, host='0.0.0.0', port=8858)
