from bastiontest import handlers
from firenado import tornadoweb


class BastiontestComponent(tornadoweb.TornadoComponent):

    def get_handlers(self):
        return [
            (r"/", handlers.IndexHandler),
        ]
