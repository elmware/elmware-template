from elmsdk import ELMSDK
import sys
import traceback
from handlers import load_full_handler_map
from base_error import BaseError


def function_handler(res, elm, test):
    # functions here
    func = res.get("func", "")
    handler = load_full_handler_map().get(func.split("_")[0], False)
    if handler is False:
        return elm.end_run(message="Invalid Input")
    hanlder_instance = handler(res, elm, test=test)
    return hanlder_instance.output()


def run_app(key, test):
    if test:
        elm = ELMSDK(key, dev_mode=True)
        elm.setup_dev_run(test)
    else:
        elm = ELMSDK(key, dev_mode=False)
    while True:
        try:
            res = elm.begin_run()
            if res.get("func", "") == "":
                break
            function_handler(res, elm, test)
        except Exception as e:
            error_message = traceback.format_exc()
            elm.report_error(error_message)
            break


if __name__ == "__main__":
    key = sys.argv[1]
    test = False
    if len(sys.argv) >= 3 and sys.argv[2] != "0":
        test = sys.argv[2]
    run_app(key, test)
