#-*-coding:utf-8-*-
import flask
import os, pymysql, re, hashlib, time, base64, io, requests
import logging, traceback
logging.basicConfig(level=logging.INFO)
logging.getLogger('werkzeug').setLevel(level=logging.WARNING)

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

ids = {
    "asdf":"asdf"
}

challenges = [
    {
        "seq": 1,
        "challenge": "xss1 - default",
        "link": "http://arang_client:9001/"
    },
    {
        "seq": 2,
        "challenge": "xss2 - bypass",
        "link": "http://arang_client:9002/"
    },
    {
        "seq": 3,
        "challenge": "xss3 - read article",
        "link": "http://arang_client:9003/"
    },
]

def sessionCheck(loginCheck=False):   
    if loginCheck:
        if "isLogin" not in flask.session:
            return False
        else:
            return True

    if "isLogin" in flask.session:
        return True
    
    return False


@app.route("/")
def index():
    if sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("main"))

    return flask.redirect(flask.url_for("login"))

@app.route("/main")
def main():
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))

    return flask.render_template("main.html", challenges = challenges)

@app.route("/login", methods=["GET","POST"])
def login():
    if flask.request.method == "GET":
        if sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("main"))
        
        return flask.render_template("login.html", msg="false")
    else:
        if sessionCheck():
            return flask.redirect(flask.url_for("main"))
        
        userid = flask.request.form["userid"]
        userpw = flask.request.form["userpw"]
        
        if userid in ids:
            if ids[userid] == userpw:
                flask.session["userid"] = userid
                flask.session["isLogin"] = True
                    
                resp = flask.make_response(flask.redirect(flask.url_for("main")))
                resp.set_cookie('userid', flask.session["userid"])
                return resp
            else:
                return flask.render_template("login.html", msg="login fail")
        else:
            return flask.render_template("login.html", msg="login fail")


@app.route("/register", methods=["GET","POST"])
def register():
    if flask.request.method == "GET":
        if sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("main"))
        
        return flask.render_template("register.html", msg="false")
    else:
        if sessionCheck():
            return flask.redirect(flask.url_for("main"))

        userid = flask.request.form["userid"] 
        userpw = flask.request.form["userpw"]
        
        if userid not in ids:
            ids[userid] = userpw
            return flask.render_template("login.html", msg="false")
        else:
            return flask.render_template("register.html", msg="already registered id")

@app.route("/logout")
def logout():
    flask.session.pop('isLogin', False)
    return flask.redirect(flask.url_for("login"))

@app.route("/report", methods=["GET", "POST"])
def report():
    if flask.request.method == "GET":
        return '''
        <form method="POST" action="/report">
            <input type="text" name="url" placeholder="input url..." style="width:25%; height: 7%;">
            <input type="submit" value="submit">
        </form>
        '''
    elif flask.request.method == "POST":
        url = flask.request.form['url']
        requests.get(f"http://172.22.0.4:9000/run?url={url}")
        return "<script>history.go(-1);</script>"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=9091, debug=True)
    except Exception as ex:
        logging.info(str(ex))
        pass
