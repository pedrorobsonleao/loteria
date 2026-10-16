# 🎯 Loteria Lab 2.0 — Análise Estatística & Gerador de Jogos

Uma ferramenta moderna, interativa e completa para análise estatística, visualização de dados históricos e geração de combinações para as principais loterias da **Caixa Econômica Federal** (**Mega-Sena**, **Lotofácil**, **Quina** e **Lotomania**).

O projeto conta com uma aplicação web estática (*Single Page Application* em HTML/CSS/JS) com interface rica em *glassmorphism*, gráficos interativos e mapa de calor térmico, além do script analítico original em Python.

---

## 🚀 Funcionalidades Principais

### 1. 📊 Dados Oficiais & Resumo ao Vivo
- **Integração direta com a API da Caixa**: Consulta dos resultados oficiais mais recentes e histórico retroativo em lotes assíncronos.
- **Temporizador Regressivo**: Contagem regressiva em tempo real até o próximo sorteio com base no cronograma oficial de cada modalidade.
- **Dezenas Animadas**: Efeito de queda escalonada (*ballDrop*) nas dezenas do último concurso.

### 2. 🌡️ Mapa de Calor Térmico Unificado
- **Escala de Temperatura Dinâmica**: Dezenas coloridas em um gradiente contínuo:
  - ❄️ **Azul / Ciano**: Baixa frequência (números mais "frios").
  - 🟢 **Verde**: Frequência intermediária.
  - 🔥 **Amarelo / Vermelho**: Alta frequência (números mais "quentes").
- **Padronização Visual**: A mesma paleta térmica é aplicada ao **Mapa de Calor**, às **bolas do último sorteio**, ao **histórico completo**, às **tabelas de frequência** e aos **jogos gerados**.

### 3. 📈 Gráficos Interativos & Tabelas
- **Gráfico de Barras de Frequência**: Visualização da incidência de cada dezena com filtros de período (Últimos 20, Últimos 50 ou Todos os concursos).
- **Evolução Temporal (Linha)**: Acompanhamento da trajetória acumulada das 5 dezenas mais sorteadas ao longo dos concursos.
- **Gráfico Radar**: Perfil de distribuição por quadrantes dos jogos gerados em comparação com a média histórica.
- **Tabelas Completas**: Rankings separados para as dezenas mais frequentes (Top 15), menos frequentes e listagem geral com barras proporcionais.
- **Pares Mais Frequentes**: Top 20 combinações de pares que mais saíram juntos nos sorteios.
- **Métricas e Paridade**: Estatísticas de porcentagem de pares/ímpares, pares consecutivos e intervalos de soma das dezenas.

### 4. 🎲 Gerador de Jogos & Ferramentas
- **Geração Inteligente**:
  - *Aleatório Puro*: Sorteio uniforme sem viés.
  - *Ponderado por Frequência*: Probabilidade proporcional à incidência histórica suavizada.
- **Efeito Confetti**: Animação festiva customizada com a identidade visual da loteria selecionada.
- **⭐ Favoritos no Navegador**: Salve combinações geradas diretamente no `localStorage` para consulta posterior.
- **📥 Exportação CSV**: Download imediato da lista de palpites gerados em formato `.csv`.
- **📤 Compartilhamento Rápido**: Links diretos formatados para envio via WhatsApp, Telegram ou cópia para a área de transferência.

### 5. 🔍 Conferidor de Apostas Retrospectivo
- Insira suas dezenas e teste seu desempenho contra até os últimos 50 concursos, com destaque para quadras, quinas, jackpots e faixas de premiação.

### 6. ⚖️ Comparador de Loterias Lado a Lado
- Painel comparativo duplo para analisar duas loterias diferentes simultaneamente com seus respectivos gráficos de frequência.

### 7. 🎨 Personalização de Interface
- **Tema Claro / Escuro**: Alternância rápida com persistência automática da preferência.
- **Efeito Aurora Borealis**: Cabeçalho animado com gradiente que se adapta à paleta de cores oficial de cada jogo.

