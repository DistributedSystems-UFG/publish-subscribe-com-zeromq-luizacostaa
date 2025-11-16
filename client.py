import rpyc
from constRPYC import * 
from datetime import datetime
import time 

class Client:
  def __init__(self):
    print(f"Cliente iniciado às {datetime.now().strftime('%H:%M:%S')} na porta {PORT}")
    try:
      print("tentando conectar")
      self.conn = rpyc.connect(SERVER, PORT)
      print("conectou")
    except Exception:
      print("❌ Não foi possível conectar ao servidor.")
      exit()

  def safe_call(self, func, *args):
      try:
          return func(*args)
      except Exception:
          print("\n❌ Servidor foi encerrado. O cliente também será fechado.")
          try:
              self.conn.close()
          except:
              pass
          exit()
    
  
  def menu(self):
    while True:
      # --- Testa conexão antes de mostrar o menu ---
      try:
          self.safe_call(self.conn.root.exposed_ping)
      except:
          print("\n❌ Conexão com o servidor perdida.")
          print("O cliente será encerrado.")
          try:
              self.conn.close()
          except:
              pass
          break
      print("\n=== MENU DE OPERAÇÕES ===")
      print("1 - Mostrar lista")
      print("2 - Inserir número no final")
      print("3 - Inserir número em posição específica")
      print("4 - Limpar lista")
      print("5 - Ordenar lista")
      print("6 - Remover número em uma posição específica")
      print("7 - Buscar elemento")
      print("8 - Sair")

      opcao = input("Escolha uma opção: ")


      # --- Teste de conexão antes de executar qualquer operação ---
      if not self.check_connection():
          # print("Tentando reconectar...")

          try:
              self.conn = rpyc.connect(SERVER, PORT)
          except:
              print("❌ Não foi possível reconectar. Encerrando o cliente.")
              break

      if opcao == "1":
        lista = self.safe_call(self.conn.root.exposed_show)
        print("Lista atual:", lista)

      elif opcao == "2":
        valor = input("Digite um número: ")
        try:
          valor = int(valor)
        except ValueError:
          print("Por favor, insira um número válido.")
          continue

        nova_lista = self.safe_call(self.conn.root.exposed_append, valor)
        print("Número inserido. Lista atual:", nova_lista)

      #insert
      elif opcao == "3":
          print("O índice máximo é 19")
          valor = input("Digite o número: ")
          pos = input("Digite a posição onde deseja inserir: ")        

          try:
              valor = int(valor)
              pos = int(pos)
          except ValueError:
              print("Por favor, insira valores válidos.")
              continue

          # chamada segura ao servidor
          resposta = self.safe_call(self.conn.root.exposed_insert, pos, valor)

          # imprimir a lista após a alteração
          lista_atual = self.safe_call(self.conn.root.exposed_show)
          print("Lista atualizada:", lista_atual)


      elif opcao == "4":
        self.safe_call(self.conn.root.exposed_clear)
        print("Lista limpa.")

      elif opcao == "5":
        print("\nVetor atual:")
        lista_atual = self.safe_call(self.conn.root.exposed_show)
        print(lista_atual)

        if not lista_atual:  #  lista vazia
            print("❌ O vetor está vazio. Nada para ordenar. Voltando ao menu...\n")
            continue


      elif opcao == "6":
        print("O índice máximo é 19")
        lista_atual = self.safe_call(self.conn.root.exposed_show)
        print("Lista atual:", lista_atual)
        pos = input("Digite a posição que deseja remover: ")

        try:
            pos = int(pos)
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

        resposta = self.safe_call(self.conn.root.exposed_remove, pos)
        print(resposta)

        lista_atual = self.safe_call(self.conn.root.exposed_show)
        print("Lista atualizada:", lista_atual)

      elif opcao == "7":
        print("\nLista atual:")
        lista_atual = self.safe_call(self.conn.root.exposed_show)
        print(lista_atual)

        # Se a lista estiver vazia, avisar e voltar ao menu
        if len(lista_atual) == 0:
            print("❌ A lista está vazia. Não é possível realizar a busca.")
            continue

        valor = input("Digite o valor que deseja buscar: ")

        try:
            valor = int(valor)
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

        resposta = self.safe_call(self.conn.root.exposed_search, valor)
        print(resposta)

        resposta = self.safe_call(self.conn.root.exposed_sort)
        print("\n Vetor ordenado:")
        print(resposta)

      elif opcao == "8":
        print("Saindo", end="", flush=True)
        for _ in range(3):
          time.sleep(0.5)
          print(".", end="", flush=True)
        print()
        self.conn.close()
        break

      else:
        print("Opção inválida. Tente novamente.")

  #testa conexao antes de fazer algo
  def check_connection(self):
      try:
          self.conn.ping()   # RPyC testa a conexão automaticamente
          return True
      except Exception:
          print("\n[ERRO] Conexão com o servidor perdida!")
          return False

if __name__ == "__main__":
  try:
    client = Client()
    client.menu()
  except KeyboardInterrupt:
    print("\nCliente encerrado com Ctrl+C.")
    try:
      client.conn.close()
    except:
      pass 

