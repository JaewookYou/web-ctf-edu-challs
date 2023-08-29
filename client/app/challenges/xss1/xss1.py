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
    "admin":os.getenv("admin_password")
}

articles = []

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
        return flask.redirect(flask.url_for("board"))

    return flask.redirect(flask.url_for("login"))



@app.route("/login", methods=["GET","POST"])
def login():
    if flask.request.method == "GET":
        if sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("board"))
        
        return flask.render_template("login.html", msg="false")
    else:
        if sessionCheck():
            return flask.redirect(flask.url_for("board"))
        
        userid = flask.request.form["userid"]
        userpw = flask.request.form["userpw"]
        
        if userid in ids:
            if ids[userid] == userpw:
                flask.session["userid"] = userid
                flask.session["isLogin"] = True
                    
                resp = flask.make_response(flask.redirect(flask.url_for("board")))
                resp.set_cookie('userid', flask.session["userid"])
                if userid == "admin":
                    resp.set_cookie('flag', os.getenv("xss1_flag"))
                return resp
            else:
                return flask.render_template("login.html", msg="login fail")
        else:
            return flask.render_template("login.html", msg="login fail")


@app.route("/register", methods=["GET","POST"])
def register():
    if flask.request.method == "GET":
        if sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("board"))
        
        return flask.render_template("register.html", msg="false")
    else:
        if sessionCheck():
            return flask.redirect(flask.url_for("board"))

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


@app.route("/board", methods=["GET"])
def board():
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))
    results = []
    for i in articles:
        if i["author"] == flask.session["userid"] or flask.session["userid"] == "admin":
            results.append(i)
    return flask.render_template("board.html", articles=results)


@app.route("/board/<seq>")
def viewboard(seq):
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))

    article = articles[int(seq)]
    if article["author"] == flask.session["userid"] or flask.session["userid"] == "admin":
        return flask.render_template("view.html", articles=article)
    else:
        return "<script>alert('This is not your article');location.replace('/');</script>"

@app.route("/write", methods=["GET", "POST"])
def write():
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))

    if flask.request.method == "GET":
        return flask.render_template("write.html", loginid=flask.session["userid"])

    elif flask.request.method == "POST":
        subject = flask.request.form["subject"]
        author = flask.request.form["author"]
        content = flask.request.form["content"]
        
        req = {
            'seq':len(articles),
            'subject':subject,
            'author':flask.session['userid'],
            'content':content,
        }

        articles.append(req)

        return flask.redirect(flask.url_for("board"))


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
        requests.get(f"http://arang_client:9000/run?chal=xss1&url={url}")
        return "<script>history.go(-1);</script>"


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=9001, debug=True)
    except Exception as ex:
        logging.info(str(ex))
        pass
