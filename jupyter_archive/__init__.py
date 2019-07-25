from notebook.utils import url_path_join
from .handlers import ZipHandler


# Jupyter Extension points
def _jupyter_server_extension_paths():
    return [{'module': 'jupyter_archive'}]


def load_jupyter_server_extension(nbapp):
    base_url = url_path_join(nbapp.web_app.settings['base_url'], 'zip-download')
    handlers = [(base_url, ZipHandler)]
    nbapp.web_app.add_handlers('.*', handlers)
    nbapp.log.info("jupyter_archive is enabled.")