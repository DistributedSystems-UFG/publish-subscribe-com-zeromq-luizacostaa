import rpyc
from constRPYC import *
from rpyc.utils.server import ThreadedServer
from datetime import datetime
import zmq

class DBList(rpyc.Service):
    value = []
    publisher = None  # será injetado externamente

    # --- Logs de conexão ---
    def on_connect(self, conn):
        print(f"[SERVER] Cliente conectado às {datetime.now().strftime('%H:%M:%S')}")

    def on_disconnect(self, conn):
        print(f"[SERVER] Cliente desconectado às {datetime.now().strftime('%H:%M:%S')}")

    def exposed_ping(self):
        return True

    # --- Métodos expostos com logs ---
    def exposed_append(self, data):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - append({data})")
        self.value = self.value + [data]
        self.publish("APPEND", f"Elemento {data} adicionado ao vetor.")
        return self.value

    def exposed_insert(self, pos, value):
        MAX_SIZE = 20
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - insert()")

        if pos < 0:
            return "❌ A posição não pode ser negativa."

        if pos >= MAX_SIZE:
            return f"❌ A posição máxima permitida é {MAX_SIZE - 1}."

        while len(self.value) < pos:
            self.value.append(0)

        if len(self.value) < MAX_SIZE:
            self.value.insert(pos, value)

            if len(self.value) > MAX_SIZE:
                self.value = self.value[:MAX_SIZE]
                return "⚠️ Lista atingiu o tamanho máximo! Último elemento removido automaticamente."

            self.publish("INSERT", f"Elemento {value} inserido na posição {pos}.")
            return self.value
        else:
            return "❌ A lista já está no tamanho máximo e não pode receber novos elementos."

    def exposed_show(self):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - show()")
        self.publish("SHOW", f"O vetor foi consultado: {self.value}")
        return self.value

    def exposed_remove(self, pos):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - remove()")

        if pos < 0:
            return "❌ A posição não pode ser negativa."

        if pos >= len(self.value):
            return f"❌ Não existe elemento na posição {pos}."

        removido = self.value.pop(pos)
        self.publish("REMOVE", f"Elemento {removido} removido da posição {pos}.")
        return f"Elemento {removido} removido da posição {pos}."

    def exposed_search(self, value):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - search({value})")
        indices = [i for i, v in enumerate(self.value) if v == value]
        if not indices:
            return f"❌ Valor {value} não encontrado na lista."
        return f"Valor {value} encontrado nas posições: {indices}"

    def exposed_sort(self):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - sort()")
        if not self.value:
            return "❌ A lista está vazia. Nada para ordenar."
        self.value.sort()
        self.publish("SORT", "O vetor foi ordenado.")
        return self.value

    def exposed_clear(self):
        print(f"[SERVER] {datetime.now().strftime('%H:%M:%S')} - clear()")
        self.value = []
        self.publish("CLEAR", "O vetor foi esvaziado.")
        return self.value

    # método de publicação
    def publish(self, topic, msg):
        if DBList.publisher:
            DBList.publisher.send_string(f"{topic} {msg}")


# -------------- BLOCO PRINCIPAL -------------------

if __name__ == "__main__":
    print(f"[SERVER] Servidor iniciado às {datetime.now().strftime('%H:%M:%S')} na porta {PORT}")

    # Criar publisher FORA da classe
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:6000")

    # Injetar publisher na classe
    DBList.publisher = publisher

    # Iniciar RPC
    server = ThreadedServer(DBList, port=PORT)
    print("[SERVER] RPC inicializado. Aguardando conexões...")
    server.start()
