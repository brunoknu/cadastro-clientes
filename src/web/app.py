from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
)

from src.clientes.database import criar_tabela
from src.clientes.repository import (
    inserir_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    buscar_clientes_por_nome,
    atualizar_cliente,
    excluir_cliente,
)
from src.clientes.validators import (
    validar_email,
    validar_cpf,
    validar_data,
)


def serializar_cliente(row) -> dict:
    """Converte um registro do banco (sqlite3.Row) para dict."""
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "telefone": row["telefone"],
        "cpf": row["cpf"],
        "data_nascimento": row["data_nascimento"],
    }


def criar_app() -> Flask:
    app = Flask(__name__)

    # Executa ao iniciar o servidor (Flask 3.x – sem before_first_request)
    with app.app_context():
        criar_tabela()

    # ============================
    # ROTAS HTML (INTERFACE WEB)
    # ============================

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
                erros.append("O email informado é inválido.")
            if not validar_cpf(cpf):
                erros.append("O CPF precisa ter 11 dígitos.")
            if not validar_data(data_nascimento):
                erros.append("A data deve estar no formato dd/mm/aaaa.")

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
                erros.append("O email informado é inválido.")
            if not validar_cpf(cpf):
                erros.append("O CPF precisa ter 11 dígitos.")
            if not validar_data(data_nascimento):
                erros.append("A data deve estar no formato dd/mm/aaaa.")

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

    # ============================
    # ROTAS API REST (JSON)
    # ============================

    @app.get("/api/clientes")
    def api_listar_clientes():
        """
        GET /api/clientes
        Opcional: ?q=nome_parcial  para buscar por nome
        """
        termo = request.args.get("q", "").strip()
        if termo:
            clientes = buscar_clientes_por_nome(termo)
        else:
            clientes = listar_clientes()

        dados = [serializar_cliente(c) for c in clientes]
        return jsonify(dados), 200

    @app.get("/api/clientes/<int:id_cliente>")
    def api_obter_cliente(id_cliente: int):
        """
        GET /api/clientes/<id>
        """
        cliente = buscar_cliente_por_id(id_cliente)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        return jsonify(serializar_cliente(cliente)), 200

    @app.post("/api/clientes")
    def api_criar_cliente():
        """
        POST /api/clientes
        Body JSON:
        {
            "nome": "...",   (obrigatório)
            "email": "...",
            "telefone": "...",
            "cpf": "...",
            "data_nascimento": "dd/mm/aaaa"
        }
        """
        payload = request.get_json(silent=True) or {}
        erros = []

        nome = (payload.get("nome") or "").strip()
        email = (payload.get("email") or "").strip()
        telefone = (payload.get("telefone") or "").strip()
        cpf = (payload.get("cpf") or "").strip()
        data_nascimento = (payload.get("data_nascimento") or "").strip()

        if not nome:
            erros.append("O campo 'nome' é obrigatório.")
        if not validar_email(email):
            erros.append("O campo 'email' é inválido.")
        if not validar_cpf(cpf):
            erros.append("O campo 'cpf' deve possuir 11 dígitos.")
        if not validar_data(data_nascimento):
            erros.append("O campo 'data_nascimento' deve estar no formato dd/mm/aaaa.")

        if erros:
            return jsonify({"erros": erros}), 400

        inserir_cliente(nome, email, telefone, cpf, data_nascimento)
        # Recupera o último cliente inserido (mais simples: listar e pegar o último)
        cliente = listar_clientes()[-1]
        return jsonify(serializar_cliente(cliente)), 201

    @app.put("/api/clientes/<int:id_cliente>")
    def api_atualizar_cliente(id_cliente: int):
        """
        PUT /api/clientes/<id>
        JSON igual ao POST.
        """
        cliente = buscar_cliente_por_id(id_cliente)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        payload = request.get_json(silent=True) or {}
        erros = []

        nome = (payload.get("nome") or "").strip()
        email = (payload.get("email") or "").strip()
        telefone = (payload.get("telefone") or "").strip()
        cpf = (payload.get("cpf") or "").strip()
        data_nascimento = (payload.get("data_nascimento") or "").strip()

        if not nome:
            erros.append("O campo 'nome' é obrigatório.")
        if not validar_email(email):
            erros.append("O campo 'email' é inválido.")
        if not validar_cpf(cpf):
            erros.append("O campo 'cpf' deve possuir 11 dígitos.")
        if not validar_data(data_nascimento):
            erros.append("O campo 'data_nascimento' deve estar no formato dd/mm/aaaa.")

        if erros:
            return jsonify({"erros": erros}), 400

        atualizar_cliente(id_cliente, nome, email, telefone, cpf, data_nascimento)
        cliente_atualizado = buscar_cliente_por_id(id_cliente)
        return jsonify(serializar_cliente(cliente_atualizado)), 200

    @app.delete("/api/clientes/<int:id_cliente>")
    def api_excluir_cliente(id_cliente: int):
        """
        DELETE /api/clientes/<id>
        """
        cliente = buscar_cliente_por_id(id_cliente)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        excluir_cliente(id_cliente)
        return jsonify({"mensagem": "Cliente excluído com sucesso"}), 200

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)

