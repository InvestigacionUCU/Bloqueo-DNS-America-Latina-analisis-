from interfaces.i_query import IQuery
from interfaces.i_query_builder import IQueryBuilder
from utils.query import Query


class QueryBuilder(IQueryBuilder):
    def __init__(self):
        self.query = Query(base_url="")

    def set_base_url(self, base_url: str) -> 'IQueryBuilder':
        self.query.base_url = base_url
        return self

    def set_test_name(self, test_name: str) -> 'IQueryBuilder':
        self.query.test_name = test_name
        return self

    def set_probe_cc(self, probe_cc: str) -> 'IQueryBuilder':
        self.query.probe_cc = probe_cc
        return self

    def set_since(self, since: str) -> 'IQueryBuilder':
        self.query.since = since
        return self

    def set_until(self, until: str) -> 'IQueryBuilder':
        self.query.until = until
        return self

    def set_ooni_run_link_id(self, ooni_run_link_id: int) -> 'IQueryBuilder':
        self.query.ooni_run_link_id = ooni_run_link_id
        return self

    def set_probe_asn(self, probe_asn: int) -> 'IQueryBuilder':
        self.query.probe_asn = probe_asn
        return self

    def set_domain(self, domain: str) -> 'IQueryBuilder':
        self.query.domain = domain
        return self

    def set_input(self, input: str) -> 'IQueryBuilder':
        self.query.input = input
        return self

    def set_category_code(self, category_code: str) -> 'IQueryBuilder':
        self.query.category_code = category_code
        return self

    def build(self) -> 'Query':
        return self.query
