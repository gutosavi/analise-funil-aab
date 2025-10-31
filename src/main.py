from extract import extract_data
from transform import transform_data
from load import load_data

def main():
    path_raw = 'D:/TripleTen/analise_funil_vendas/data/raw/logs_exp_us.csv'
    path_processed = 'D:/TripleTen/analise_funil_vendas/data/processed/logs_exp_us_processado'

    df = extract_data(path_raw)
    df_transformed = transform_data(df.copy())
    #df_transformed = transform_data(df)
    load_data(df_transformed, path_processed)

    print('Pipeline processado com sucesso!')

if __name__ == '__main__':
    main()
