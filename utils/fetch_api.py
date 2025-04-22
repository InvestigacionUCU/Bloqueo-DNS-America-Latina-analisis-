
from interfaces.i_execute import IExecute
import requests
from tenacity import retry, wait_exponential, stop_after_attempt, RetryError

class FetchAPI(IExecute):
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    @retry(wait=wait_exponential(), stop=stop_after_attempt(3), reraise=True)
    def execute(self, url: str):
        """Realiza la solicitud HTTP con manejo de errores y reintentos."""
        try:
            response = requests.get(url)
            response.raise_for_status() 
            return response.json()

        except requests.Timeout:
            print(f"Tiempo de espera agotado para {url}. Reintentando...")
            raise  

        except requests.TooManyRedirects:
            print(f"Demasiados redireccionamientos para {url}. Revisar la URL.")
            raise 

        except requests.RequestException as e:
            print(f"Error al consultar {url}: {e}. Reintentando...")
            raise  

        except Exception as e:
            print(f"Error inesperado: {e}. Deteniendo los intentos.")
            return None