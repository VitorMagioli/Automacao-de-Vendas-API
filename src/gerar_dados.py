import pandas as pd
import os

dados = {
    'Vendedor': ['Ana', 'Carlos', 'Ana', 'Beto', 'Carlos', 'Ana', 'Beto', 'Ana'],
    'Produto': ['Notebook', 'Mouse', 'Monitor', 'Teclado', 'Notebook', 'Mouse', 'Monitor', 'Cabo HDMI'],
    'Valor': [3500, 50, 1200, 150, 3400, 45, 1100, 30],
    'Data': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-03', '2023-01-02', '2023-01-04', '2023-01-03', '2023-01-01']
}

df = pd.DataFrame(dados)

caminho_pasta = '../data' # O '..' significa "volte uma pasta", pois estamos dentro de 'src'

if not os.path.exists(caminho_pasta):
    os.makedirs(caminho_pasta)

df.to_excel(f'{caminho_pasta}/vendas_brutas.xlsx', index=False)

print("Sucesso! O arquivo 'vendas_brutas.xlsx' foi criado na pasta 'data'.")