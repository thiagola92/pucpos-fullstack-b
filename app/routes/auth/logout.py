from app.routes.auth import blueprint, tag
from app.routes.generic import generic200


@blueprint.post("/logout", tags=[tag], responses={200: generic200})
def logout():
    # Utilizando JWT quer dizer que nós não podemos revogar,
    # única maneira de impedir o acesso seria registrando
    # o JWT numa lista de bloqueado.
    #
    # Porém isto tira o maior propósito do JWT,
    # acelerar o processo de validação.
    return ("Acesso revogado", 200)
