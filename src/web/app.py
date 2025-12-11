from flask import Flask, render_template, request, redirect, url_for

from src.clientes.database import criar_tabela
from src.clientes.repository import (
    inserir_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    excluir_cliente,
)
from src.clientes.validators import (
    validar_email,
    validar_cpf,
    validar_data,
)




def criar_app():
    app = Flask(__name__)

    with app.app_context():
        criar_tabela()


    @app.route("/")
    def index():
        clientes = listar_clientes()
        return render_template("index.html", clientes=clientes)

    @app.route("/novo", methods=["GET", "POST"])
    def novo_cliente():
        erros = []

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            telefone = request.form.get("telefone", "").strip()
            cpf = request.form.get("cpf", "").strip()
            data_nascimento = request.form.get("data_nascimento", "").strip()

            if not nome:
                erros.append("O nome é obrigatório.")
            if not validar_email(email):
                erros.append("Email inválido.")
            if not validar_cpf(cpf):
                erros.append("CPF inválido (11 dígitos).")
            if not validar_data(data_nascimento):
                erros.append("Data inválida. Formato dd/mm/aaaa.")

            if not erros:
                inserir_cliente(nome, email, telefone, cpf, data_nascimento)
                return redirect(url_for("index"))

            dados = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
            }

            return render_template(
                "form.html",
                titulo="Cadastrar novo cliente",
                action_url=url_for("novo_cliente"),
                dados=dados,
                erros=erros,
            )

        dados = {
            "nome": "",
            "email": "",
            "telefone": "",
            "cpf": "",
            "data_nascimento": "",
        }

        return render_template(
            "form.html",
            titulo="Cadastrar novo cliente",
            action_url=url_for("novo_cliente"),
            dados=dados,
            erros=erros,
        )

    @app.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
    def editar_cliente_view(id_cliente):
        cliente = buscar_cliente_por_id(id_cliente)

        if not cliente:
            return "Cliente não encontrado.", 404

        erros = []

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            telefone = request.form.get("telefone", "").strip()
            cpf = request.form.get("cpf", "").strip()
            data_nascimento = request.form.get("data_nascimento", "").strip()

            if not nome:
                erros.append("O nome é obrigatório.")
            if not validar_email(email):
                erros.append("Email inválido.")
            if not validar_cpf(cpf):
                erros.append("CPF deve ter 11 dígitos.")
            if not validar_data(data_nascimento):
                erros.append("Data inválida. Formato dd/mm/aaaa.")

            if not erros:
                atualizar_cliente(
                    id_cliente, nome, email, telefone, cpf, data_nascimento
                )
                return redirect(url_for("index"))

            dados = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
            }

            return render_template(
                "form.html",
                titulo=f"Editar cliente #{id_cliente}",
                action_url=url_for("editar_cliente_view", id_cliente=id_cliente),
                dados=dados,
                erros=erros,
            )

        dados = {
            "nome": cliente["nome"],
            "email": cliente["email"],
            "telefone": cliente["telefone"],
            "cpf": cliente["cpf"],
            "data_nascimento": cliente["data_nascimento"],
        }

        return render_template(
            "form.html",
            titulo=f"Editar cliente #{id_cliente}",
            action_url=url_for("editar_cliente_view", id_cliente=id_cliente),
            dados=dados,
            erros=erros,
        )

    @app.route("/excluir/<int:id_cliente>", methods=["POST"])
    def excluir_cliente_route(id_cliente):
        cliente = buscar_cliente_por_id(id_cliente)

        if not cliente:
            return "Cliente não encontrado.", 404

        excluir_cliente(id_cliente)
        return redirect(url_for("index"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)