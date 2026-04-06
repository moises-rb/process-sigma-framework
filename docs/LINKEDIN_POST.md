# Post LinkedIn — ProcessSigma Framework

---

Transformei 3 anos de dados de uma cadeia de suprimentos global em um Business Case Black Belt — automaticamente.

E agora publiquei o framework para qualquer pessoa replicar.

**O problema que investiguei:**

Uma operação com mais de 180 mil registros, 23 regiões no mundo inteiro, operando há 3 anos com mais de 57% de atraso nas entregas. Ninguém sabia exatamente por quê.

**O que os dados provaram:**

Três testes estatísticos independentes — Qui-Quadrado, ANOVA e Teste T — chegaram à mesma conclusão: a diferença entre a pior região (61% de atraso) e a melhor (52%) é ruído estatístico. Não existe uma região culpada.

O problema está no processo central de agendamento. Afeta todas as 23 regiões com a mesma intensidade. É estável há 37 meses consecutivos.

Isso é o diagnóstico mais valioso que um Black Belt pode entregar — não "região X está com problema", mas "o design do processo está errado e precisa ser redesenhado".

**Os números do Business Case:**

- DPMO: 573.336 (meta: 6.210)
- Nível Sigma: 1.5σ (meta: 4.0σ)
- Cpk: 0.11 (processo incapaz — meta: ≥ 1.33)
- Gap para a meta: 98.9% de redução no DPMO necessária

**O que foi construído para chegar nisso:**

Pipeline completo com arquitetura Medalhão (Bronze → Silver → Gold) no Supabase, ETL em Python, análise estatística em R com qcc (Carta P, Carta XBar, Análise de Capabilidade), Process Mining com PM4Py, dashboard interativo no Streamlit e painel executivo no Power BI.

**O que estou publicando como open source:**

Um minimal example que qualquer pessoa pode rodar em 5 minutos — sem banco de dados, sem infraestrutura, sem configuração complexa. Um notebook Jupyter + um app Streamlit que lê um CSV e entrega:

→ Distribuição do desvio de lead time
→ OTD% por região com linha de meta
→ Tendência mensal com identificação de causas especiais
→ P-Chart com detecção automática de pontos fora de controle
→ Resumo executivo com Sigma Level e recomendação

**O que aprendi que vale compartilhar:**

R e Python não são concorrentes. Python faz o pipeline. R faz o que o Minitab faz para os Belts — Cartas de Controle, Cpk, testes de hipótese — com output direto, sem implementar do zero.

Um processo estável no lugar errado é tão preocupante quanto um processo fora de controle. Estável em 57% de atraso durante 3 anos não é azar. É design.

Dado limpo conta a história. Mas dado interpretado estatisticamente muda decisões.

**Link do repositório público:**

github.com/seu-usuario/processsigma-framework

O framework funciona para logística, healthcare, TI, RH, construção — qualquer processo que tenha uma data de início, uma data de fim e um prazo prometido.

Se você trabalha com dados e qualidade, vale explorar.

---

*Hashtags sugeridas:*
#sixsigma #blackbelt #engenhariadadados #python #rlanguage #processimprovement #dataanalytics #streamlit #portfólio #qualidade #supplychain #leanseissigma #processmining #datascience
