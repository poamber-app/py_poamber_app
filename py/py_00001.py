# Comment: request: werkzeug Request
handler: Handler class for this request
kw: keyword arguments from werkzeug URL routing patterns
    def __init__(self, request, handler, **kw):
        
        self.request = request
        self.handler = handler
        self.kwargs = kw
        self.headers_sent = False
        # Information to be logged about this query
        self.info = {
            "view": self.__class__.__name__,
            "ts_start": time.time(),
        }



# Comment: Return a dict with the configuration of the dataset named in
self.kwargs["name"]
    def get_dataset_config(self):
        
        name = self.kwargs["name"]
        self.info["dataset"] = name
        if not self.handler.server.cfg.has_section(name):
            raise NotFound("Dataset {} not found".format(name))
        return dict(self.handler.server.cfg.items(name))



# Comment: Return the arki.DatasetReader for the dataset named in
self.kwargs["name"]
    def get_dataset_reader(self):
        
        return arki.DatasetReader(self.get_dataset_config())



# Comment: Return the dataset query matcher string
    def get_query(self):
        
        query = self.request.values.get("query", "").strip()
        if query: self.info["query"] = query
        return query



# Comment: Return the sort order string
    def get_sort(self):
        
        sort = self.request.values.get("sort", "").strip()
        if sort: self.info["sort"] = sort
        return sort



# Comment: Return the file name to use in the Content-Disposition header.

None if the Content-Disposition header should not be sent
    def get_headers_filename(self):
        
        return getattr(self, "headers_filename", None)



# Comment: Send headers for a successful response
    def send_headers(self):
        
        self.info["ts_headers"] = time.time()
        self.handler.send_response(200)
        self.handler.send_header("Content-Type", self.content_type)
        fname = self.get_headers_filename()
        if fname is not None:
            self.handler.send_header("Content-Disposition", "attachment; filename=" + fname)
        self.handler.end_headers()
        self.handler.flush_headers()
        self.headers_sent = True



# Comment: Called in an exception handler, send a response to communicate the
exception.

If response headers have already been sent, then there is nothing we
can do, and just log the exception.
    def handle_exception(self):
        
        if not self.headers_sent:
            logging.exception("Exception caught before headers have been sent")
            ex = sys.exc_info()[1]
            # If the exception has code attribute, use for the status code
            code = getattr(ex, "code", 500)
            self.handler.send_response(code)
            self.handler.send_header("Content-Type", "text/plain")
            self.handler.send_header("Arkimet-Exception", str(ex))
            self.handler.end_headers()
            self.handler.flush_headers()
            self.handler.wfile.write(str(ex).encode("utf-8"))
            self.handler.wfile.write(b"\n")
        else:
            logging.exception("Exception caught after headers have been sent")



# Comment: Generate a response
    def run(self):
        
        try:
            self.stream()
            if not self.headers_sent:
                self.send_headers()
        except Exception:
            self.handle_exception()
        self.log_end()




# Comment: Base class for Django-CBV-style query handlers
class ArkiView:
    
    content_type = "application/octet-stream"

    def __init__(self, request, handler, **kw):
        """
        request: werkzeug Request
        handler: Handler class for this request
        kw: keyword arguments from werkzeug URL routing patterns
        """
        self.request = request
        self.handler = handler
        self.kwargs = kw
        self.headers_sent = False
        # Information to be logged about this query
        self.info = {
            "view": self.__class__.__name__,
            "ts_start": time.time(),
        }

    def get_dataset_config(self):
        """
        Return a dict with the configuration of the dataset named in
        self.kwargs["name"]
        """
        name = self.kwargs["name"]
        self.info["dataset"] = name
        if not self.handler.server.cfg.has_section(name):
            raise NotFound("Dataset {} not found".format(name))
        return dict(self.handler.server.cfg.items(name))

    def get_dataset_reader(self):
        """
        Return the arki.DatasetReader for the dataset named in
        self.kwargs["name"]
        """
        return arki.DatasetReader(self.get_dataset_config())

    def get_query(self):
        """
        Return the dataset query matcher string
        """
        query = self.request.values.get("query", "").strip()
        if query: self.info["query"] = query
        return query

    def get_sort(self):
        """
        Return the sort order string
        """
        sort = self.request.values.get("sort", "").strip()
        if sort: self.info["sort"] = sort
        return sort

    def get_headers_filename(self):
        """
        Return the file name to use in the Content-Disposition header.

        None if the Content-Disposition header should not be sent
        """
        return getattr(self, "headers_filename", None)

    def send_headers(self):
        """
        Send headers for a successful response
        """
        self.info["ts_headers"] = time.time()
        self.handler.send_response(200)
        self.handler.send_header("Content-Type", self.content_type)
        fname = self.get_headers_filename()
        if fname is not None:
            self.handler.send_header("Content-Disposition", "attachment; filename=" + fname)
        self.handler.end_headers()
        self.handler.flush_headers()
        self.headers_sent = True

    def handle_exception(self):
        """
        Called in an exception handler, send a response to communicate the
        exception.

        If response headers have already been sent, then there is nothing we
        can do, and just log the exception.
        """
        if not self.headers_sent:
            logging.exception("Exception caught before headers have been sent")
            ex = sys.exc_info()[1]
            # If the exception has code attribute, use for the status code
            code = getattr(ex, "code", 500)
            self.handler.send_response(code)
            self.handler.send_header("Content-Type", "text/plain")
            self.handler.send_header("Arkimet-Exception", str(ex))
            self.handler.end_headers()
            self.handler.flush_headers()
            self.handler.wfile.write(str(ex).encode("utf-8"))
            self.handler.wfile.write(b"\n")
        else:
            logging.exception("Exception caught after headers have been sent")

    def log_end(self):
        self.info["ts_end"] = time.time()
        logging.info("Query: %r", self.info, extra={"perf": self.info})

    def run(self):
        """
        Generate a response
        """
        try:
            self.stream()
            if not self.headers_sent:
                self.send_headers()
        except Exception:
            self.handle_exception()
        self.log_end()


class HTMLWriter:


# Comment: Move to a temporary directory while running the ArkiView
class TempdirMixin:
    
    def run(self):
        origdir = os.getcwd()
        try:
            with tempfile.TemporaryDirectory(prefix="arki-server-") as tmpdir:
                os.chdir(tmpdir)
                self.stream()
                if not self.headers_sent:
                    self.send_headers()
        except Exception:
            self.handle_exception()
        finally:
            os.chdir(origdir)
        self.log_end()


class ArkiDatasetQuery(TempdirMixin, ArkiView):


# Comment: Create the right view for a dataset query, given the `style` form value.
def arki_dataset_query(request, handler, **kw):
    
    style = request.values.get("style", "metadata").strip()
    View = get_view_for_style(style)
    return View(request, handler, **kw)




