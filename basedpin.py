from flask import Flask, request, render_template, redirect, url_for
from wtforms import Form, BooleanField, StringField, validators
import dictionary
import database
import sqlite3


app = Flask(__name__)


class PasteForm(Form):
    paste = StringField('paste', [validators.Length(min=1, max=1000000), validators.DataRequired()])
    alias = StringField('alias', [validators.Length(min=1, max=30)])
    unlisted = BooleanField('unlisted', default=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form and request.method == 'POST':
        form = PasteForm(request.form)
        if form.validate():
            conn, cur = database.get()
            linkid = dictionary.get_string()

            with conn:
                try:
                    conn.execute( "INSERT INTO Pastes ('unlisted', 'contents', 'ip', 'userid', 'alias', 'linkid') VALUES (?, ?, ?, ?, ?, ?)",
                                    (bool(form.unlisted.data), form.paste.data, request.remote_addr, "userid", form.alias.data, linkid))
                except sqlite3.IntegrityError:
                    return "Non-unique id generated. Change this later to retry."

            return redirect(linkid)
        else:
            return "There was error validating your form."

    return render_template('index.html', pasted=False)


@app.route('/<pasteid>', methods=['GET'])
def get_paste(pasteid):
    conn, cur = database.get()
    cur.execute("SELECT contents, views, alias, timestamp FROM Pastes WHERE linkid=? LIMIT 1", (pasteid,))

    data = cur.fetchone()
    if not data:
        return "Paste not found."

    with conn:
        conn.execute("UPDATE Pastes set views = views + 1 WHERE linkid=?", (pasteid,))

    return render_template('paste.html', paste=data[0], alias=data[2], date=data[3], views=data[1])
