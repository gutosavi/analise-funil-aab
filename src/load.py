from pathlib import Path
import pandas as pd

def load_data(df: pd.DataFrame, output_path: str, format: str = 'csv') -> None:
    
    # Validação
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f'Era esperado um DataFrame, mas foi recebido outro objeto {type(df)}')
    
    # Caminho e extensão
    file_path = Path(f'{output_path}.{format.lower()}')

    if file_path.parent:
        file_path.parent.mkdir(parents=True, exist_ok=True)

    # Formato
    try:
        if format.lower() == 'csv':
            df.to_csv(file_path, index=False)
        elif format.lower() == 'parquet':
            df.to_parquet(file_path, index=False)
        else:
            print(f'Format{format} não suportado. Salvando em CSV por padrão.')
            df.to_csv(file_path.with_suffix('.csv'), index=False)

        print(f'Dados carregados com sucesso para {file_path}')
        print(f'Número de registros salvos: {df.shape[0]}')

    except Exception as e:
        print(f'Erro durante a fase de load: {e}')

