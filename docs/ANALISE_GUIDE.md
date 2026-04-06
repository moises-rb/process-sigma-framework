# ProcessSigma — Guia de Análise
## Etapas do Projeto e Objetivo de Cada Gráfico

---

## Como ler este documento

Cada seção explica **o que estamos fazendo**, **por que estamos fazendo** e **o que o gráfico está dizendo**. O objetivo não é decorar os conceitos — é entender o raciocínio para conseguir explicar para um cliente ou gestor sem precisar de consulta.

---

## Etapa 1 — Bronze: Ingestão Bruta

### O que fazemos
Carregamos o CSV exatamente como chegou, sem nenhuma transformação. Registramos a origem (`csv_upload` ou `form`) e o momento da ingestão.

### Por que fazemos assim
Se algo der errado nas etapas seguintes, o dado original está intacto para reprocessamento. Em projetos reais, a Bronze é a única camada que nunca é deletada — ela é o histórico permanente.

### O que observar
- Quantidade de registros carregados
- Colunas presentes vs colunas esperadas
- Presença de nulos nos campos críticos

---

## Etapa 2 — Silver: Limpeza e Enriquecimento

### O que fazemos
Calculamos dois campos que não existem no CSV original:

**`delay_days`** = days_real − days_scheduled

**`is_late`** = True se delay_days > 0

Removemos duplicatas por `order_id` e nulos nos campos críticos.

### Por que fazemos assim
`delay_days` é o DNA do processo. Tudo que vem depois — OTD, DPMO, Sigma, P-Chart, Cpk — é calculado a partir dele. Se esse campo estiver errado, toda a análise estará errada.

### O que observar
- Quantos registros foram removidos como duplicatas
- Média e desvio padrão do `delay_days`
- Percentual de `is_late = True`

---

## Etapa 3 — Gold: Indicadores Prontos

### O que fazemos
Agregamos os dados Silver por período e região para calcular OTD%, DPMO e Nível Sigma.

### Por que fazemos assim
O negócio não consome dados brutos — consome respostas. A camada Gold transforma 65 mil linhas em 37 números mensais que o gestor consegue interpretar em 30 segundos.

---

## Gráfico 1 — Distribuição do Desvio de Lead Time

### O que mostra
Um histograma da variável `delay_days` — a diferença em dias entre o prazo prometido e o prazo realizado.

### Como ler
- **Barras à esquerda da linha vermelha** (valores negativos): entregas adiantadas — o processo entregou antes do prometido
- **Linha vermelha (x=0)**: ponto de equilíbrio — entrega exatamente no prazo
- **Barras à direita da linha vermelha** (valores positivos): entregas atrasadas
- **Linha laranja pontilhada**: média do processo — se estiver à direita do zero, o processo é sistematicamente atrasado

### O que procurar
- **Distribuição centrada no zero** → processo balanceado, cumpre o prazo na média
- **Distribuição deslocada para a direita** → problema sistêmico, o processo promete mais do que entrega
- **Distribuição muito larga** → alta variabilidade, processo imprevisível
- **Cauda longa à direita** → casos extremos de atraso que merecem investigação separada

### Pergunta que este gráfico responde
*"O processo é sistematicamente atrasado ou os atrasos são aleatórios?"*

---

## Gráfico 2 — OTD (%) por Região

### O que mostra
Um gráfico de barras horizontais com o percentual de entregas no prazo por região geográfica, ordenado do pior para o melhor desempenho. A escala de cor vai do vermelho (pior) ao verde (melhor). A linha tracejada representa a meta de 95%.

### Como ler
- **Barras verdes acima da linha de meta**: regiões dentro do padrão esperado
- **Barras amarelas/laranjas**: regiões em atenção — monitorar
- **Barras vermelhas abaixo da meta**: regiões críticas — investigar causas
- **Linha branca pontilhada**: média global — referência do processo como um todo

### O que procurar
- **Todas as barras abaixo da meta** → o problema não é regional, é sistêmico
- **Apenas algumas regiões abaixo** → existe causa regional específica a investigar
- **Spread pequeno entre regiões** → processo uniforme em todo território
- **Spread grande** → operações regionais muito diferentes entre si

### Pergunta que este gráfico responde
*"Existe uma região com desempenho muito diferente das demais, ou todas sofrem do mesmo problema?"*

> **Insight crítico do projeto:** quando todas as regiões aparecem com OTD similar (entre 52% e 61%), isso é evidência estatística de causa raiz sistêmica — confirmado pelos testes de hipótese (p > 0.05 em Qui-Quadrado, ANOVA e Teste T).

