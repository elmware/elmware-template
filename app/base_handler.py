import settings


field_keys = [
    "test",
    "res",
    "elm",
    "func",
    "inputs",
    "db_creates",
    "db_updates",
    "db_deletes",
    "output_message",
    "output_link",
    "input_fields",
    "file_upload",
    "next_function",
]


class BaseHandler:
    def __init__(self, res, elm, test=False):
        self.test = test
        self.res = res
        self.elm = elm
        self.func = res.get("func", "")
        self.arg = False
        if len(self.func.split('_')) > 2:
            self.arg = self.func.split('_')[2]
        self.inputs = res.get("inputs", {})
        self.db_creates = []
        self.db_updates = []
        self.db_deletes = []
        self.output_message = ""
        self.output_link = ""
        self.input_fields = []
        self.file_upload = False
        self.next_function = False
        # modify this to test
        self.to_test = settings.TO_TEST

    @staticmethod
    def download_file(url, name):
        local_filename = "{0}/{1}".format(settings.SCRATCH_DIR, name)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return local_filename

    def process(self):
        getattr(self, self.func.split("_")[1])()

    def use_nested_handler(self, handler):
        nh = handler(self.res, self.elm, test=self.test)
        nh.process()
        self.load_from_nested_handler(nh)

    def load_from_nested_handler(self, handler):
        for f in field_keys:
            setattr(self, f, getattr(handler, f))

    def build_continue(self):
        if self.next_function == False:
            return False
        output = dict(func=self.next_function)
        if self.file_upload:
            output["file_upload"] = True
        if self.input_fields:
            output["inputs"] = self.input_fields
        return output

    def output(self):
        self.process()
        return self.elm.end_run(
            message=self.output_message,
            link=self.output_link,
            db_creates=self.db_creates,
            db_updates=self.db_updates,
            db_deletes=self.db_deletes,
            continue_run=self.build_continue(),
        )
