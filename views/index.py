from flask import render_template

from . import index_blu




@index_blu.route("/")
def index():
	print("成功-----")
	return render_template("index.html")
