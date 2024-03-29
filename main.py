import http
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
def appendEvent(**kwargs):
    new_event = EventsLucky(**kwargs)
    DBase.session.add(new_event)
    DBase.session.commit()


def updateEvent(**kwargs):
    event = EventsLucky()
    # /* NAME */
    if kwargs.get('event_name'):
        event.event_name = kwargs['event_name']
    # /* START */
    elif kwargs.get("event_start"):
        event.event_start = kwargs['event_start']
    # /* END */
    elif kwargs.get("event_end"):
        event.event_end = kwargs['event_end']
    # /* OPEN */
    elif isinstance(kwargs.get("open"), bool):
        event.open = kwargs['open']
    # /* WILL OPEN */
    elif kwargs.get('will_open'):
        event.will_open = kwargs['will_open']

    # /* success: commit */
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
    event_start = DBase.Column(DBase.Float, nullable=False)
    event_end = DBase.Column(DBase.Float, nullable=False)
    open = DBase.Column(DBase.Boolean, unique=False, default=True)
    will_open = DBase.Column(DBase.Float, nullable=True, default=time())
    event_price = DBase.Column(DBase.Float, nullable=True, default=DEFAULT_PRICE)

    def __repr__(self):
        return "<Event %r>" % self.event_id


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
    if not n_event:
        return jsonify({"success": False})
    if n_event == "rasta":
        event = EventsLucky.query.filter_by(event_name=n_event).first()
    elif n_event == "alpha":
        event = EventsLucky.query.filter_by(event_name=n_event).first()
    elif n_event == "product":
        event = EventsLucky.query.filter_by(event_name=n_event).first()
    else:
        return jsonify({"success": False})
    # /* DONE */
    return jsonify({"success": True, "event_time": ctime(event.event_end),
                    "title_event": titleEventTime(event.event_start, event.event_end)[0]})


# /* API REQUEST: TEXT/HTML */
@mainApp.route("/eventhtml", methods=['POST'])
def eventData():
    tmp: str = ""
    # /* may kwargs will be empty */
    kwargs: dict = {}
    if request.cookies.get("anonymous") and request.cookies.get("for_event"):  # session.get('player'):
        if request.form.get("type") == '1':
            tmp = ""
        elif request.form.get("type") == '2':
            tmp = "ltmp/event_registerL1.html"
        elif request.form.get("type") == '3':
            tmp = "ltmp/event_registerL2.html"
            # /* get price of event
            event_price = EventsLucky.query.filter_by(event_name=request.cookies['for_event']).first().event_price
            kwargs.update(event=request.cookies.get('for_event'), event_price=event_price)

        else:
            return render_template_string("<h1>none</h1>")

        return render_template(tmp, **kwargs)


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
        location = ""  # same page (reload)
        verify_policy = request.form.get('accept')
        type_pay = request.form.get('type_pay')
        print(type_pay, verify_policy)
        if verify_policy == "true":
            if type_pay == "1":
                # /* BIT */
                location = "https://www.bitpay.co.il/he"
            elif type_pay == "2":
                # /* FREE CREDIT */
                location = "https://www.google.com"
            return jsonify({'success': True, "location":location})
        else:
            return jsonify({"success":False, "des": "הבקשה נכשלה"})
    else:
        # /* wtf with the request */
        return jsonify({"success": False, "des": "הבקשה נכשלה"})

    # TODO: save on db, create session
    # /* success */
    return jsonify({"success": True})


# /* INDEXES: ALL */
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
    # /* verify request user */
    if not request.cookies.get('anonymous'): return redirect(url_for("Index"))
    # /* verify request user is login or nope */
    register = session.get('player') and not request.cookies.get("anonymous")

    # /* select from db the price of event */
    event = EventsLucky.query.filter_by(event_name='rasta').first()
    # /* make response: DONE */
    res = make_response(render_template('rasta.html', event="rasta", register=register, event_price=event.event_price))
    res.set_cookie(key='for_event', value='rasta', httponly=True)
    return res


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
        # /* CONFIGURATion at a first time */
        if not EventsLucky.query.first():
            appendEvent(event_name="rasta", event_start=time(), event_end=time() + EManager.rasta_time)
            appendEvent(event_name="alpha", event_start=time(), event_end=time() + EManager.alpha_time)
            appendEvent(event_name="product", event_start=time(), event_end=time() + EManager.product_time)
            print("* append Events: (first config)")

    mainApp.run(host="0.0.0.0", port=43556, debug=True)
