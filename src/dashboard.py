import streamlit as st
import pandas as pd
import plotly.express as px
import pywhatkit
import time
import keyboard


# --- FUNÇÃO TRADUTORA (A MÁGICA ACONTECE AQUI) ---
def carregar_dados(arquivo):
    # Verifica a extensão do arquivo para usar o leitor correto
    if arquivo.name.endswith('.csv'):
        try:
            # Tenta ler como CSV padrão (UTF-8)
            df = pd.read_csv(arquivo)
        except:
            # Se falhar, tenta ler como padrão do Excel/Facebook (UTF-16)
            arquivo.seek(0)
            df = pd.read_csv(arquivo, sep='\t', encoding='utf-16')
    else:
        # Assume que é Excel (.xlsx)
        # Requer: pip install openpyxl
        df = pd.read_excel(arquivo)

    return df

def normalizar_tabela(df):
    # O Tradutor: Renomeia as colunas do Facebook para o nosso padrão
    # Mapa: 'Nome no Facebook': 'Nome no Nosso Sistema'
    mapa_colunas = {
        'full_name': 'Cliente',
        'phone_number': 'Telefone',
        'campaign_name': 'Imóvel de Interesse',
        'created_time': 'Data'
    }

    # Renomeia se encontrar as colunas
    df = df.rename(columns=mapa_colunas)

    # 3. Tratamento de Dados Extras
    # Se não tiver coluna "Status" (o Facebook não tem), criamos como "Novo"
    if 'Status' not in df.columns:
        df['Status'] = 'Novo Lead'

    # Se não tiver "Valor", colocamos "Sob Consulta" ou 0
    if 'Valor Potencial' not in df.columns:
        df['Valor Potencial'] = 0.0

    # Limpeza básica de data (pegar só o dia YYYY-MM-DD)
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data']).dt.date

    return df


# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestor Imobiliário PRO", layout="wide")
st.title("🏠 Gestão de Leads - Integração Facebook Ads")

# --- BARRA LATERAL ---
st.sidebar.header("Configuração")
numero_destino = st.sidebar.text_input("Seu WhatsApp para Teste:", value="+5521999999999")

# --- UPLOAD ---
st.info("Suporta arquivos Excel (.xlsx) ou Exportação do Facebook (.csv)")
arquivo_upload = st.file_uploader("Arraste o arquivo aqui", type=["xlsx", "csv"])

if arquivo_upload is not None:
    try:
        # 1. Carregar e Normalizar
        df_bruto = carregar_dados(arquivo_upload)
        df = normalizar_tabela(df_bruto)

        # Mostra os dados
        with st.expander("Ver Tabela de Dados"):
            st.dataframe(df)

        # --- MÉTRICAS ---
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Leads", len(df))
        # Verifica se a coluna existe antes de calcular a moda
        campanha_top = df['Imóvel de Interesse'].mode()[0] if 'Imóvel de Interesse' in df.columns else "N/A"
        col2.metric("Campanha Principal", campanha_top)

        # Conta novos leads hoje
        hoje = pd.to_datetime('today').date()
        novos_hoje = len(df[df['Data'] == hoje]) if 'Data' in df.columns else 0
        col3.metric("Novos Hoje", novos_hoje)

        # --- GRÁFICOS ---
        # Gráfico 1: Leads por Campanha (Imóvel)
        if 'Imóvel de Interesse' in df.columns:
            contagem = df['Imóvel de Interesse'].value_counts().reset_index()
            contagem.columns = ['Imóvel', 'Quantidade']
            fig = px.bar(contagem, x='Imóvel', y='Quantidade', color='Imóvel')
            st.plotly_chart(fig, use_container_width=True)

        # --- AUTOMAÇÃO (FIFO: FIRST IN, FIRST OUT) ---
        st.divider()
        st.subheader("📲 Fila de Atendimento")

        # Filtra apenas Novos
        novos_leads = df[df['Status'] == 'Novo Lead']

        if not novos_leads.empty:
            # --- ORDENAÇÃO FIFO (O PULO DO GATO) ---
            # Ordena por Data Crescente (Antigo -> Novo)
            if 'Data' in novos_leads.columns:
                novos_leads = novos_leads.sort_values(by='Data', ascending=True)

            # Pega o primeiro da fila (agora garantido ser o mais antigo)
            lead_atual = novos_leads.iloc[0]

            nome = lead_atual.get('Cliente', 'Lead sem Nome')
            imovel = lead_atual.get('Imóvel de Interesse', 'Imóvel')

            st.info(f"**Próximo da Fila (Mais Antigo):** {nome}")
            st.write(f"Interesse: {imovel} | Data: {lead_atual.get('Data', '-')}")

            msg_padrao = f"Olá {nome}, vi seu interesse no {imovel}. Podemos agendar uma visita?"
            mensagem = st.text_area("Mensagem:", value=msg_padrao)

            if st.button("Enviar WhatsApp"):
                st.warning("Abrindo WhatsApp...")
                try:
                    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20)
                    time.sleep(2)
                    keyboard.press_and_release('enter')
                    st.success("Enviado!")
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.success("🎉 Fila zerada! Todos os leads foram atendidos.")

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        st.warning("Dica: Se enviou um Excel, verifique se instalou o openpyxl: pip install openpyxl")
