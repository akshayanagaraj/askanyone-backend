from flask import request, jsonify, current_app
import logging
from service.response import Response
from service.db_session import db_session
from service.db_service_v2 import DBService
from webargs.flaskparser import use_args
from webargs import fields
from datetime import datetime


def check():
    '''
    Checks whether the app is running and api connection works
    '''
    return Response.success('success', {'message':'Have a good day'})



def get_user_id():
    try:
        with db_session() as session:
            service = DBService(session, current_app.logger)
            context = {
                'username' : request.args.get('username'),
            }
            rs = service.get_result('get_user_id', context)
            result = [dict(row) for row in rs.fetchall()]
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'error in fetching results', 'error': str(e)}), 500
    print(result,'get user id response')
    return Response.success('success', result)      


@use_args(
    {
        "per_page":
        fields.Int(required=True),
        "page":
        fields.Int(required=True),
        "user_id":
        fields.Int(required=True),
        "status":
        fields.Str(required=True),
        "key":
        fields.Str(required=True),
        
    },
    location="query")
def get_questions(args):
    try:
        per_page,page,user_id,status,key = args['per_page'],args['page'],args['user_id'],args['status'],args['key']
        with db_session() as session:
            service = DBService(session, current_app.logger)
            offset = int(per_page) * (int(page) - 1)
                
            context = {
                'per_page': per_page,
                'page': page,
                "user_id": user_id,
                "offset": offset
                }
            result = []
            if key == "others":
                rs = service.get_result('get_all_questions_others', context)
                result = [dict(row) for row in rs.fetchall()]
            else:
                rs = service.get_result('get_all_questions_mine', context)
                result = [dict(row) for row in rs.fetchall()]
            print(result)
            for i in range(len(result)):
                context = {
                'per_page': per_page,
                'page': page,
                "user_id": user_id,
                "offset": offset,
                "question_id": result[i]['question_id']
                
                }
                comment_result = []
                print(result[i])
                rs = service.get_result('get_all_comments', context)
                comment_result = [dict(row) for row in rs.fetchall()]
                result[i]['comments'] = comment_result
                print(result[i])

                
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'error in fetching results', 'error': str(e)}), 500
    return Response.success('success', result)  


@use_args(
    {
        "per_page":
        fields.Int(required=True),
        "page":
        fields.Int(required=True),
        "user_id":
        fields.Int(required=True),
        "question_id":
        fields.Int(required=True), 
        
    },
    location="query")
def get_comments(args):
    try:
        per_page,page,user_id, question_id = args['per_page'],args['page'],args['user_id'],args['question_id']
        with db_session() as session:
            service = DBService(session, current_app.logger)
            offset = int(per_page) * (int(page) - 1)
                
            context = {
                'per_page': per_page,
                'page': page,
                "user_id": user_id,
                "offset": offset,
                "question_id": question_id
                
                }
            result = []
            
            rs = service.get_result('get_all_comments', context)
            result = [dict(row) for row in rs.fetchall()]
                
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'error in fetching results', 'error': str(e)}), 500
    return Response.success('success', result) 


@use_args({
    "title":
    fields.Str(required=True),
    "user_id":
    fields.Int(required=True),
    "question":
    fields.Str(required=True),

}, location="query")
def create_question(args):
    try:
        title, user_id, question = args['title'],args['user_id'],args['question']
        with db_session() as session:
            service = DBService(session, current_app.logger)
            context = {
                'title': title,
                'user_id': user_id,
                "question": question,
                "created_at": datetime.now()
                }
            
            
            rs = service.get_result('create_question', context)
           
                
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'error in fetching results', 'error': str(e)}), 500
    return Response.success('success', 'Question created') 


@use_args({
    "user_id":
    fields.Int(required=True),
    "comment":
    fields.Str(required=True),
    "question_id":
    fields.Int(required=True)
}, location="query")
def create_comment(args):
    try:
        user_id, question_id, comment = args['user_id'],args['question_id'], args['comment']
        with db_session() as session:
            service = DBService(session, current_app.logger)
            context = {
                
                'user_id': user_id,
                "question_id": question_id,
                "created_at": datetime.now(),
                "comment": comment
                }
            
            
            rs = service.get_result('create_comment', context)
           
                
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'error in fetching results', 'error': str(e)}), 500
    return Response.success('success', 'Comment created')     
