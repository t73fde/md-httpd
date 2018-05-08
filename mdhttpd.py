#!/usr/bin/env python

import datetime
import os
import os.path
import re
import sys

from flask import Flask, render_template, request, safe_join, redirect, \
    url_for, flash, abort
import markdown2

PY3 = sys.version_info[0] == 3

ROOT = os.path.expanduser("~/Sync/Mobil/notes")

app = Flask(__name__)
FILE_RE = re.compile("\A([a-z0-9_ -.!#]+)(\.md)\Z", re.IGNORECASE)
FILE_ENCODING = 'utf-8'


def get_filename(name):
    return safe_join(ROOT, name + ".md")


def get_info(name):
    try:
        return os.stat(get_filename(name))
    except OSError:
        return None


def read_data(name):
    try:
        with open(get_filename(name), "r") as f:
            if PY3:
                data = f.read()
            else:
                data = f.read().decode(FILE_ENCODING)
    except IOError:
        abort(404)
    return data


def write_data(name, data):
    try:
        with open(get_filename(name), "w") as f:
            if PY3:
                f.write(data)
            else:
                f.write(data.encode(FILE_ENCODING))
    except IOError:
        abort(404)


@app.route("/")
def index():
    infos = []
    for fname in os.listdir(ROOT):
        if fname[0] == '.':
            continue
        m = FILE_RE.match(fname)
        if not m:
            continue
        name = m.group(1)
        info = get_info(name)
        infos.append(
            {
                'name': name,
                'modified': datetime.datetime.fromtimestamp(info.st_mtime),
            })
    infos.sort(key=lambda i: i['name'])
    return render_template("index.html", infos=infos)


@app.route("/new", methods=['GET', 'POST'])
def do_new():
    name = ''
    if request.method == 'POST':
        name = request.form['name']
        if not FILE_RE.match(name + '.md'):
            flash('invalid note name')
        elif get_info(name):
            flash('note already exists')
        else:
            write_data(name, 'ENTER HERE')
            return redirect(url_for("do_edit", name=name))
    return render_template('do_new.html', name=name)


@app.route("/<path:name>/view")
@app.route("/<path:name>")
def do_view(name):
    return render_template(
        "do_view.html",
        name=name, content=markdown2.markdown(read_data(name)))


@app.route("/<path:name>/edit", methods=['GET', 'POST'])
def do_edit(name):
    if request.method == 'POST':
        data = request.form['data']
        if data != read_data(name):
            write_data(name, data)
            flash('note saved')
        else:
            flash('nothing changed')
        return redirect(url_for('do_view', name=name))
    return render_template("do_edit.html", name=name, data=read_data(name))


@app.route("/<path:name>/delete", methods=['GET', 'POST'])
def do_delete(name):
    if request.method == 'POST':
        try:
            os.remove(get_filename(name))
            flash('note deleted')
            return redirect(url_for('index'))
        except OSError:
            flash('unable to delete note')
    return render_template('do_delete.html', name=name)


if __name__ == "__main__":
    port = 0x6f6d
    debug = True

    if not debug or os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        # Otherwise, in reload mode this code would be executed twice...
        # See werkzeug.serving.run_with_reloader()
        import threading
        import webbrowser
        url = "http://localhost:%d" % port
        t = threading.Timer(1.0, webbrowser.open, [url])
        t.start()
    app.secret_key = 'not very secret'
    app.run(port=port, debug=debug)
