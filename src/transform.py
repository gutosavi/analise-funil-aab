from extract import extract_data
import pandas as pd

def transform_data(df):

    df = df.dropna().reset_index(drop=True)
    new_columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    df.columns = new_columns

    # Convertendo o timestamp para o tipo datetime
    df['eventtimestamp'] = pd.to_datetime(df['eventtimestamp'], unit='s')
    print('Coluna "eventtimestamp" convertida para datetime.')

    #df['event_date'] = df['eventtimestamp'].dt.date
    df['event_date'] = df['eventtimestamp'].dt.floor('D')
    #df['event_date'] = df['eventtimestamp'].dt.hour

    # Filtragem usando data de corte conforme análise prévia
    data_de_corte = pd.to_datetime('2019-08-01')

    total_eventos_originais = df.shape[0]
    total_usuarios_originais = df['deviceidhash'].nunique()

    df = df[df['event_date'] >= data_de_corte]

    eventos_perdidos = total_eventos_originais - df.shape[0]
    usuarios_perdidos = total_usuarios_originais - df['deviceidhash'].nunique()

    # Mapeamento dos grupos
    df['group_name'] = df['expid'].map({
        246: 'A1_Controle',
        247: 'A2_Controle',
        248: 'B_Teste'
    })

    # Usuários que estão em mais de um grupo
    users_in_multiple_groups = (
        df.groupby('deviceidhash')['expid']
        .nunique()
    )

    # Identificação de usuários contaminados
    contaminated_users = users_in_multiple_groups[users_in_multiple_groups > 1].index

    usuarios_perdidos_contaminacao = len(contaminated_users)

    print("Detalhes da Transformação")
    print(f"Período anterior a {data_de_corte} removido.")
    print(f"Usuários em múltiplos grupos removidos: {usuarios_perdidos_contaminacao}")
    print(f"Eventos removidos (Corte + Contaminação): {total_eventos_originais - df.shape[0]}")
    print(f"Total de eventos remanescentes: {df.shape[0]}")
    print(f"Total de usuários remanescentes: {df['deviceidhash'].nunique()}")
    print()
    print('Dados transformados com sucesso!')
    return df

