# 🔁 Transferência Automática de Dados entre Campos no Bitrix24 🇧🇷  
_(Scroll down for English version 🇺🇸)_

Este projeto foi desenvolvido para **automatizar a cópia de valores entre campos personalizados** em negócios (deals) do Bitrix24. Ideal para repassar informações entre áreas, como Vendas e BKO, com base em valores mapeados manualmente.

---

### ✅ O que ele faz?

- Conecta-se ao Bitrix24 via API.
- Busca o valor de um campo personalizado.
- Converte o valor numérico para um nome, com base em um mapa interno.
- Atualiza outro campo no mesmo negócio com o nome correspondente.
- Possui dois endpoints: um para Vendas e outro para BKO.

---

### 🔧 Como funciona?

1. Recebe um `ID_DEAL` ou `ID_REGISTRO` via JSON.
2. Consulta o negócio correspondente na API do Bitrix24.
3. Verifica o campo de origem e faz a correspondência com o nome.
4. Atualiza o campo de destino com o nome identificado.

---

### 🛡️ Segurança

- Uso de `.env` para manter credenciais seguras.
- Comunicação via HTTPS com a API oficial do Bitrix24.
- Tratamento de erros para respostas claras e robustas.

---

### 📈 Benefícios para sua empresa

- Automatiza tarefas internas entre setores.
- Garante que os dados estejam sempre sincronizados.
- Evita preenchimento manual e retrabalho operacional.

> Quer aplicar esse tipo de automação no seu Bitrix24? Fale comigo e vamos personalizar para o seu fluxo. 😉

---

# 🔁 Automatic Field Transfer in Bitrix24 🇺🇸

This project automates the **transfer of data between custom fields** in Bitrix24 deals. It’s perfect for syncing internal team data (like Sales and BKO) based on predefined mappings.

---

### ✅ What does it do?

- Connects to Bitrix24 via API.
- Reads a numeric value from a custom field.
- Maps the value to a person’s name.
- Updates another field in the same deal with that name.
- Provides two separate endpoints for different flows.

---

### 🔧 How does it work?

1. Receives `ID_DEAL` or `ID_REGISTRO` via JSON request.
2. Fetches the deal from Bitrix24 API.
3. Maps the numeric value to a readable name.
4. Updates a second custom field with that name.

---

### 🛡️ Security

- Uses `.env` file to store secure credentials.
- Interacts only with official Bitrix24 API.
- Includes error handling for reliable automation.

---

### 📈 Business Benefits

- Automates internal data handoff between teams.
- Keeps CRM fields consistently filled.
- Reduces manual work and human error.

> Want this kind of workflow automation in your Bitrix24? Let’s talk and tailor it for your operation. 😉
