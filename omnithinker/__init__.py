from gevent.pywsgi import WSGIHandler

def neuter_monkey():
    """Fix a bug in flask_sockets' monkey-patching of WSGIHandler's logger."""
    def log_request(self):
        log = self.server.log
        if log:
            if hasattr(log, "info"):
                log.info(self.format_request())
            else:
                log.write(self.format_request() + "\n")
    WSGIHandler.log_request = log_request
