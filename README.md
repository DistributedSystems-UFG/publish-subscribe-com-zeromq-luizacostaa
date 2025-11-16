# Tarefa 10 de publish subscribe

## Como usr
-Tenha python3 atualizado

1 - Iniciar servidor
```bash
    python server.py
```

2 - Iniciar cliente
```bash
    python client.py
```

3 - Iniciar subscriber
```bash
    python subscriber.py
```
Ao iniciar, o subscriber pergunta qual tópico você deseja assinar. É possível assinar:
SHOW, INSERT, APPEND, REMOVE, SORT, CLEAR

Também é possível assinar todos os tópicos deixando o campo vazio e apertando ENTER



## Observações sobre o desenvolvimento

Acabei aproveitando a atividade 8 que usava RPC. Na atividade 8 era possível adicionar, atualizar, limpar, ordenar e fazer várias outras coisas com um vetor. O publish subscribe entra com a ideia de que cada uma das funções: "SHOW", "INSERT", "APPEND", "REMOVE", "SORT" e "CLEAR" serão um tópico. 
Adaptei os códigos e agora toda vez que o vetor sofrer alguma alteração ou ser apenas visualizado, o publisher vai ser notificado.

### ATenção: o publisher foi colocado dentro do server.py
- Quando o servidor é iniciado, ele cria um socket do tipo PUB (publisher) e o associa à classe DBList
```bash
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:6000")
    DBList.publisher = publisher
```
-Todas as operações que modificam ou consultam a lista (append, insert, remove, show, sort, clear) chamam o método publish da própria classe
```bash
    def publish(self, topic, msg):
    if DBList.publisher:
        DBList.publisher.send_string(f"{topic} {msg}")
```    

### Estrutura do Projeto

- server.py – Servidor RPC que gerencia a lista e publica eventos

- client.py – Cliente RPC que permite manipular a lista

- subscriber.py – Cliente para receber notificações em tempo real

- constRPYC.py – Constantes de configuração (SERVER, PORT)