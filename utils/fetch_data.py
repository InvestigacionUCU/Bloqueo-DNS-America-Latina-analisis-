from utils.fetch_api import FetchAPI


def fetch_data(query_db: str):
    """Obtiene los datos de la URL usando la clase FetchAPI."""
    fetcher = FetchAPI()  
    data = fetcher.execute(query_db) 
    return data
