from app.routes.auth import blueprint, tag


@blueprint.post("/logout", tags=[tag], responses={200: {}})
def logout():
    # Utilizando JWT quer dizer que nós não podemos revogar,
    # única maneira de impedir o acesso seria registrando
    # o JWT numa lista de bloqueado.
    #
    # Porém isto tira o maior propósito do JWT,
    # acelerar o processo de validação.
    return ("", 200)
