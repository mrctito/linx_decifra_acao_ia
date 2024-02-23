import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


TABELA_COMANDOS_EMPORIO = [
  {
    "command": "cadastrar novo produto",
    "description": "Adicionar um novo produto ao inventário",
    "code": "CMD1000001"
  },
  {
    "command": "atualizar estoque",
    "description": "Atualizar a quantidade de um produto no estoque",
    "code": "CMD1000002"
  },
  {
    "command": "remover produto",
    "description": "Remover um produto do inventário",
    "code": "CMD1000003"
  },
  {
    "command": "verificar níveis de estoque",
    "description": "Consultar a quantidade atual de produtos no estoque",
    "code": "CMD1000004"
  },
  {
    "command": "relatório de estoque",
    "description": "Gerar um relatório detalhado do estoque",
    "code": "CMD1000005"
  },
  {
    "command": "cadastrar fornecedor",
    "description": "Adicionar um novo fornecedor ao sistema",
    "code": "CMD1000006"
  },
  {
    "command": "excluir fornecedor",
    "description": "Remover um fornecedor do sistema",
    "code": "CMD1000007"
  },
  {
    "command": "registrar entrada de produtos",
    "description": "Registrar a entrada de novos produtos no estoque",
    "code": "CMD1000008"
  },
  {
    "command": "registrar saída de produtos",
    "description": "Registrar a saída de produtos do estoque",
    "code": "CMD1000009"
  },
  {
    "command": "analisar tendências de estoque",
    "description": "Analisar padrões e tendências no movimento de estoque",
    "code": "CMD1000010"
  },
  {
    "command": "criar pedido de compra",
    "description": "Criar um novo pedido de compra",
    "code": "CMD1000011"
  }
]

TABELA_COMANDOS_EMPORIO_STR = json.dumps(TABELA_COMANDOS_EMPORIO)

PROMPT_BASE = '''
Você é um assistente inteligente que analisa comandos relacionados a operações comerciais.
Sua tarefa é decompor cada comando em suas partes constituintes, identificando a ação, produto, 
fornecedor, cliente, serviço, data, quantidade, preço, unidade de medida, motivo, endereço,  
número da nota fiscal, número do pedido, e quaisquer outros elementos relevantes que façam sentido 
para o pedido.

Para a ação identificada, você deve seguir essas instruções adicionais: 
Com base na tabela de mapeamento de comandos e códigos de um sistema de gestão de estoque, informada 
abaixo entre os marcadores [INICIO] e [FIM], analise a ação identificada acima para determinar calcular 
o código de comando correspondente. Use a descrição e o comando associado para fazer a melhor 
correspondência possível.

Finalmente elabore sua resposta, em formato JSON, conforme estes exemplos de como você deve processar e 
responder em formato JSON:

Exemplo 1:
Comando: criar pedido de 1.000 litros de gasolina aditivada.
Resposta em JSON:
{{
  "Ação": "Criar Pedido",
  "Comando": "CMD1000011"
  "Produto": "Gasolina Aditivada",
  "Quantidade": "1.000 litros"
}}

Exemplo 2:
Comando: cadastrar óleo de soja lata 150 ml preço 25 reais.
Resposta em JSON:
{{
  "Ação": "cadastrar produto",
  "Comando": "CMD1000001",
  "Produto": "óleo de soja",
  "Unidade": "lata 150 ml",
  "Preço": "25 reais"
}}

Exemplo 3:
Comando: gerar relatório de estoque de ontem.
Resposta em JSON:
{{
  "Ação": "gerar relatório de estoque",
  "Comando": "CMD1000005",
  "Data": "22/02/2023" (supondo que hoje seja 23/02/2023)
}}

Tabela de de-para de comandos:
[INICIO]
{tabela}
[FIM]

Agora, analise o seguinte comando e decomponha-o nos elementos relevantes, respondendo no formato JSON:
Comando: {texto}
Resposta em JSON:
'''

def prepara_prompt():
    prompt = PromptTemplate(
        template=PROMPT_BASE,
        input_variables=["texto", "tabela"],
    )
    return prompt
