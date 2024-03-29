from flask_restful import Api, Resource, reqparse
from .models import User, Transaction
from .database import db
# from .controllers import raw
import datetime

def raw(text): # text = Transaction One
    split_list = text.split() #----> list ['Transaction', 'One']
    src_word = ''
    for word in split_list:
        src_word += word.lower()
    return src_word

api = Api()

parser = reqparse.RequestParser()

# defined and notified the api that I am going have a request body

parser.add_argument('t_name')
parser.add_argument('t_type')
parser.add_argument('s_city')
parser.add_argument('d_city')
parser.add_argument('description')

class TransApi(Resource):
    def get(self, user_id): # retrieve all trans of a particular user
        this_user = User.query.get(user_id)
        user_trans = this_user.trans # list of objects
        user_transactions = []  # list of dictionaries
        for trans in user_trans:  # trans_id, t_name, type, s_city, d_city, description 
            trans_details = {}
            trans_details["id"] = trans.id
            trans_details["name"] = trans.t_name
            trans_details["type"] = trans.t_type
            trans_details["source"] = trans.s_city
            trans_details["destination"] = trans.d_city
            trans_details["description"] = trans.decription
            user_transactions.append(trans_details)
        return user_transactions
    
    def post(self, user_id):
        trans_data = parser.parse_args()
        new_trans = Transaction(t_name = trans_data["t_name"], t_search_name = raw(trans_data["t_name"]), t_type = trans_data["t_type"], t_date = datetime.datetime.now(), s_city = trans_data["s_city"], d_city = trans_data["d_city"], decription = trans_data["description"], user_id = user_id)
        db.session.add(new_trans)
        db.session.commit()
        return "created succesfully", 201

    # def post(self): # create a transaction for a particular user

api.add_resource(TransApi, '/api/transactions/<int:user_id>')
