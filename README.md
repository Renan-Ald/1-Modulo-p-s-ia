# avaliacao
Repositório da Avaliação da disciplina de Algoritmos e Programação
 Funções do Script
1. detectar_compras_duplicadas(compras)
python
Copiar
Editar
def detectar_compras_duplicadas(compras):
    ...
Objetivo: Identificar casos em que o mesmo funcionário comprou o mesmo item mais de uma vez.

Passos:

Agrupa pelo nome do funcionário e item comprado.

Conta quantas vezes esse par aparece.

Filtra apenas os pares repetidos.

Retorna um DataFrame com as compras duplicadas.

2. organizar_por_servidor(compras)
python
Copiar
Editar
def organizar_por_servidor(compras):
    ...
Objetivo: Agrupar as compras por servidor e calcular o total gasto por cada um.

Passos:

Agrupa as compras pelo nome do funcionário.

Filtra e concatena os itens válidos (não numéricos e não nulos).

Calcula o total gasto.

Formata os valores em reais.

Retorna um DataFrame organizado, ordenado pelo gasto.

3. listarvalores(compras)
python
Copiar
Editar
def listarvalores(compras):
    ...
Objetivo: Listar todas as compras com valor acima de R$ 1000,00.

Passos:

Filtra as compras cujo campo valor_em_real seja maior que 1000.

Retorna um DataFrame contendo nome, item e valor.

4. compras_fora_de_horario(compras)
python
Copiar
Editar
def compras_fora_de_horario(compras):
    ...
Objetivo: Detectar compras realizadas fora do horário comercial (antes das 8h ou após as 18h).

Passos:

Converte a coluna data_da_compra para datetime.

Remove valores inválidos.

Extrai a hora da compra.

Filtra as compras feitas fora do horário comercial.

Retorna um DataFrame com os detalhes dessas compras.

📊 Função principal: gerar_relatorio(compras)
python
Copiar
Editar
def gerar_relatorio(compras):
    ...
Objetivo: Gerar um relatório visual no terminal com todas as análises aplicadas.

Inclui:

Compras duplicadas.

Compras com valor acima de R$ 1000.

Gastos organizados por servidor.

Compras feitas fora do horário comercial.

Formato: O relatório é impresso com a biblioteca tabulate# 1-Modulo-p-s-ia
