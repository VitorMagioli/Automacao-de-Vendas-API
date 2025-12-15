# 🚀 Sistema de Automação de Vendas e Dashboard

Este projeto é uma solução completa para análise de dados de vendas, geração de relatórios automáticos e envio de notificações via WhatsApp. Desenvolvido para demonstrar a aplicação de Python na otimização de processos comerciais.

## 🛠️ Funcionalidades

- **ETL Automático:** Leitura e tratamento de planilhas Excel (brutas).
- **Análise de Dados:** Cálculo de KPIs (Melhor vendedor, Total de vendas).
- **Dashboard Interativo:** Interface visual web construída com Streamlit e Plotly.
- **Automação de WhatsApp:** Envio de mensagens personalizadas para a equipe ou gestores com um clique.

## 💻 Tecnologias Utilizadas

- **Python 3.12**
- **Pandas:** Manipulação e análise de dados.
- **Streamlit:** Criação da interface web (Dashboard).
- **Plotly:** Gráficos interativos.
- **OpenPyXL:** Leitura e escrita de arquivos Excel.
- **PyWhatKit:** Automação de envio de mensagens via WhatsApp Web.

## 📂 Estrutura do Projeto

```bash
AutomacaoVendas/
├── data/               # Armazena as planilhas de entrada e saída
├── src/
│   ├── gerar_dados.py  # Script para criar massa de dados fictícia
│   ├── analise_vendas.py # Script de processamento ETL
│   ├── enviar_zap.py   # Script de automação de envio simples
│   └── dashboard.py    # Aplicação Web principal
└── README.md