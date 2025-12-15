import streamlit as st
import pandas as pd
import plotly.express as px
import pywhatkit
import time
import keyboard

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Automação de Vendas", layout="wide")

st.title("🚀 Sistema de Gestão de Vendas & Automação")
st.write("Faça upload da sua planilha, analise os dados e envie relatórios via WhatsApp.")

# --- BARRA LATERAL (CONFIGURAÇÕES DE ENVIO) ---
st.sidebar.header("🤖 Configuração do Robô")

# 1. Campo para digitar o número (Pedido do Cliente)
numero_destino = st.sidebar.text_input("Número para envio (com DDD: ",value="+5521999999999")

# 2. Seletor de Mensagens (Pedido do Cliente)
tipo_mensagem = st.sidebar.selectbox(
    "Escolha o Modelo de Mensagem:",
    [
        "Padrão (Campeão de Vendas)",
        "Motivacional (Meta Batida)",
        "Cobrança (Relatório Geral)"
    ]
)

# --- PASSO 1: UPLOAD DO ARQUIVO ---
arquivo_upload = st.file_uploader("Arraste sua planilha de vendas aqui (.xlsx)", type="xlsx")

if arquivo_upload is not None:
    # Ler o arquivo que o usuário enviou
    df = pd.read_excel(arquivo_upload)

    # --- PASSO 2: DASHBOARD (GRÁFICOS) ---
    st.divider() #linha divisória
    st.subheader("📊 Análise de Performance")

    # Lógica de Agrupamento
    relatorio = df.groupby('Vendedor')['Valor'].sum().reset_index()
    relatorio = relatorio.sort_values(by='Valor', ascending=False)

    # Identificar o campeão
    campeao = relatorio.iloc[0]['Vendedor']
    total_campeao = relatorio.iloc[0]['Valor']

    # Mostrar métricas lado a lado (Colunas)
    col1, col2 = st.columns(2)
    col1.metric("Melhor Vendedor", campeao)
    col1.metric("Total Vendido (Top 1)", f"R$ {total_campeao:,.2f}")

    # Gráfico de Barras Bonitão com Plotly
    grafico = px.bar(relatorio, x='Vendedor', y='Valor', title='Vendas por Vendedor', color='Vendedor')
    st.plotly_chart(grafico, use_container_width=True)

    # --- PASSO 3: AUTOMAÇÃO (BOTÃO MÁGICO) ---
    st.divider()
    st.subheader("📲 Enviar Relatório")

    # Lógica para definir o texto da mensagem com base na escolha do usuário
    mensagem_final = ""
    if tipo_mensagem == "Padrão (Campeão de Vendas)":
        mensagem_final = f"Olá! O destaque de hoje foi {campeao} com R$ {total_campeao} em vendas."
    elif tipo_mensagem == "Motivacional (Meta Batida)":
        mensagem_final = f"Parabéns equipe! Hoje batemos a meta. O destaque foi {campeao}."
    elif tipo_mensagem == "Cobrança (Relatório Geral)":
        mensagem_final = f"Relatório do dia fechado. Total geral de vendas: R$ {relatorio['Valor'].sum()}."

    st.info(f"Mensagem que será enviada: {mensagem_final}")

    # O Botão que faz a mágica
    if st.button("Enviar via WhatsApp"):
        if numero_destino:
            st.warning("Abrindo o Whatsapp Web... Por favor, não mexa no mouse.")

            # Automação do PyWhatKit
            try:
                pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem_final, wait_time=20)
                time.sleep(2)
                keyboard.press_and_release('enter')
                st.success("Enviado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao enviar via WhatsApp: {e}")

        else:
            st.error("Por favor, digite um número de telefone na barra lateral.")
