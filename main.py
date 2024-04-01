import json

from command.generator import *
from table.generator import *


if __name__ == '__main__':
    print(CommandGenerator().generate())
    print(TableGenerator().generate())
