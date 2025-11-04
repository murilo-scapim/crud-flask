import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
load_dotenv()

estoque = []


def criar_conexao_banco():
    con = psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("PASSWORD")
    )
    return con


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_produto():
    if request.method == "GET":
        return render_template("cadastro.html")

    descricao = request.form["descricao"]
    preco = float(request.form["preco"])
    quantidade = int(request.form["quantidade"])
    quantidade_minima = int(request.form["quantidade_minima"])

    try:
        con = criar_conexao_banco()
        cursor = con.cursor()
        cursor.execute('''INSERT INTO produto(descricao, preco,
            quantidade, quantidade_minima)
            VALUES (%s, %s, %s, %s);''', (descricao, preco,
                                          quantidade, quantidade_minima))
        con.commit()
        cursor.close()
        con.close()
        print("Produto inserido!")
        return redirect(url_for("listar_produtos"))
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")


@app.route("/listar")
def listar_produtos():
    return render_template("lista.html", produtos=estoque)


@app.route("/relatorio")
def exibir_relatorio():
    return render_template("relatorio.html", produtos=estoque)


def buscar_produto_por_cod(codigo):
    for produto in estoque:
        if produto["codigo"] == codigo:
            return produto
    return None


@app.route("/editar/<int:codigo>", methods=["GET", "POST"])
def editar_produto(codigo):
    produto = buscar_produto_por_cod(codigo)

    if produto:
        if request.method == "POST":
            produto["descricao"] = request.form["descricao"]
            produto["preco"] = float(request.form["preco"])
            produto["quantidade"] = int(request.form["quantidade"])
            produto["quantidade_minima"] = int(request.form["quantidade_minima"])
            return redirect(url_for("listar_produtos"))

        return render_template("editar.html", produto=produto)
    else:
        print("Produto não encontrado")


@app.route("/apagar/<int:codigo>", methods=["POST"])
def apagar_produto(codigo):
    produto = buscar_produto_por_cod(codigo)

    if produto:
        estoque.remove(produto)
    return redirect(url_for("listar_produtos"))


@app.route("/entrada/<int:codigo>", methods=["GET", "POST"])
def entrada_estoque(codigo):
    produto = buscar_produto_por_cod(codigo)
    if not produto:
        return "Produto não encontrado"

    if request.method == "POST":
        quantidade = int(request.form["quantidade"])
        if quantidade > 0:
            produto["quantidade"] += quantidade
            return redirect(url_for("listar_produtos"))
        return render_template("entrada_estoque.html", produto=produto,
                               erro="Quantidade inválida!")
    return render_template("entrada_estoque.html", produto=produto)


if __name__ == '__main__':
    app.run(debug=True)
