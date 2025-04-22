from utils.query import Query


class QueryRaw(Query):
    def __init__(self, query: Query):
        self.query = query
        
    def QueryRaw(self, measurement_uid: str) -> str:
        parametros = {
            "measurement_uid": measurement_uid
        }
        return self.query.build_query(parametros)
