from jinjasql import JinjaSql
from sqlalchemy import text
from functools import lru_cache
from typing import AnyStr, Dict, List, Any

jinja_sql = JinjaSql(param_style='named')

@lru_cache(maxsize=50)
def get_jinja_sql_query(query_id):
    with open(f'queries/{query_id}.jsql', 'r') as f:
        query_text = f.read()
    return query_text


class DBService:
    def __init__(self, connection, logger):
        self.conn = connection
        self.logger = logger

    def build_sql(self, query_id: AnyStr, context: Dict[AnyStr, Any]):
        query_text = get_jinja_sql_query(query_id)
        query, bind_params = jinja_sql.prepare_query(query_text, context)
        self.logger.debug('%s %s' % (query.replace('\n', ' '), bind_params))
        return query, bind_params

    def get_result(self, query_id: AnyStr, context: Dict[AnyStr, Any]):
        query, bind_params = self.build_sql(query_id, context)
        print(query, bind_params)
        rs = self.conn.execute(text(query), bind_params)
        return rs

    def insert_one(self, query: AnyStr, data: Dict[AnyStr, Any]):
        return self.conn.execute(text(query), data)

    def insert_many(self, query: AnyStr, data_list: List[Dict[AnyStr, Any]]):
        return self.conn.execute(text(query), data_list)

    def execute_query(self, query: AnyStr, data_dict: Dict[AnyStr, Any]):
        return self.conn.execute(text(query), data_dict)

    def execute(self, query_id: AnyStr, context: Dict[AnyStr, Any],
                data_dict: Dict[AnyStr, Any]):
        query, bind_params = self.build_sql(query_id, context)
        return self.execute_query(query, data_dict)