import pandas as pd
import random
from datetime import datetime, timedelta

print("Gerando simulação de arquivo exportado do Facebook Ads...")

# --- ESTRUTURA PADRÃO DO FACEBOOK (META ADS) ---
# O Facebook geralmente entrega CSV com essas colunas em inglês
colunas_fb = ['id', 'created_time', 'full_name', 'phone_number', 'email', 'campaign_name', 'platform']

nomes = ['Ana Clara', 'Bruno Diniz', 'Carlos Eduardo', 'Daniela Lima', 'Eduardo Costa']
campanhas = ['[Compra] Ap Centro', '[Venda] Casa Condomínio', '[Aluguel] Studio Barra', '[Lançamento] Torre Norte']

dados = []

for i in range(50):
    dias_atras = random.randint(0, 7)
    data = datetime.now() - timedelta(days=dias_atras)

    #Formato de data do Facebook (ISO 8601)
    data_str = data.strftime("%Y-%m-%dT%H:%M:%S+0000")

    item = {
        'id': f"lead_{1000+i}",
        'created_time': data_str,
        'full_name': random.choice(nomes),
        'phone_number': f"+55219{random.randint(10000000, 99999999)}",
        'email': "email@teste.com",
        'campaign_name': random.choice(campanhas),
        'platform': 'ig' #instagram
    }
    dados.append(item)

df = pd.DataFrame(dados)
# O Facebook exporta em CSV, não em Excel
arquivo_saida = '../data/leads_facebook_export.csv'
df.to_csv(arquivo_saida, index=False)

print(f"Sucesso! Arquivo 'cru' do Facebook gerado em: {arquivo_saida}")
print(df.head())
