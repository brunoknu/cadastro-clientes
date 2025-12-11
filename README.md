# Cadastro de Clientes — Aplicação Web com Flask

Este projeto é uma aplicação web desenvolvida em **Python (Flask)** para cadastro, edição, listagem e exclusão de clientes utilizando o banco de dados **SQLite**.

A aplicação possui uma estrutura profissional, separando camadas de:

- **Interface Web (Flask)**
- **Regras de Negócio**
- **Banco de Dados**
- **Validações**
- **Utilitários**
- **Interface CLI (opcional)**

Ideal para estudos, portfólio e demonstrações de arquitetura limpa em Python.

---

## 🚀 Funcionalidades

- Cadastrar novos clientes
- Listar todos os clientes registrados
- Editar informações de um cliente
- Excluir clientes do banco
- Validações de:
  - Email
  - CPF (formato simples)
  - Data de nascimento (dd/mm/aaaa)
- Interface Web responsiva usando Bootstrap

---

## 📁 Estrutura do Projeto
src/
├── cli/ # Interface opcional via terminal
├── clientes/ # Regra de negócio + banco
│ ├── database.py
│ ├── repository.py
│ ├── validacao.py
├── utils/ # Funções auxiliares
│ └── email.py
├── web/ # Aplicação Flask
│ ├── static/ # CSS, JS e imagens
│ ├── templates/ # Arquivos HTML
│ ├── app.py # Rotas e inicialização
│ └── init.py

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask**
- **SQLite**
- **HTML + Bootstrap**
- **Git/GitHub**

---

## 📦 Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/brunoknu/cadastro-clientes.git
cd cadastro-clientes
