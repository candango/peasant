from bastiontest import handlers
from firenado import tornadoweb


class BastiontestComponent(tornadoweb.TornadoComponent):

    def get_handlers(self):
        return [
            (r"/", handlers.GetHandler),
            (r"/delete", handlers.DeleteHandler),
            (r"/head", handlers.HeadHandler),
            (r"/options", handlers.OptionsHandler),
            (r"/patch", handlers.PatchHandler),
            (r"/post", handlers.PostHandler),
            (r"/put", handlers.PutHandler),
        ]
