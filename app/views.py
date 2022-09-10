from flask.views import MethodView
from models import Message, User
from validator import validate
from shcema import USER_CREATE, MESSAGE_CREATE
from flask import jsonify, request
from hashlib import md5
from sqlalchemy import asc

from app import app
from errors import AuthError
from auth import check_token


@app.route('/health/', methods=['GET', ])
def health():
    return {'status': 'OK'}


class RegisterView(MethodView):

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.add()
        return jsonify({'token': user.token})


class LoginView(MethodView):
   def post(self):
        name = request.json['name']
        password = request.json['password']
        
        if name is None or password is None:
            return jsonify({'message': 'Bad Request'}), 400

        user = User.by_name(name)
        hash_password = md5(password.encode()).hexdigest()
        if  user.password != hash_password:
            raise AuthError

        return jsonify({'token': user.token})        


class MessageView(MethodView):
    # @validate('json', MESSAGE_CREATE)
    def post(self):
        if 'Authorization' not in request.headers:
            raise AuthError

        token = str.split(request.headers['Authorization'], '_', 1)[1]
        if not check_token(token):
            return jsonify({'message': 'Invalid auth token'}), 401

        user = User.by_token(token)

        if user is None:
            return jsonify({'message': 'User not Found'}), 404

        txt_message = request.json['message']
        txt_parsed = str.split(txt_message, ' ')
        if len(txt_parsed) == 2 and txt_parsed[0] == 'history' and txt_parsed[1].isnumeric():
            txt_count = int(txt_parsed[1])
            db_result = Message.query.order_by(asc(Message.created_at)).all()
            msg_list = [m.to_dict() for m in db_result]
            return jsonify(msg_list[-txt_count:]), 200


        new_message = Message(**request.json)
        new_message.add()
        return jsonify(new_message.to_dict())


app.add_url_rule(
    '/register',
    view_func=RegisterView.as_view('users_register'),
    methods=['POST', ])
app.add_url_rule(
    '/login',
    view_func=LoginView.as_view('users_login'),
    methods=['POST', ])
app.add_url_rule(
    '/message',
    view_func=MessageView.as_view('messages'),
    methods=['POST', ])
