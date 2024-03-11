from flask import request, json, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with


from application.data.model import db, User


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('user_mail', type=str, required=True, help="user mail is required")
user_post_args.add_argument('password', type=str, required=True, help="password is required")

user_put_args = reqparse.RequestParser()
user_put_args.add_argument('user_mail', type=str)
user_put_args.add_argument('password', type=str)


resource_fields = {
    'user_id': fields.Integer,
    'user_mail': fields.String,
    'password': fields.String
}

class UserAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.filter_by(user_id = user_id).first()
        if not user:
            abort(404, message="no user exist with this user id")
        return user
    
    def delete(self, user_id):
        user = User.query.filter_by(user_id = user_id).first()
        if not user:
            abort(404, message="no user exist with this user id")
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status': "success",'message':'user is deleted' })

    @marshal_with(resource_fields)
    def put(self,user_id):
        args=user_put_args.parse_args()
        user=User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message="no user exist with this user id")
        if args["user_mail"]:
            user.user_mail=args["user_mail"]
        if args["password"]:
            user.password=args["password"]
        db.session.commit()

    
class AllUserAPI(Resource):
    def get(resource):
        users = User.query.all()
        all_user=[]
        for user in users:
            all_user.append({'user_id':user.user_id,
                             'user_mail': user.user_mail,
                             'password': user.password})
        return all_user

    def post(resource):
        args = user_post_args.parse_args()
        user = User.query.filter_by(user_mail = args["user_mail"]).first()
        if "@" not in args["user_mail"]:
            abort(409, message="user mail is not mail")
        if user:
            abort(409, message="user mail already exists")
        input = User(user_mail=args['user_mail'], password=args['password'])
        db.session.add(input)
        db.session.commit()
        return "user is registered", 200