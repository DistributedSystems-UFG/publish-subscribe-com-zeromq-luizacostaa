import zmq
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Cores para tópicos diferentes
TOPIC_COLORS = {
    "SHOW": Fore.CYAN,
    "INSERT": Fore.GREEN,
    "APPEND": Fore.MAGENTA,
    "REMOVE": Fore.RED,
    "SORT": Fore.YELLOW,
    "CLEAR": Fore.BLUE
}

def main():
    context = zmq.Context()
    s = context.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:6000")

    # Mensagem de boas-vindas
    print("Bem-vindo(a) à nossa revista digital do vetor!")
    print("Fique por dentro de tudo o que acontece com o vetor v.")
    print("Se alguém consultá-lo, modificá-lo ou ordená-lo, você vai saber! Escolha quais tópicos te interessam.\n")

    # Perguntar qual tópico(s) assinar
    print("Tópicos disponíveis:", ", ".join(TOPIC_COLORS.keys()))
    selected_topics = input("Digite os tópicos que deseja assinar, separados por vírgula (ou ENTER para todos): ").strip()

    if selected_topics:
        topics = [t.strip().upper() for t in selected_topics.split(",")]
        for t in topics:
            s.setsockopt_string(zmq.SUBSCRIBE, t)
        print(f"Assinando os tópicos: {', '.join(topics)}")
    else:
        s.setsockopt_string(zmq.SUBSCRIBE, "")
        print("Assinando TODOS os tópicos.")

    print("\nSubscriber iniciado. Aguardando mensagens...\n")

    try:
        while True:
            msg = s.recv_string()
            # separar o tópico da mensagem
            parts = msg.split(" ", 1)
            topic = parts[0]
            conteudo = parts[1] if len(parts) > 1 else "(sem conteúdo)"
            hora = datetime.now().strftime("%H:%M:%S")
            color = TOPIC_COLORS.get(topic, Fore.WHITE)
            print(f"{color}[{hora}] [{topic}] {conteudo}{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print("\nEncerrando subscriber...")
    finally:
        s.close()
        context.term()

if __name__ == "__main__":
    main()
