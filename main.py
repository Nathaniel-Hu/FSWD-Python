import os
# from replit import db
from flask import Flask, redirect, url_for, render_template

from Backend.Item import Item

template_dir = os.path.abspath("Frontend/Templates/")
app = Flask(__name__, template_folder=template_dir)
admin_access = False


@app.route("/<name>/")
def index(name):
    return render_template("index.html", content=name, content2=["bob", "joe", "sam"])


# @app.route("/<name>/")
# def user(name):
#     return f"Hello {name}!"
#
#
# @app.route("/admin/")
# def admin():
#     if admin_access:
#         return f"Welcome to the admin page!"
#     else:
#         return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    app.run()
