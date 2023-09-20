#-*-coding:utf-8-*-
import flask
import os, subprocess

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

@app.route("/")
def index():
	if "name" in flask.request.args:
		template =f'''
		<h2> hello {flask.request.args['name']}! </h2>
		'''
		return flask.render_template_string(template)
	else:
		template = '''
		<h2> hello noname............ </h2>
		'''
		return flask.render_template_string(template)


if __name__ == "__main__":
	try:
		app.run(host="0.0.0.0", port=9302, debug=True)
	except Exception as ex:
		logging.info(str(ex))
		pass