---

## Gráfico 3 — Evolução Mensal do OTD

### O que mostra
Uma linha do tempo com o OTD% mês a mês. A linha tracejada representa a meta de 95%.

### Como ler
- **Linha azul próxima à meta verde** → processo sob controle e dentro das especificações
- **Linha azul estável mas longe da meta** → processo previsível mas incapaz
- **Linha azul oscilante** → processo instável, com causas especiais agindo periodicamente
- **Tendência de queda** → deterioração — agir antes de piorar
- **Tendência de alta** → melhoria em andamento — identificar o que está funcionando

### O que procurar
- Picos ou quedas abruptas em meses específicos (causas especiais)
- Tendência geral ao longo do tempo
- Sazonalidade (padrões que se repetem em determinados meses)

### Pergunta que este gráfico responde
*"O processo está melhorando, piorando ou estável ao longo do tempo?"*

---

## Gráfico 4 — P-Chart (Carta de Controle para Proporções)

### O que mostra
A Carta P monitora a proporção de defeitos (atrasos) ao longo do tempo, com três linhas horizontais:
- **UCL** (Upper Control Limit): limite superior de controle — 3 desvios padrão acima da média
- **CL** (Center Line): média do processo
- **LCL** (Lower Control Limit): limite inferior de controle — 3 desvios padrão abaixo da média

Pontos marcados em **vermelho** indicam que o processo saiu dos limites estatísticos de controle.

### Como ler
- **Todos os pontos dentro dos limites** → processo estatisticamente estável (sem causas especiais)
- **Pontos acima do UCL** → mês com defeitos anormalmente altos — evento especial ocorreu
- **Pontos abaixo do LCL** → mês com defeitos anormalmente baixos — algo muito bom aconteceu (aprender e replicar)
- **CL alto (ex: 57%)** → o processo é estável no problema, não fora de controle

### A distinção mais importante do CEP
Um processo pode ser **estável E ruim** ao mesmo tempo. Isso é o cenário mais preocupante em Six Sigma — significa que o problema é crônico, não acidental. Não adianta apagar incêndios mês a mês. É preciso redesenhar o processo.

> **Analogia:** um funcionário que chega 30 minutos atrasado todos os dias é "estável" — você consegue prever o comportamento. Mas é um problema sistêmico que exige uma mudança de processo, não uma conversa pontual.

### Pergunta que este gráfico responde
*"O processo é estatisticamente estável, ou existem causas especiais agindo em determinados períodos?"*

---

## Seção Final — Resumo Executivo (Business Case)

### O que mostra
Uma consolidação de todos os indicadores em um formato de decisão: estado atual vs estado alvo, com recomendação clara.

### Como usar com um cliente ou gestor
1. Mostre o **OTD atual vs meta** — impacto direto no cliente
2. Mostre o **DPMO** — linguagem universal de qualidade
3. Mostre o **Sigma Level** — posicionamento na escala Six Sigma
4. Apresente a **recomendação** baseada nos dados

### Tabela de referência Six Sigma

| Nível Sigma | DPMO | OTD equivalente | O que significa |
|------------|------|-----------------|-----------------|
| 6σ | 3.4 | 99.9997% | Classe Mundial — aeronáutica, cirurgia |
| 5σ | 233 | 99.98% | Excelente — indústria de ponta |
| 4σ | 6.210 | 99.4% | Bom — meta mínima recomendada |
| 3σ | 66.807 | 93.3% | Atenção — melhoria necessária |
| 2σ | 308.538 | 69.1% | Ruim — problema sério |
| 1.5σ | 500.000+ | < 50% | Crítico — redesenho urgente |

### Pergunta que esta seção responde
*"O que precisamos fazer, com qual urgência e qual é o gap para chegar onde queremos?"*

---

## Replicando em outro segmento

Para usar este framework em um contexto diferente de logística, o único ajuste necessário é redefinir o que é um **"defeito"** no seu processo:

| Segmento | Equivalente de `is_late` | Equivalente de `delay_days` |
|----------|-------------------------|----------------------------|
| Healthcare | Readmissão em 30 dias | Dias além do tempo de internação previsto |
| IT Service Desk | SLA breach | Tempo de resolução − SLA contratado |
| HR | Turnover em 90 dias | Dias além do prazo de hiring |
| Construção | Não conformidade | Dias de atraso na entrega da obra |

O código não muda. Só o significado do dado muda.