---

## 📂 Estrutura do Repositório

```text
├── index.html     # Aplicação Web Single Page completa (HTML5, CSS3, JS ES6+)
├── loteria.py     # Script analítico em Python (Pandas, Matplotlib, Requests)
└── README.md      # Documentação do projeto
```

---

## 🛠️ Como Utilizar

### Opção A: Executando a Aplicação Web (`index.html`)

Por realizar requisições assíncronas (`fetch`) para a API oficial de loterias, recomenda-se servir a página através de um servidor HTTP local para evitar restrições de CORS locais:

```bash
# 1. Navegue até o diretório do projeto
cd /home/pleao/Documents/Projects/loteria

# 2. Inicie um servidor local simples com Python:
python3 -m http.server 8080

# 3. Abra o navegador em:
# http://localhost:8080
```

> **Dica**: Você também pode abrir diretamente o arquivo com `xdg-open index.html` no Linux ou clicando duas vezes no arquivo no seu explorador.

#### Passo a Passo na Interface:
1. No menu superior, escolha a **Loteria** desejada (*Mega-Sena*, *Lotofácil*, *Quina* ou *Lotomania*).
2. Defina a quantidade de concursos para o **Histórico** (de 10 a 200).
3. Clique em **🔍 Analisar** para carregar os dados oficiais da Caixa.
4. Explore os cards de **Mapa de Calor**, **Frequência**, **Estatísticas** e **Probabilidades**.
5. Na seção **Gerar Jogos**, configure a quantidade desejada, escolha o método e clique em **🎲 Gerar Jogos**.

---

### Opção B: Executando o Script Python (`loteria.py`)

Para usuários de terminal, notebooks Jupyter ou Google Colab:

```bash
# Instale as dependências necessárias
pip install requests pandas matplotlib ipywidgets numpy

# Execute o script interativo
python3 loteria.py
```

O script gerará arquivos de dados locais:
- `historico_loteria.csv`: Histórico detalhado dos concursos consultados.
- `frequencia_loteria.csv`: Ranking de ocorrências e porcentagens por dezena.
- `jogos_gerados.csv`: Jogos gerados pela amostragem ponderada.

---

## 📐 Loterias Suportadas & Regras

| Modalidade | Universo de Dezenas | Dezenas Sorteadas | Faixas de Premiação Principal |
| :--- | :---: | :---: | :--- |
| **Mega-Sena** | 1 a 60 | 6 | Quadra (4), Quina (5), Sena (6) |
| **Lotofácil** | 1 a 25 | 15 | 11, 12, 13, 14 e 15 pontos |
| **Quina** | 1 a 80 | 5 | Duque (2), Terno (3), Quadra (4), Quina (5) |
| **Lotomania** | 0 a 99 (100) | 20 | 15, 16, 17, 18, 19 e 20 pontos |

---

## 🧮 Base Matemática & Bibliotecas

- **Chart.js 4.4.0**: Renderização de gráficos de barras, linhas acumuladas e radares.
- **Canvas-Confetti 1.9.2**: Feedback visual com confetes dinâmicos.
- **Análise Combinatória**: Cálculo exato de chances teóricas via combinação simples:
  $$C(n, k) = \frac{n!}{k!(n-k)!}$$
- **Amostragem Ponderada**: Algoritmo ponderado sem reposição para geração de apostas.

---

## ⚠️ Aviso Legal & Jogo Responsável

- Esta ferramenta foi desenvolvida com **finalidade estritamente educacional, recreativa e estatística**.
- **Atenção**: De acordo com a teoria das probabilidades, cada sorteio é um evento estocástico independente. *A frequência passada de uma dezena não garante nem altera a probabilidade matemática do seu sorteio futuro*.
- Apostas são proibidas para menores de 18 anos. Jogue com moderação e responsabilidade.
