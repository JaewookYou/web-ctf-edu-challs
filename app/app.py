#-*-coding:utf-8-*-
import flask
import os, pymysql, re, hashlib, time, base64, io, requests, json
import logging, traceback
logging.basicConfig(level=logging.INFO)
logging.getLogger('werkzeug').setLevel(level=logging.WARNING)

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

ids = {}
def load_user():
    global ids
    if os.path.exists("users.json"):
        with open("users.json","r") as f:
            ids = json.loads(f.read())
        for i in ids.keys():
            ids[i]['solved'] = list(set(ids[i]['solved']))
    else:
        ids = {
            "arang":{
                "password": "123123",
                "solved": [],
                "lastsolved":0
            }
        }
load_user()


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
    {
        "seq": 4,
        "challenge": "domclobbering",
        "link": "http://arang_client:9200/domclobbering.php"
    },
    {
        "seq": 5,
        "challenge": "csrf1 - change admin password1",
        "link": "http://arang_client:9004/"
    },
    {
        "seq": 6,
        "challenge": "csrf2 - change admin password2",
        "link": "http://arang_client:9005/"
    },
    {
        "seq": 7,
        "challenge": "xsleak - get secret value of admin",
        "link": "http://arang_client:9006/"
    },
    {
        "seq": 8,
        "challenge": "sqli1 - basic",
        "link": "http://arang_client:9200/sqli1.php"
    },
    {
        "seq": 9,
        "challenge": "sqli2 - bypass filtering",
        "link": "http://arang_client:9200/sqli2.php"
    },
    {
        "seq": 10,
        "challenge": "sqli3 - blind sqli + bypass filtering",
        "link": "http://arang_client:9200/sqli3.php"
    },
    {
        "seq": 11,
        "challenge": "lif1 - basic",
        "link": "http://arang_client:9201/lfi1.php"
    },
    {
        "seq": 12,
        "challenge": "lfi2 - get the shell",
        "link": "http://arang_client:9201/lfi2.php"
    },
    {
        "seq": 13,
        "challenge": "command injection - blind",
        "link": "http://arang_client:9301/"
    },
    {
        "seq": 14,
        "challenge": "ssti - get the shell",
        "link": "http://arang_client:9302/"
    },
    {
        "seq": 15,
        "challenge": "prototype - eval js code",
        "link": "http://arang_client:9200/prototype_pollution.php"
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
    global ids
    if not sessionCheck(loginCheck=True):
        return flask.redirect(flask.url_for("login"))

    load_user()
    t=[]
    for i in range(len(challenges)):
        if i in ids[flask.session["userid"]]["solved"]:
            tt = challenges[i]
            tt["solved"] = True
        else:
            tt = challenges[i]
            tt["solved"] = False
        t.append(tt)
    
    return flask.render_template("main.html", c=t)


@app.route("/ranking")
def ranking():
    load_user()
    t = []
    sorted_dict = dict(sorted(ids.items(), key=lambda item: (-len(item[1]["solved"]), item[1]["lastsolved"])))
    print(sorted_dict)
    for i in sorted_dict.keys():
        if not sorted_dict[i]["solved"]:
            continue
        t.append({i:sorted_dict[i]})
    print(t)
    return flask.render_template("ranking.html", ids=t)
    

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
            if ids[userid]["password"] == hashlib.sha256(userpw.encode()).hexdigest():
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
        userpw = hashlib.sha256(flask.request.form["userpw"].encode()).hexdigest()
    
        if userid not in ids:
            ids[userid] = {
                "password": userpw,
                "solved": [],
                "lastsolved": 0
            }
            with open("users.json", "w") as f:
                f.write(json.dumps(ids, indent=4))
            return flask.render_template("login.html", msg="false")
        else:
            return flask.render_template("register.html", msg="already registered id")

@app.route("/logout")
def logout():
    flask.session.pop('isLogin', False)
    resp = flask.make_response(flask.redirect(flask.url_for("login")))
    resp.set_cookie('userid', expires=0)
    return resp

@app.route("/checkflag", methods=["GET", "POST"])
def report():
    if flask.request.method == "GET":
        if not sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("login"))
        else:
            return '''
            <form method="POST" action="/checkflag">
                <input type="text" name="flag" placeholder="input flag..." style="width:25%; height: 7%;">
                <input type="submit" value="submit">
            </form>
            '''
    elif flask.request.method == "POST":
        if not sessionCheck(loginCheck=True):
            return flask.redirect(flask.url_for("login"))

        flag = flask.request.form['flag']
        with open("/app/flags.json", "r") as f:
            flags = json.loads(f.read())

        if flag in list(flags.values()):
            i = list(flags.values()).index(flag)
            ids[flask.session["userid"]]["solved"].append(i)
            ids[flask.session["userid"]]["lastsolved"] = time.time()
            with open("users.json", "w") as f:
                f.write(json.dumps(ids, indent=4))
            return "<script>alert('right! congratulation!!');location='/';</script>"
        else:
            return "<script>alert('wrong... try again');history.go(-1);</script>"
        

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=9091, debug=True)
    except Exception as ex:
        logging.info(str(ex))
        pass
