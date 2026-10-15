# ============================================================
# LOTERIA LAB 2.0 - RESULTADOS ONLINE + ANÁLISE ESTATÍSTICA
# Google Colab | Python
# ============================================================

!pip -q install requests pandas matplotlib ipywidgets

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from math import comb
from collections import Counter
from datetime import datetime

BASE = "https://servicebus2.caixa.gov.br/portaldeloterias/api"

JOGOS = {
    "Mega-Sena":   {"slug": "megasena", "universo": 60, "dezenas": 6},
    "Lotofácil":   {"slug": "lotofacil", "universo": 25, "dezenas": 15},
    "Quina":       {"slug": "quina", "universo": 80, "dezenas": 5},
    "Lotomania":   {"slug": "lotomania", "universo": 100, "dezenas": 20},
}

sessao = requests.Session()
sessao.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://loterias.caixa.gov.br",
    "Referer": "https://loterias.caixa.gov.br/"
})

def consultar(url):
    resposta = sessao.get(url, timeout=20)
    resposta.raise_for_status()
    return resposta.json()

def obter_historico(nome, quantidade):
    slug = JOGOS[nome]["slug"]

    # Primeiro consulta o concurso mais recente
    ultimo = consultar(f"{BASE}/{slug}")
    numero_atual = int(ultimo["numero"])

    resultados = []

    # Recupera concursos anteriores, começando pelo mais recente
    for numero in range(
        numero_atual,
        max(0, numero_atual - quantidade),
        -1
    ):
        try:
            if numero == numero_atual:
                item = ultimo
            else:
                item = consultar(f"{BASE}/{slug}/{numero}")

            dezenas = item.get("listaDezenas")

            if not dezenas:
                continue

            resultados.append({
                "Concurso": int(item["numero"]),
                "Data": item.get("dataApuracao", ""),
                "Dezenas": sorted(int(x) for x in dezenas)
            })

        except Exception as erro:
            print(f"Aviso: concurso {numero} não foi obtido: {erro}")

    if not resultados:
        raise RuntimeError(
            "Não foi possível obter resultados. "
            "A fonte pode estar indisponível ou bloquear o acesso do Colab."
        )

    return sorted(resultados, key=lambda x: x["Concurso"])

