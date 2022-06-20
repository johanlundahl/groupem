from flask import request, render_template, redirect, abort, url_for, session
from groupem.flask_app import FlaskApp
import random


app = FlaskApp(__name__)
app.secret_key = '5WCMvGdgSGIHL6nF3QJQ'


@app.route('/', methods=['GET'])
def entry():
    return render_template('index.html')


@app.route('/groups', methods=['POST', 'GET'])
def groups():
    if request.method == 'POST':
        if not all(x in request.form for x in ['names', 'group-size']):
            abort(400, 'missing required form parameters')

        if not request.form['group-size'].isdigit():
            abort(400, 'group size need to be a number')

        names = request.form['names'].split('\r\n')
        group_size = int(request.form['group-size'])

        random.shuffle(names)
        names = chunks(names, group_size)

        session['groups'] = names
        session['group-size'] = group_size
        return redirect(url_for("groups"))
    else:
        groups = session['groups']
        group_size = session['group-size']
        names = '\r\n'.join(['\r\n'.join(x) for x in groups])
        return render_template('groups.html',
                               groups=groups, names=names,
                               group_size=group_size)


def chunks(list, size):
    return [list[i:i + size] for i in range(0, len(list), size)]


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def error_page(e):
    return render_template("error-code.html",
                           response_status=e.description,
                           code=e.code), e.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
