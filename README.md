# 💰 Controle Financeiro

Aplicação desktop para controle de despesas pessoais, desenvolvida em Python com CustomTkinter.

O sistema permite cadastrar, editar e excluir despesas, controlar gastos fixos, variáveis e parcelados, além de possibilitar a divisão de despesas entre várias pessoas.

## ✨ Funcionalidades

- 💰 Controle de despesas
- 🔒 Despesas fixas
- 🔄 Despesas variáveis
- 📅 Despesas parceladas
- ✅ Controle de parcelas pagas
- 👥 Divisão de despesas
- ✏️ Edição de despesas
- 🗑️ Exclusão de despesas
- 📊 Relatórios por categoria
- 📊 Relatórios por tipo de despesa
- 🌙 Tema escuro e claro
- 💾 Salvamento automático dos dados em JSON

## 🖥️ Interface

O sistema possui uma interface gráfica desenvolvida com CustomTkinter.

### Dashboard

O painel inicial apresenta um resumo dos gastos:

- Total gasto
- Quantidade de despesas
- Gastos fixos
- Gastos variáveis
- Gastos parcelados

### Controle de despesas

É possível cadastrar despesas informando:

- Descrição
- Valor
- Tipo
- Categoria
- Parcelamento
- Divisão da despesa

### Divisão de despesas

Uma despesa pode ser dividida entre várias pessoas.

O sistema permite:

- Divisão igual entre as pessoas
- Definição manual da parte do usuário

## 🛠️ Tecnologias

- Python
- CustomTkinter
- JSON
- Git
- GitHub

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/DiegoMarino11/controle-financeiro-python.git


2. Entre na pasta

cd controle-financeiro-python

3. Instale a dependência

pip install customtkinter

4. Execute o programa

python main.py

📁 Estrutura do projeto
controle-financeiro-python/
│
├── main.py
├── despesas.json
└── README.md
💾 Armazenamento

Os dados das despesas são armazenados localmente no arquivo:

despesas.json

Não é necessário utilizar banco de dados ou servidor para executar a aplicação.

📌 Projeto

Projeto desenvolvido para estudo, prática de programação e construção de portfólio.

Desenvolvido por Diego Marino

