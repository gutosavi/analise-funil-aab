import pandas as pd
from pathlib import Path

def extract_data(path):
    
    try:
        df = pd.read_csv(path, sep='\t')
        print('Dados extraídos com sucesso') 
        return df
    except FileNotFoundError:
        print(f'Erro: O arquivo {path} não foi encontrado.')
        raise