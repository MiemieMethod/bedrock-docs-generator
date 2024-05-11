import json

from command.generator import *
from table.generator import *
from protocol.generator import *
from script.generator import *
from data_driven.generator import *


if __name__ == '__main__':
    print(CommandGenerator().generate())
    print(TableGenerator().generate())
    protocolPageList = ProtocolGenerator().generate()
    print(protocolPageList[0])
    print(protocolPageList[1])
    print(ScriptAPIGenerator().generate())
    print(BlockceptionSchemaGenerator().generate())
    print(BEDWSchemaGenerator().generate())

