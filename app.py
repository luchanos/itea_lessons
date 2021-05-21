# магазинное приложения на Flask

from flask import Flask, render_template

app = Flask("my_shiny_shop_corp_app")


@app.route("/main")
@app.route("/home")
@app.route("/")
def main_page():
    return render_template("base.html")


@app.route("/order/<int:order_id>")
def get_order(order_id):
    return f"{order_id} OK"


if __name__ == "__main__":
    # так создаётся простое приложение на Flask, которое при запуске поднимет серверочек
    app.run(debug=True)
