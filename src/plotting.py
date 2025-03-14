import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Função para gerar o gráfico do Bitcoin
def plot_btc(df: pd.DataFrame) -> None:
    # Configuração do gráfico
    fig, ax1 = plt.subplots(figsize=(16, 9))

    # Gráfico para preço de fechamento e média móvel
    sns.lineplot(
        x="data",
        y="close",
        data=df,
        ax=ax1,
        label="Preço de Fechamento Bitcoin",
        color="blue",
    )
    sns.lineplot(
        x="data",
        y="media_movel_200",
        data=df,
        ax=ax1,
        label="Média Móvel Últimos 200 dias",
        color="orange",
    )

    # Criar o segundo eixo Y para o Múltiplo de Mayer
    ax2 = ax1.twinx()
    sns.lineplot(
        x="data",
        y="multiplo_de_mayer",
        data=df,
        ax=ax2,
        label="Múltiplo de Mayer",
        color="green",
    )

    # Configurações adicionais
    ax1.set_xlabel("Data")
    ax1.set_ylabel("Preço / Média Móvel (USDT)", color="blue")
    ax2.set_ylabel("Múltiplo de Mayer", color="green")

    # Ajustes de cores
    ax1.tick_params(axis="y", labelcolor="blue")
    ax2.tick_params(axis="y", labelcolor="green")

    # Título do gráfico
    plt.title("BITCOIN - Preço de Fechamento, Média Móvel e Múltiplo de Mayer")

    # Exibindo a legenda
    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")

    # Exibindo o gráfico
    plt.tight_layout()
    plt.savefig(r"images\btc_plot")
    plt.show()


# Função para gerar o gráfico da moeda Ethereum
def plot_eth(df: pd.DataFrame) -> None:
    # Configuração do gráfico
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Configuração do eixo de preço de fechamento
    sns.lineplot(
        x="data",
        y="close",
        data=df,
        ax=ax1,
        label="Preço de Fechamento",
        color="blue",
    )

    # Configuração do eixo de média móvel
    sns.lineplot(
        x="data",
        y="media_movel_200",
        data=df,
        ax=ax1,
        label="Média Móvel Últimos 200 dias",
        color="orange",
    )

    # Ajustando as labels
    ax1.set_xlabel("Data")
    ax1.set_ylabel("Preço de Fechamento / Média Móvel (USDT)")

    # Título do gráfico
    plt.title("ETHEREUM - Preço de Fechamento e Média Móvel")

    # Exibindo o gráfico
    plt.tight_layout()
    plt.savefig(r"images\eth_plot")
    plt.show()


# Função para gerar o gráfico com o preço de fechamento de todas as moedas
def plot_closing_prices(df: pd.DataFrame):
    # Configuração do gráfico
    plt.figure(figsize=(14, 8))

    # Lista de moedas únicas para iterar e plotar
    coins = df["moeda"].unique()

    # Paleta de cores para garantir que as moedas sejam representadas por cores distintas
    palette = sns.color_palette(
        "tab10", len(coins)
    )  # Usando uma paleta de 10 cores diferentes

    # Plotando o preço de fechamento para cada moeda
    for i, moeda in enumerate(coins):
        coin_data = df[df["moeda"] == moeda]

        # Preço de fechamento
        sns.lineplot(x="data", y="close", data=coin_data, label=moeda, color=palette[i])

    # Configurações do gráfico
    plt.title(
        "Preço de Fechamento das Criptomoedas (Solana, Xrp, Polkadot, Aave, Litecoin, Chainlink, Avax)"
    )

    # Configurando as labels
    plt.xlabel("Data")
    plt.ylabel("Preço (USD)")
    # Configurando as legendas para fora do gráfico
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Legenda fora do gráfico
    plt.tight_layout()
    plt.savefig(r"images\other_coins_close")
    # Exibindo o gráfico
    plt.show()


# Função para gerar o gráfico com a média móvel de 200 dias de todas as moedas
def plot_moving_averages(df: pd.DataFrame):
    # Configuração do gráfico
    plt.figure(figsize=(14, 8))

    # Lista de moedas únicas para iterar e plotar
    coins = df["moeda"].unique()

    # Paleta de cores para garantir que as moedas sejam representadas por cores distintas
    palette = sns.color_palette(
        "tab10", len(coins)
    )  # Usando uma paleta de 10 cores diferentes

    # Plotando a média móvel de 200 dias para cada moeda
    for i, moeda in enumerate(coins):
        coin_data = df[df["moeda"] == moeda]

        # Média móvel
        sns.lineplot(
            x="data",
            y="media_movel_200",
            data=coin_data,
            label=f"{moeda} - Média Móvel 200 dias",
            color=palette[i],
            linestyle="--",  # Linhas tracejadas para a média móvel
        )

    # Configurações do gráfico
    plt.title(
        "Média Móvel de 200 dias das Criptomoedas (Solana, Xrp, Polkadot, Aave, Litecoin, Chainlink, Avax)"
    )

    # Configurando as labels
    plt.xlabel("Data")
    plt.ylabel("Preço (USD) - Média Móvel")
    # Configurando as legendas pra fora do gráfico
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Legenda fora do gráfico
    plt.tight_layout()
    plt.savefig(r"images\other_coins_moving_average")
    # Exibindo o gráfico
    plt.show()
