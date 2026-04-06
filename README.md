# ⚡ ProcessSigma Framework
### Pipeline de Inteligência de Entregas — Exemplo Minimalista

> **Six Sigma + Engenharia de Dados + Process Mining**  
>Um framework leve e sem necessidade de banco de dados para aplicar a metodologia DMAIC em qualquer conjunto de dados operacionais..

---

## O que é isso?

O ProcessSigma é um framework reutilizável que transforma dados brutos de entrega em indicadores Six Sigma acionáveis — de forma automática.

Este repositório contém o **exemplo minimalista**: um notebook autocontido e um dashboard Streamlit que rodam a partir de um único arquivo CSV, sem necessidade de banco de dados ou infraestrutura em nuvem.

O projeto completo (privado) inclui:
- Arquitetura Medalhão no Supabase (Bronze → Silver → Gold)
- Dashboard Streamlit em tempo real com 5 páginas
- Análise estatística em R (CEP, Testes de Hipótese, Capabilidade)
- Mineração de Processos (Process Mining) com PM4Py e GraphViz
- Dashboard executivo em Power BI

---

## Início Rápido

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/processsigma-framework.git
cd processsigma-framework
```

### 2. Criar ambiente com uv (recomendado)
```bash
# Instalar uv (se ainda não estiver instalado)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Criar ambiente com Python 3.11
uv venv --python 3.11
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Instalar dependências (~2 minutos)
uv pip install -r requirements_minimal.txt
```

### Alternativa: usar pip
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements_minimal.txt
```

### 3. Adicionar seus dados
Coloque seu CSV na pasta data/ seguindo o formato do template, ou deixe o notebook gerar dados sintéticos automaticamente.

### 4. Executar o notebook
```bash
jupyter notebook minimal_example.ipynb
```

### 5. Executar o dashboard
```bash
streamlit run minimal_example_app.py
```

---

## Estrutura do Projeto

```
processsigma-framework/
├── minimal_example.ipynb       # Notebook narrativo passo a passo
├── minimal_example_app.py      # Dashboard Streamlit standalone
├── requirements_minimal.txt    # Dependências mínimas (uv recomendado)
├── data/
│   └── template_injecao.csv    # Template de dados
├── exports/                    # Gráficos gerados (criado automaticamente)
└── docs/
    ├── STUDY_GUIDE.md          # Guia metodológico completo
    ├── architecture.md         # Decisões da Arquitetura Medalhão
    └── data_dictionary.md      # Definições de campos
```

---

## O que o Notebook Demonstra

| Etapa | O que faz |
|------|-------------|
| 🥉 Bronze | Ingestão bruta — dados preservados como estão |
| 🥈 Silver | Limpeza, deduplicação, cálculo de atraso |
| 🥇 Gold | OTD%, DPMO, Nível Sigma por período e região |
| 📊 EDA | Distribuição, OTD por região, tendência mensal |
| 📈 CEP | Carta P com detecção automática de pontos fora de controle |
| 🎯 Business Case | Resumo executivo com recomendação |

---

## Requisitos Mínimos de Dados

| Análise | Mínimo | Recomendado |
|----------|---------|-------------|
| EDA | 30 registros | 200+ |
| Carta P | 25 subgrupos | 30+ |
| Cpk | 100 registros | 500+ |
| Nível Sigma | 100 oportunidades | 1,000+ |

---

## Replicável para Qualquer Segmento

O framework requer apenas 5 campos para rodar:

| Campo | Campo | Exemplo |
|-------|------|---------|
| `order_id` | Integer | ID único do evento |
| `order_date` | Date | Data de início do processo |
| `ship_date` | Date | Data de fim do processo |
| `days_scheduled` | Integer | Lead time planejado |
| `days_real` | Integer | Lead time real |

**Segmentos aplicáveis:** Logística, Saúde (Healthcare), Service Desk de TI, RH, Construção, Finanças, Manufatura.

---

## Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-5.22-lightblue?style=flat-square)
![uv](https://img.shields.io/badge/uv-0.11-green?style=flat-square)

---

## Licença

Licenciado sob a **Business Source License 1.1 (BSL 1.1)**.
Grátis para uso não comercial. Uso comercial requer autorização.
Converte-se em MIT após 4 anos.

---

## Projeto Completo & Consultoria

Interessado no pipeline completo ou em aplicar isso ao seu negócio?  
Connect on [LinkedIn](https://www.linkedin.com/in/moisesrsjr/)

---

*ProcessSigma — Onde os Dados Encontram a Excelência de Processos*
