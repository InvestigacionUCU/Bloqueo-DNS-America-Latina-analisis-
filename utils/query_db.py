from utils.query import Query


class QueryDB(Query):
    def __init__(self, query: Query, limit: int, anomaly: bool):
        self.query = query
        self.limit = limit
        self.anomaly = anomaly
        
    def query_db(self) -> str:
        parametros = {
            "probe_cc": self.query.probe_cc,
            "probe_asn": self.query.probe_asn,
            "since": self.query.since,
            "until": self.query.until,
            "limit": self.limit,  
            "anomaly": self.anomaly,
            "test_name": self.query.test_name,
            "domain": self.query.domain,
            "input": self.query.input,
            "ooni_run_link_id": self.query.ooni_run_link_id,
            "category_code": self.query.category_code,
        }
        return self.query.build_query(parametros)
