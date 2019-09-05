from base_handler import BaseHandler
from base_error import BaseError
from utils import gen_simple_ss
import datetime, json


class MainHandler(BaseHandler):
    def start(self):
        self.input_fields.append(
            dict(
                name="mode",
                options=[
                    ["add", "add"],
                    ["update", "update"],
                    ["delete", "delete"],
                    ["list", "list"],
                    ["check", "check"]
                ],
            )
        )
        self.next_function = "master_choose"
        self.output_message = "choose your mode"

    def choose(self):
        mode = self.inputs.get("mode", "")
        if self.test:
            mode = "check"
        if mode == "update":
            self.input_fields.append(dict(name="key"))
            self.input_fields.append(dict(name="value"))
            self.next_function = "master_update"
            self.output_message = "enter an update"
        elif mode == "add":
            self.input_fields.append(dict(name="key"))
            self.input_fields.append(dict(name="value"))
            self.next_function = "master_add"
            self.output_message = "enter a new key value pair"
        elif mode == "check":
            self.input_fields.append(dict(name="key"))
            self.next_function = "master_check"
            self.output_message = "enter a key to check"
        elif mode == 'delete':
            self.input_fields.append(dict(name="key"))
            self.next_function = "master_delete"
            self.output_message = "enter a key to delete"
        elif mode == "list":
            fname = self.generate_program_list()
            self.output_link = self.elm.file_download_link(fname, "results.csv")
        else:
            self.output_message = "invalid selection"

    def generate_program_list(self):
        data = self.elm.db_read(1, [])
        titles = ["key", "value"]
        output = [titles]
        for d in data:
            output.append([d.get("key", ''), d.get("value", '')])
        return gen_simple_ss(output)

    def check(self):
        if self.test:
            pk = "test"
        pk = self.inputs.get("key", "")
        if not pk:
            self.output_message = "no  key entered"
            return False
        check  = self.elm.db_read(1, ["key", "eq", pk])
        if not check:
            self.output_message = "No value for this key"
            if self.test:
                print("done")
            return False
        self.output_message = "The value for this key is {0}.  Is this correct.  If no, it will be deleted".format(check[0].get("value", ""))
        self.input_fields.append(
            dict(
                name="choice",
                options=[
                    ["yes", "yes"],
                    ["no", "no"],
                ],
            )
        )
        self.next_function = "master_checkfollowup_{0}".format(pk)

    def checkfollowup(self):
        self.output_message = "Checker finished"
        if self.inputs.get("choice", "") == "no":
            query = ["key", "eq", self.arg]
            self.db_deletes.append(
                dict(table=1, query=query)
            )




    def delete(self):
        pk = self.inputs.get("key", "")
        if not pk:
            self.output_message = "no program key entered"
            return False
        query = ["key", "eq", pk]
        self.db_deletes.append(
            dict(table=1, query=query)
        )
        self.output_message = "deleted"



    def update(self):
        pk = self.inputs.get("key", "")
        value = self.inputs.get("value", "")
        if not pk:
            self.output_message = "no  key entered"
            return False
        query = ["key", "eq", pk]
        self.db_updates.append(
            dict(table=1, query=query, update=dict(value=value))
        )
        self.output_message = "updated"

    def add(self):
        pk = self.inputs.get("key", "")
        value = self.inputs.get("value", "")
        if not pk:
            self.output_message = "no  key entered"
            return False
        check  = self.elm.db_read(1, ["key", "eq", pk])
        if check:
            self.output_message = "key already exists"
            return False
        self.db_creates.append(
            dict(table=1, data=dict(key=pk, value=value))
        )
        self.output_message = "added"





def load_full_handler_map():
    return {"master": MainHandler}
