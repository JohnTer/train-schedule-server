import os
import traceback
import logging
import projsettings
from logging.handlers import RotatingFileHandler
from model import Model
from time import strftime
from flask_login import LoginManager, login_user, login_required, current_user
from entity.user import User
from flask import Flask, request, abort, render_template, \
redirect, url_for



model = Model()
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''
app.config['SECRET_KEY'] = os.urandom(16)

handler = RotatingFileHandler(projsettings.LOG_NAME, 
                            maxBytes=projsettings.LOG_MAX_BYTES, 
                            backupCount=projsettings.LOG_BACKUP_COUNT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)




@login_manager.user_loader
def load_user(user_id):
    return User(user_id)  

@app.route('/protected')
@login_required
def protected():
    return "protected"


@app.route('/login', methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('get_search'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    password = request.form['password']
    login = request.form['login']
    result, id = model.auth_user(login, password)
    if result is None:
        abort(400)
    if result:
        login_user(User(id))
        return redirect(url_for('get_search'))
    else:
        return redirect(url_for('get_login'))



@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('get_login'))

@app.route('/search', methods=['GET'])
@login_required
def get_search():
    return render_template('search.html')


@app.route('/trainlist', methods=['GET'])
@login_required
def get_search_parameters():
    parameters = request.args.get('param')
    parameters = parameters.split(',')
    from_station = parameters[0]
    to_station = parameters[1]
    time_station = parameters[2]
    select = parameters[3]

    result, select = model.get_search_result(from_station, to_station, time_station, select)
    
    if result is None:
        abort(400)
    elif len(result) == 0:
        abort(404)
    search_param = [from_station, to_station, time_station]
    return render_template('trainlist.html', items=result, selected = select, search_param = search_param)

@app.route('/train', methods=['GET'])
@login_required
def get_train():
    parameters = request.args.get('fields')
    parameters = parameters.split(',')

    train_list, title = model.get_train_info(parameters[0],parameters[1])
    if train_list is None:
        abort(400)
    elif len(train_list) == 0:
        abort(404)
    return render_template('train.html', items=train_list, title = title)


@app.route('/location', methods=['GET'])
@login_required
def get_location():
    return render_template('location.html')


@app.route('/map', methods=['GET'])
@login_required
def post_location():
    parameters = request.args.get('fields')
    parameters = parameters.split(',')
    stationlist, img_path = model.get_map_info(parameters[0], parameters[1])
    if stationlist is None:
        abort(400)
    return render_template('map.html', items = stationlist, image = img_path)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('notfound.html')

@app.errorhandler(401)
def auth_guard(error):
    return redirect(url_for('get_login'))

@app.after_request
def after_request(response):
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.info('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500





