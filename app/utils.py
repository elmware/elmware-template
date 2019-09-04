import settings
import binascii, os
from openpyxl.workbook import Workbook


def create_hash():
    return binascii.b2a_hex(os.urandom(17))


def gen_simple_ss(data):
    wb = Workbook()
    ws = wb.get_active_sheet()
    fname = "{0}.xlsx".format(create_hash())
    for i in range(len(data)):
        for j in range(len(data[i])):
            ws.cell(row=i + 1, column=j + 1).value = data[i][j]
    wb.save(filename=os.path.join(settings.SCRATCH_DIR, fname))
    return fname
