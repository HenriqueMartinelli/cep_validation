def get_value_by_possible_keys(data: dict, possible_keys: list) -> str:
    """
    Busca o valor no dicionário usando uma lista de chaves possíveis.

    :param data: Dicionário com os dados.
    :param possible_keys: Lista de possíveis nomes de chave.
    :return: Valor encontrado ou None se nenhuma chave existir.
    """
    for key in possible_keys:
        if key in data:
            return data[key]
    return None
