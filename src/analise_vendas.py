import pandas as pd
import os

# --- ETAPA 1: EXTRACT (LER O ARQUIVO) ---
caminho_arquivo = '../data/vendas_brutas.xlsx'

# Verificação de segurança
if not os.path.exists(caminho_arquivo):
    print("Erro! O arquivo não foi encontrado na pasta.")
    exit() # Para o programa se não achar o arquivo

print("Lendo o arquivo 'vendas_brutas.xlsx'")
df = pd.read_excel(caminho_arquivo)

#Mostra as 5 primeiras linhas no terminal
print("\n--- Dados Lidos ---")
print(df.head())

# --- ETAPA 2: TRANSFORM (PROCESSAR OS DADOS) ---
print("\nCalculando Vendas por vendedor...")

# A MÁGICA: O comando .groupby() é a "Tabela Dinâmica" do Python.
relatorio = df.groupby('Vendedor')['Valor'].sum().reset_index()

relatorio = relatorio.sort_values(by='Valor', ascending=False)

print("\n---Resumo das Vendas\n")
print(relatorio)

arquivo_saida= '../data/relatorio_final.xlsx'
relatorio.to_excel(arquivo_saida, index=False)

print(f"\nSucesso! Relatório salvo em: {arquivo_saida}")
