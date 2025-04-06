"""
Hackathon Relâmpago - Caçadores de Fraudes
Autor: Renan Almeida Ferreira , Lucas Mesquita da Silva 
Data: 06/04/2025
Objetivo: Detectar fraudes em lista de compras públicas utilizando Python.
"""

import pandas as pd
from tabulate import tabulate

# Leitura do CSV
#compras = pd.read_csv('avaliacao\public_servant_purchases_new.csv')
compras = pd.read_csv('1-Modulo-p-s-ia\public_servant_purchases_new.csv')
# Funções
# Detecta combinações repetidas de funcionário e item (compras duplicadas)
def detectar_compras_duplicadas(compras):
    contagem = compras.groupby(['nome_do_funcionario', 'item_comprado']).size().reset_index(name='quantidade')
    duplicados = contagem[contagem['quantidade'] > 1]
    df_duplicadas = compras.merge(duplicados[['nome_do_funcionario', 'item_comprado']], 
                                  on=['nome_do_funcionario', 'item_comprado'],
                                  how='inner')
    return df_duplicadas

# Agrupa dados por funcionário e mostra itens comprados e total gasto
def organizar_por_servidor(compras):
    agrupado = compras.groupby('nome_do_funcionario')
    dados = []

    for nome, grupo in agrupado:
        itens_validos = grupo['item_comprado'].dropna()
        itens_validos = itens_validos[itens_validos.apply(lambda x: isinstance(x, str) and not x.strip().isnumeric())]

        if itens_validos.empty:
            continue

        itens = ", ".join(itens_validos)
        total = grupo['valor_em_real'].sum()

        dados.append({
            'Nome do Funcionário': nome,
            'Itens Comprados': itens,
            'Total Gasto (R$)': total
        })

    df_organizado = pd.DataFrame(dados)
    df_organizado = df_organizado[df_organizado['Itens Comprados'].str.strip().astype(bool)]
    df_organizado = df_organizado.sort_values(by='Total Gasto (R$)', ascending=False)
    df_organizado['Total Gasto (R$)'] = df_organizado['Total Gasto (R$)'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    return df_organizado

# Lista compras com valor maior que R$ 1000
def listarvalores(compras):
    valores = compras[compras['valor_em_real'] > 1000]
    return valores[['nome_do_funcionario', 'item_comprado', 'valor_em_real']]

# Filtra compras feitas fora do horário comercial (antes de 08h ou após 18h)
def compras_fora_de_horario(compras):
    compras['data_da_compra'] = pd.to_datetime(compras['data_da_compra'], errors='coerce')
    compras = compras.dropna(subset=['data_da_compra'])
    compras['hora'] = compras['data_da_compra'].dt.hour
    fora_do_horario = compras[(compras['hora'] < 8) | (compras['hora'] >= 18)]
    return fora_do_horario[['nome_do_funcionario', 'item_comprado', 'valor_em_real', 'data_da_compra']]

def verificar_valores_suspeitos(compras):
    # Converte a data corretamente e extrai hora completa
    compras['data_da_compra'] = pd.to_datetime(compras['data_da_compra'], errors='coerce')
    compras = compras.dropna(subset=['data_da_compra'])   
    compras['hora_completa'] = compras['data_da_compra'].dt.strftime('%H:%M:%S')
    compras['hora'] = compras['data_da_compra'].dt.hour

    suspeitos = []

    # Verifica desvios de valor por funcionário + item
    grupos = compras.groupby(['nome_do_funcionario', 'item_comprado'])

    for (nome, item), grupo in grupos:
        media_valor = grupo['valor_em_real'].mean()

        for _, linha in grupo.iterrows():
            valor = linha['valor_em_real']
            if valor <= 0:
                motivo = 'valor zero ou negativo'
            elif valor < 0.8 * media_valor or valor > 1.6 * media_valor:
                motivo = 'valor fora da média (20-60%)'
            else:
                motivo = None

            if motivo:
                registro = linha.to_dict()
                registro['motivo_suspeita'] = motivo
                suspeitos.append(registro)

    df_suspeitos = pd.DataFrame(suspeitos)

    # Compras fora do horário comercial
    fora_do_horario = compras[(compras['hora'] < 8) | (compras['hora'] >= 18)].copy()
    fora_do_horario['motivo_suspeita'] = 'compra fora do horário'

    # Junta tudo e remove duplicados
    df_final = pd.concat([df_suspeitos, fora_do_horario]).drop_duplicates()

    return df_final[['nome_do_funcionario', 'item_comprado', 'valor_em_real', 'data_da_compra', 'hora_completa', 'motivo_suspeita']]

# Função principal
def gerar_relatorio(compras):
    print("="*70)
    print("📄 RELATÓRIO DE COMPRAS E DETECÇÃO DE PADRÕES")
    print("="*70)

    print("\n🔍 1. Compras Duplicadas (funcionário comprando o mesmo item):")
    df_duplicados = detectar_compras_duplicadas(compras).head(10)
    print(tabulate(df_duplicados, headers='keys', tablefmt='grid', showindex=False))

    print("\n💰 2. Compras com valor acima de R$ 1000,00:")
    df_acima_1000 = listarvalores(compras).head(5)
    print(tabulate(df_acima_1000, headers='keys', tablefmt='grid', showindex=False))

    print("\n👤 3. Compras organizadas por servidor (top 4 por gasto):")
    df_servidores = organizar_por_servidor(compras).head(4)
    print(tabulate(df_servidores, headers='keys', tablefmt='grid', showindex=False))

    print("\n⏰ 4. Compras fora do horário comercial (antes das 08h ou após as 18h):")
    df_fora_horario = compras_fora_de_horario(compras).head(5)
    print(tabulate(df_fora_horario, headers='keys', tablefmt='grid', showindex=False))

    print("\n 5. Relatorio de Fraudes:(top 10)")
    df_valores_suspeitos = verificar_valores_suspeitos(compras).head(10)
    print(tabulate(df_valores_suspeitos, headers='keys', tablefmt='grid', showindex=False))

    print("\n✅ Fim do relatório.")
    print("="*70)

# Execução principal
if __name__ == "__main__":
    print("Iniciando análise...\n")
    gerar_relatorio(compras)

    ###### detalhes de funcionamento e especificações no README.MD #########################