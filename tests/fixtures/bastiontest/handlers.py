from firenado import tornadoweb
import logging
from tornado.web import HTTPError

logger = logging.getLogger(__name__)


class HeadHandler(tornadoweb.TornadoHandler):

    def head(self):
        user_agent = self.request.headers.get("user-agent")
        if not user_agent:
            raise HTTPError(status_code=400)
            return
        self.add_header("head-response", "Head method response")
        self.add_header("user-agent", user_agent)


class DeleteHandler(tornadoweb.TornadoHandler):

    def delete(self):
        body = self.request.body
        self.add_header("request-body", body)
        self.write("Delete method output")


class GetHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("Get method output")


class OptionsHandler(tornadoweb.TornadoHandler):

    def options(self):
        body = "da body"
        self.add_header("request-body", body)
        self.write("Options method output")


class PatchHandler(tornadoweb.TornadoHandler):

    def patch(self):
        body = self.request.body
        self.add_header("request-body", body)
        self.write("Patch method output")


class PostHandler(tornadoweb.TornadoHandler):

    def post(self):
        body = self.request.body
        self.add_header("request-body", body)
        self.write("Post method output")


class PutHandler(tornadoweb.TornadoHandler):

    def put(self):
        body = self.request.body
        self.add_header("request-body", body)
        self.write("Put method output")
