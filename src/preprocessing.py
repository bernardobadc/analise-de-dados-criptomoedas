import ccxt
import pandas as pd

# Conectando com a API
BINANCE_API = ccxt.binance()


def get_coin_historic(coin: str, interval: str, time_limit: int) -> pd.DataFrame:
    """
    Obtém os dados históricos de preços de uma moeda a partir da API da Binance.

    Essa função consulta a API da Binance para obter o histórico de preços
    (open, high, low, close, volume) de uma criptomoeda e retorna um DataFrame com esses dados.
    Args:
        coin (str): Par de moedas (ex.: BTC/USDT).
        interval (str): Intervalo de tempo (ex.: '1d').
        time_limit (int): Número de dias para buscar (ex.: 365 para 12 meses).
    Returns:
        pd.DataFrame: DataFrame com os dados históricos.
    """

    # Armazenando os valores de open, high, low, close e volume da criptomoeda
    ohlcv = BINANCE_API.fetch_ohlcv(coin, timeframe=interval, limit=time_limit)

    # Transformando os dados retornados pela API em um DataFrame
    df = pd.DataFrame(ohlcv, columns=["data", "open", "high", "low", "close", "volume"])

    # Adicionando a coluna moeda
    df["moeda"] = coin

    # Mantendo apenas as colunas necessárias no dataframe
    df = df[["data", "moeda", "close"]]

    # Convertendo a coluna 'data' para datetime
    df["data"] = pd.to_datetime(df["data"], unit="ms")

    # Retornando o dataframe
    return df


def generate_coins_data(df: pd.DataFrame, coins: list) -> pd.DataFrame:
    """
    Obtém os dados históricos de múltiplas criptomoedas e os combina em um DataFrame.

    Esta função itera por uma lista de criptomoedas, coleta os dados históricos
    de cada uma usando a função `get_coin_historic`, e os adiciona ao DataFrame existente
    fornecido como entrada.

    Args:
        existing_data (pd.DataFrame): DataFrame onde os dados de cada moeda serão adicionados.
        coins (list): Lista de pares de moedas (ex.: ["BTC/USDT", "ETH/USDT", ...]) para as quais os dados serão coletados.

    Returns:
        pd.DataFrame: DataFrame atualizado contendo os dados históricos (data, moeda, preço de fechamento) de todas as moedas.

    Example:
        >>> updated_df = generate_coins_data(existing_df, ["BTC/USDT", "ETH/USDT"])
    """

    # Itera sobre cada moeda na lista fornecida
    for coin in coins:
        # Obtém os dados históricos para a moeda atual
        coin_data = get_coin_historic(coin, interval="1d", time_limit=700)

        # Adiciona os dados da moeda ao DataFrame existente
        df = pd.concat([df, coin_data], ignore_index=True)

    # Retorna o DataFrame atualizado com os dados de todas as moedas
    return df


def moving_average_calc(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a média móvel de 200 dias para o preço de fechamento de cada criptomoeda.

    Esta função adiciona uma nova coluna ao DataFrame fornecido, chamada 'media_movel_200',
    que contém a média móvel de 200 dias dos preços de fechamento para cada criptomoeda,
    calculada separadamente para cada grupo de moeda.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados históricos de preços das criptomoedas,
                             incluindo as colunas 'moeda' e 'close'.

    Returns:
        pd.DataFrame: DataFrame original com a nova coluna 'media_movel_200' contendo as médias móveis.

    Example:
        >>> df_with_ma = moving_average_calc(df)
    """

    # Calcular a média móvel de 200 dias para cada moeda
    data["media_movel_200"] = data.groupby("moeda")["close"].transform(
        lambda price_series: price_series.rolling(window=200).mean()
    )

    # Retornar o DataFrame com a coluna da média móvel
    return data


def mayer_multiple(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o Múltiplo de Mayer para o preço de fechamento do Bitcoin.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'close' (preço de fechamento)
                             e 'media_movel_200' (média móvel de 200 dias) para o Bitcoin.

    Returns:
        pd.DataFrame: DataFrame original com a nova coluna 'multiplo_de_mayer' calculada.

    Example:
        >>> df_with_mayer = mayer_multiple(df)
    """

    # Calculando o Múltiplo de Mayer: preço de fechamento / média móvel de 200 dias
    data["multiplo_de_mayer"] = data["close"] / data["media_movel_200"]

    # Retornando o DataFrame com a nova coluna calculada
    return data