def analisar(nome, quantidade, numero_jogos, criterio):
    regra = JOGOS[nome]
    universo = regra["universo"]
    qtd_dezenas = regra["dezenas"]

    historico = obter_historico(nome, quantidade)
    contador = Counter(
        dezena
        for concurso in historico
        for dezena in concurso["Dezenas"]
    )

    ranking = pd.DataFrame({
        "Dezena": range(0 if nome == "Lotomania" else 1, universo + 1)
    })

    ranking["Ocorrências"] = ranking["Dezena"].map(
        lambda n: contador[n]
    )

    total_concursos = len(historico)
    ranking["Frequência (%)"] = (
        ranking["Ocorrências"] / total_concursos * 100
    )

    print(f"\n{'=' * 55}")
    print(f"🎯 LOTERIA LAB | {nome}")
    print(f"{'=' * 55}")
    print(f"Concursos obtidos: {total_concursos}")
    print(f"Último concurso: {historico[-1]['Concurso']}")
    print(f"Data: {historico[-1]['Data']}")
    print("Últimas dezenas sorteadas:",
          " - ".join(f"{n:02d}" for n in historico[-1]["Dezenas"]))

    print("\n🔥 DEZENAS MAIS FREQUENTES")
    display(ranking.sort_values(
        ["Ocorrências", "Dezena"], ascending=[False, True]
    ).head(10).round(2))

    print("\n❄️ DEZENAS MENOS FREQUENTES")
    display(ranking.sort_values(
        ["Ocorrências", "Dezena"], ascending=[True, True]
    ).head(10).round(2))

    # Gráfico de frequência
    plt.figure(figsize=(13, 4))
    plt.bar(ranking["Dezena"], ranking["Ocorrências"])
    plt.title(f"Frequência histórica — {nome}")
    plt.xlabel("Dezena")
    plt.ylabel("Número de aparições")
    plt.xticks(ranking["Dezena"])
    plt.grid(axis="y", alpha=0.25)
    plt.show()

    # Probabilidade teórica de acertar todas as dezenas
    combinacoes = comb(universo, qtd_dezenas)
    print(f"\n📐 Combinações possíveis: {combinacoes:,}".replace(",", "."))
    print(f"Chance de acertar todas em uma aposta simples: "
          f"1 em {combinacoes:,}".replace(",", "."))

    # Gerador de combinações
    dezenas_disponiveis = ranking["Dezena"].to_numpy()

    if criterio == "Frequência histórica":
        # Suavização: evita peso zero para dezenas pouco sorteadas.
        pesos = ranking["Ocorrências"].to_numpy(dtype=float) + 1
        pesos = pesos / pesos.sum()
    else:
        pesos = np.ones(len(dezenas_disponiveis))
        pesos = pesos / pesos.sum()

    print("\n🎲 JOGOS GERADOS PARA ANÁLISE")
    jogos_gerados = set()

    while len(jogos_gerados) < numero_jogos:
        sorteio = np.random.choice(
            dezenas_disponiveis,
            size=qtd_dezenas,
            replace=False,
            p=pesos
        )
        jogos_gerados.add(tuple(sorted(int(n) for n in sorteio)))

    for i, jogo in enumerate(sorted(jogos_gerados), 1):
        print(f"Jogo {i:02d}: " + " - ".join(f"{n:02d}" for n in jogo))

    # Salvar resultados e frequência em arquivos
    pd.DataFrame([
        {
            "Concurso": h["Concurso"],
            "Data": h["Data"],
            **{
                f"Dezena_{i+1}": n
                for i, n in enumerate(h["Dezenas"])
            }
        }
        for h in historico
    ]).to_csv("historico_loteria.csv", index=False)

    ranking.to_csv("frequencia_loteria.csv", index=False)

    pd.DataFrame([
        {"Jogo": i, "Dezenas": " ".join(f"{n:02d}" for n in jogo)}
        for i, jogo in enumerate(sorted(jogos_gerados), 1)
    ]).to_csv("jogos_gerados.csv", index=False)

    print("\n📁 Arquivos criados:")
    print("- historico_loteria.csv")
    print("- frequencia_loteria.csv")
    print("- jogos_gerados.csv")
    print("\n⚠️ Frequência passada não prevê o próximo resultado.")
    print("Todas as combinações válidas têm a mesma chance "
          "em um sorteio justo.")

# Interface interativa
selecao = widgets.Dropdown(
    options=list(JOGOS.keys()),
    value="Mega-Sena",
    description="Loteria:"
)

concursos = widgets.IntSlider(
    value=100, min=10, max=500, step=10,
    description="Histórico:",
    continuous_update=False
)

qtd_jogos = widgets.IntSlider(
    value=5, min=1, max=30,
    description="Jogos:",
    continuous_update=False
)

criterio = widgets.Dropdown(
    options=["Aleatório", "Frequência histórica"],
    value="Aleatório",
    description="Método:"
)

botao = widgets.Button(
    description="🔄 Buscar e analisar",
    button_style="success"
)

saida = widgets.Output()

def executar(_):
    with saida:
        clear_output(wait=True)
        botao.disabled = True
        try:
            print("Conectando à fonte de resultados...")
            analisar(
                selecao.value,
                concursos.value,
                qtd_jogos.value,
                criterio.value
            )
        except Exception as erro:
            print("\n❌ Não foi possível concluir a análise.")
            print("Detalhe:", str(erro))
            print(
                "\nVerifique a conexão e tente novamente. "
                "A fonte pode estar indisponível ou bloquear o Colab."
            )
        finally:
            botao.disabled = False

botao.on_click(executar)

display(widgets.HTML("<h2>🎯 LOTERIA LAB 2.0</h2>"))
display(widgets.HTML(
    "<p>Resultados online, estatísticas históricas e gerador de jogos.</p>"
))
display(selecao, concursos, qtd_jogos, criterio, botao, saida)

