import json
import os

import uvicorn
from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from llm import cria_chain
from prompt import TABELA_COMANDOS_HUMANUS, prepara_prompt

app = FastAPI()

# rotina para testar o serviço
def test():
  prompt = prepara_prompt()
  llm = cria_chain(prompt)
  while True:
      print("\n")
      texto_usuario = input("Digite o comando desejado: ")
      if texto_usuario == ".":
        break

      usuario_input = UsuarioInput(codigo_sistema="EMPORIO", texto_usuario=texto_usuario)
      result = decompoe_acao(usuario_input)
      print(result)


class UsuarioInput(BaseModel):
  codigo_sistema: str
  texto_usuario: str

# serviço que recebe um comando do usuário e retorna o código de menu correspondente
@app.post("/decompoe_acao/")
def decompoe_acao(usuario_input: UsuarioInput) -> str:
  prompt = prepara_prompt()
  llm = cria_chain(prompt)

  # decide qual tabela de comandos usar
  tabela = TABELA_COMANDOS_HUMANUS
  
  # chama a API que traduz o comando do usuario em um código de menu
  result = llm.invoke({"texto": usuario_input, "tabela": tabela})
  return result["text"]
  
if __name__ == "__main__":

  modo_teste = os.getenv("MODO_TESTE", "N")
  if modo_teste == "S":
    # se modo teste ativo, então roda test()
    test()
  else:
    # senão coloca o serviço no ar
    print()
    print("Iniciando servidor...")
    print()
    print("Acesse http://localhost:8107/docs para Swagger")
    print()
    print("Para testar, use o comando abaixo")
    print('curl -X "POST" "http://localhost:8107/obtem_comando_menu/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"texto_usuario\": \"novo produto\"}"')
    print()
    uvicorn.run("main:app", host="0.0.0.0", port=8107)

# para testar
# curl -X "POST" "http://localhost:8106/obtem_comando_menu/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"texto_usuario\": \"novo produto\"}"



"""
1- No programa principal, criar um campo de texto para o usuário digitar o comando desejado.
2- Chamar a API que traduz o comando do usuario em um código de menu.
3- Escrever um "case" ou "ifs aninhados" para cada código de menu, que chama a função do sistema correspondente.
"""
