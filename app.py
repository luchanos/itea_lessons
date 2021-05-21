# магазинное приложения на Flask

from flask import Flask, render_template, url_for

app = Flask("my_shiny_shop_corp_app")


@app.route("/main")
@app.route("/home")
@app.route("/")
def main_page():
    return render_template("base.html")


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    return render_template("shop.html", shop_id=shop_id)


if __name__ == "__main__":
    # так создаётся простое приложение на Flask, которое при запуске поднимет серверочек
    app.run(debug=True)
