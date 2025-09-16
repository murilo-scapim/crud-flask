from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

estoque = []


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_produto():

    if request.method == "GET":
        return render_template("cadastro.html")

    descricao = request.form["descricao"]
    preco = float(request.form["preco"])
    quantidade = int(request.form["quantidade"])
    quantidade_minima = int(request.form["quantidade_minima"])

    produto = {
        "codigo": len(estoque) + 1,
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidade,
        "quantidade_minima": quantidade_minima
    }

    estoque.append(produto)
    return redirect(url_for("listar_produtos"))


@app.route("/listar")
def listar_produtos():
    return render_template("lista.html", produtos=estoque)


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

        print(produto)

        return render_template("editar.html", produto=produto)
    else:
        print("Produto não encontrado")


@app.route("/apagar/<int:codigo>", methods=["POST"])
def apagar_produto(codigo):
    produto = buscar_produto_por_cod(codigo)

    if produto:
        estoque.remove(produto)
    return redirect(url_for("listar_produtos"))


if __name__ == '__main__':
    app.run(debug=True)
