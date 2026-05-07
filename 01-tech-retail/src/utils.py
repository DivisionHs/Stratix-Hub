import unicodedata

def remover_acentos(txt):
    """
    Normaliza strings removendo acentos e caracteres especiais.
    Args:
        txt (str): Texto original (ex: "Placa de Vídeo").
    Returns:
        str: Texto normalizado (ex: "Placa de Video").
    """
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

def limpar_monetario(valor):
    """
    Converte valores monetários para float, lidando com:
    - Padrão BR: "1.250,50"
    - Padrão 'meio termo': "366.3"
    - Tipos numéricos diretos
    """
    if valor is None or str(valor).strip() == "":
        return 0.0

    if isinstance(valor, (int, float)):
        return float(valor)

    v = str(valor).replace("R$", "").strip()

    # Se houver vírgula, tratamos como padrão brasileiro (1.200,50 ou 1250,50)
    if ',' in v:
        v = v.replace('.', '').replace(',', '.')
    # Se NÃO houver vírgula, mas houver UM ponto:
    # Verificamos se é decimal (ex: 366.3) ou milhar (ex: 1.250)
    elif '.' in v:
        partes = v.split('.')
        # Se após o ponto houver 1 ou 2 dígitos, é decimal (366.3 ou 366.30)
        if len(partes[-1]) <= 2:
            pass  # mantém o ponto como está
        else:
            v = v.replace('.', '')  # era ponto de milhar (ex: 1.000.000)

    try:
        return float(v)
    except ValueError:
        return 0.0