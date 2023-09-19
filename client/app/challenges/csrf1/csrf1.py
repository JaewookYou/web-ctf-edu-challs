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

articles = [{
    "seq":0,
    "subject":"flag is here!",
    "author":"admin",
    "content": os.getenv("csrf1_flag")
}]

def sessionCheck(loginCheck=False):   
    if loginCheck:
        if "isLogin" not in flask.session:
            return False
        else:
            return True

    if "isLogin" in flask.session:
        return True
    
    return False

def xsscheck(content):
    content = content.lower()
    vulns = ["javascript", "frame", "object", "on", "data", "embed", "&#", "base","\\u","alert","fetch","XMLHttpRequest","eval","constructor"]
    vulns += list("'\"")
    for char in vulns:
        if char in content:
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
            if ids[userid] == userpw or (userid=="admin" and userpw==os.getenv("admin_password")):
                flask.session["userid"] = userid
                flask.session["isLogin"] = True
                    
                resp = flask.make_response(flask.redirect(flask.url_for("board")))
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

@app.route("/changepw", methods=["GET"])
def changepw():
    if "userid" not in flask.request.args or "userpw" not in flask.request.args:
        return flask.render_template("changepw.html", msg="false")
    else:
        userid = flask.request.args["userid"]        
        userpw = flask.request.args["userpw"]

        if userid == "admin":
            if "172.28.0." not in flask.request.remote_addr:
                return flask.render_template("changepw.html", msg="admin password is only changed at internal network")
        
        if userid in ids:
            ids[userid] = userpw
            return flask.redirect(flask.url_for("login"))
        else:
            return flask.render_template("changepw.html", msg="user doesn't exist")



@app.route("/logout")
def logout():
    flask.session.pop('isLogin', False)
    resp = flask.make_response(flask.redirect(flask.url_for("login")))
    resp.set_cookie('userid', expires=0)
    return resp


@app.route("/board", methods=["GET"])
def board():
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))
    results = []
    for i in articles:
        if i["author"] == flask.session["userid"] or flask.session["userid"] == "admin" or i["author"] == "admin":
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

        if not xsscheck(content):
            # substitute markdown image refference to html image tag
            content = re.sub(r"!\[(.*?)\]\((.*?)\)",r'<img src="\2" id="\1">',content.replace('"',''))

            req = {
                'seq':len(articles),
                'subject':subject,
                'author':flask.session['userid'],
                'content':content,
            }

            articles.append(req)

            return flask.redirect(flask.url_for("board"))
        else:
            return '<script>alert("no hack");history.go(-1);</script>'


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
        requests.post(f"http://arang_client:9000/run", data=f"url={url}&chal=csrf1", headers={"Content-Type":"application/x-www-form-urlencoded", "Content-Length":"1"})
        return "<script>history.go(-1);</script>"


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=9004, debug=True)
    except Exception as ex:
        logging.info(str(ex))
        pass
