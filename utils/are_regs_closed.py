from os import environ
from datetime import datetime

def are_regs_closed():
    date_string = environ.get("EndOfReg")
    date = datetime.strptime(date_string, "%d.%m.%Y")

    if date > datetime.now():
        return False
    else:
        return True