def criar_app() -> Flask:
    app = Flask(__name__)

    with app.app_context():
        criar_tabela()

    # ============================
    # ROTAS HTML
    # ============================

    @app.route("/")
    def index():
        clientes = listar_clientes()
        return render_template("index.html", clientes=clientes)

    # (suas outras rotas HTML /novo, /editar, /excluir ficam aqui)

    # ============================
    # ROTAS API
    # ============================

    @app.get("/api/clientes")
    def api_listar_clientes():
        termo = request.args.get("q", "").strip()
        if termo:
            clientes = buscar_clientes_por_nome(termo)
        else:
            clientes = listar_clientes()
        dados = [serializar_cliente(c) for c in clientes]
        return jsonify(dados), 200

    @app.post("/api/clientes")
    def api_criar_cliente():
        payload = request.get_json(silent=True) or {}
        erros = []

        nome = (payload.get("nome") or "").strip()
        email = (payload.get("email") or "").strip()
        telefone = (payload.get("telefone") or "").strip()
        cpf = (payload.get("cpf") or "").strip()
        data_nascimento = (payload.get("data_nascimento") or "").strip()

        if not nome:
            erros.append("O campo 'nome' é obrigatório.")
        if not validar_email(email):
            erros.append("O campo 'email' é inválido.")
        if not validar_cpf(cpf):
            erros.append("O campo 'cpf' deve possuir 11 dígitos.")
        if not validar_data(data_nascimento):
            erros.append("O campo 'data_nascimento' deve estar no formato dd/mm/aaaa.")

        if erros:
            return jsonify({"erros": erros}), 400

        inserir_cliente(nome, email, telefone, cpf, data_nascimento)
        cliente = listar_clientes()[-1]
        return jsonify(serializar_cliente(cliente)), 201

    @app.post("/api/clientes/lote")
    def api_criar_clientes_lote():
        """
        Endpoint PLUS engatilhado.
        Aceita uma lista (array JSON) com vários clientes.
        """
        payload = request.get_json(silent=True)

        if not isinstance(payload, list):
            return jsonify({"erro": "Envie uma lista (array JSON) como body."}), 400

        criadas = []
        falhas = []

        for indice, cliente in enumerate(payload):
            nome = (cliente.get("nome") or "").strip()
            email = (cliente.get("email") or "").strip()
            telefone = (cliente.get("telefone") or "").strip()
            cpf = (cliente.get("cpf") or "").strip()
            data_nascimento = (cliente.get("data_nascimento") or "").strip()

            erros = []

            if not nome:
                erros.append("nome obrigatório")
            if not validar_email(email):
                erros.append("email inválido")
            if not validar_cpf(cpf):
                erros.append("cpf inválido (precisa ter 11 dígitos)")
            if not validar_data(data_nascimento):
                erros.append("data inválida (formato dd/mm/aaaa)")

            if erros:
                falhas.append({
                    "indice": indice,
                    "cliente": cliente,
                    "erros": erros,
                })
                continue

            inserir_cliente(nome, email, telefone, cpf, data_nascimento)
            criadas.append(cliente)

        return jsonify({
            "criadas": len(criadas),
            "falhas": len(falhas),
            "detalhes_falhas": falhas,
        }), 207

    # NENHUMA rota abaixo dessa linha
    return app


app = criar_app()

# DEBUG: listar todas as rotas registradas
print("=== ROTAS REGISTRADAS ===")
for rule in app.url_map.iter_rules():
    print(rule, "->", list(rule.methods))
print("=== FIM DAS ROTAS ===")

if __name__ == "__main__":
    app.run(debug=True)

# ================================================================
# ROTA FUTURA (ENGATILHADA) - IMPORTAÇÃO EM LOTE DE CLIENTES
# ---------------------------------------------------------------
# Esta rota será usada no futuro para permitir envio de vários
# clientes ao mesmo tempo em um único request (API profissional).
#
# No momento, ela está comentada porque:
#  - não queremos expor no README ainda,
#  - ainda estamos validando a estrutura,
#  - e não deve ser usada por while.
#
# Quando quiser ativar:
#  1. descomente o bloco,
#  2. garanta que processar_lote_clientes esteja implementado,
#  3. e adicione testes no Thunder Client/Postman.
#
# from src.clientes.service import processar_lote_clientes
#
# @app.post("/api/clientes/lote")
# def api_criar_clientes_lote():
#     payload = request.get_json(silent=True)
#
#     # Chama o serviço que processa o lote de clientes
#     criadas, falhas = processar_lote_clientes(payload)
#
#     # Retorno padrão para operações em lote:
#     #  - 207 Multi-Status (HTTP oficial para respostas mistas)
#     return jsonify({
#         "criadas": len(criadas),
#         "falhas": len(falhas),
#         "detalhes_falhas": falhas,
#     }), 207
# ================================================================
