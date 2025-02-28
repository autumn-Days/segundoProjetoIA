from generateInput import *
from SERIALIZER import *

"""
As linhas comentadas dizem respeito a quantidade a serialização dos dados para
o arquivo. NÃO É PARA RODAR ESSA PARTE DNV PQ VAI SOBRESCREVER OS DADOS.
As linhas descomentadas são um exemplo do uso de desserialização.
"""

#locals_:List[Tuple[int,int]] = genRandomLocals(60)
#eucDistancies = eucDistCartesianProduct(locals_)
#flows = genRandomFlows(60,120)

#mySerializer = DataHandler(locals_,eucDistancies, flows)
#mySerializer.serialize("PQA_DATA.txt")

locals2_ = []
eucDistancies2 = []
flows2 = []

myDesserializer = DataHandler(locals2_, eucDistancies2, flows2)
myDesserializer.deserialize("PQA_DATA.txt")


locals2_ = myDesserializer.locals_
eucDistancies2 = myDesserializer.eucDistancies
flows2 = myDesserializer.flows

print(locals2_)
print(eucDistancies2)
print(flows2)
