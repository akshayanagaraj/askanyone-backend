from jinjasql import JinjaSql


class DBService:
    jinja_sql = JinjaSql()

    def __init__(self, connection):
        self.conn = connection

    def get_jsql_query(self, query_id):
        with open(f'queries/{query_id}.jsql', 'r') as f:
            query_text = f.read()
        return query_text

    def get_result(self, query_id, context):
        query_text = self.get_jsql_query(query_id)
        query, bind_params = self.jinja_sql.prepare_query(query_text, context)
        print(query.replace('\n', ' '), bind_params)

        rs = self.conn.execute(query, *bind_params)
        return rs

    def execute(self, query_id, context):
        query_text = self.get_jsql_query(query_id)
        query, bind_params = self.jinja_sql.prepare_query(query_text, context)
        print(query.replace('\n', ' '), bind_params)
        return self.conn.execute(query, *bind_params)
