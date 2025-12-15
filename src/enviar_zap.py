import pywhatkit
import pandas as pd
import keyboard
import time

try:
    tabela = pd.read_excel('../data/relatorio_final.xlsx')
except:
    print("Erro! Não achei o arquivo 'relatorio_final.xlsx'. Verifique o nome na pasta.")
    exit()

melhor_vendedor = tabela.iloc[0]['Vendedor']
total_vendas = tabela.iloc[0]['Valor']

numero_destino = "+5521968233122"
mensagem = f"Bot Python (Vitor) informa: O campeão de hoje foi {melhor_vendedor} com R${total_vendas} em vendas!"

print(f"Enviando mensagem para {numero_destino}...")
print("O Navegador vai abrir sozinho. NÃO MEXA NO MOUSE e AGUARDE!")

pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20)

print("Comando de envio finalizado!")