from flask import Blueprint
from askanyone_v1.controller import *

askanyone_v1 = Blueprint('asanyoe_v1', __name__)

askanyone_v1.add_url_rule(
    rule='/check',
    endpoint='check',
    view_func=check,
    methods= ['GET','POST']
    
)
askanyone_v1.add_url_rule(
    rule='/get_user_id',
    endpoint='get_user_id',
    view_func=get_user_id,
    methods= ['GET']
)

askanyone_v1.add_url_rule(
    rule='/get_questions',
    endpoint='get_questions',
    view_func=get_questions,
    methods= ['GET']
)

askanyone_v1.add_url_rule(
    rule='/get_comments',
    endpoint='get_comments',
    view_func=get_comments,
    methods= ['GET']
)

