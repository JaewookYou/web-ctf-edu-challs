#-*-coding:utf-8-*-
import flask
import os, subprocess

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

@app.route("/")
def index():
	if "cmd" not in flask.request.args:
		with open("app.py","r") as f:
			content = f.read()
		return content
	else:
		cmd = flask.request.args["cmd"]
		p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
		return "!"


if __name__ == "__main__":
	try:
		app.run(host="0.0.0.0", port=9301, debug=True)
	except Exception as ex:
		logging.info(str(ex))
		pass
