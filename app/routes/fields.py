import sys

from pydantic import Field

plan_description = """[Bit field](https://en.wikipedia.org/wiki/Bit_field) para indicar os planos dos imóveis os quais está buscando.  
1 - Imóveis à venda  
2 - Imóveis para alugar  
---  
"""

type_description = """[Bit field](https://en.wikipedia.org/wiki/Bit_field) para indicar os tipos de imóveis os quais está buscando.  
1 - Casa  
2 - Apartamento  
---  
"""

AccountField = Field(1, description="O Identificador da conta.", gt=0)
PropertyField = Field(1, description="O Identificador do imóvel.", gt=0)
PlanField = Field(1, description="O plano do imóvel.", gt=0, lt=3)
TypeField = Field(1, description="O tipo de imóvel.", gt=0, lt=3)
PriceField = Field(
    1, description="O preço do imóvel (mínimo de 1 real).", gt=0, lt=sys.maxsize
)
StreetField = Field("", description="A rua do imóvel.")

PlanBitField = Field(0, description=plan_description, gt=-1, lt=4)
TypeBitField = Field(0, description=type_description, gt=-1, lt=4)
