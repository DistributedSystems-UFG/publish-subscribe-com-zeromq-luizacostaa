import zmq
import sys
from datetime import datetime

# === Cores ANSI ===
RESET = "\033[0m"
BOLD = "\033[1m"

# Cores
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GRAY = "\033[90m"

def main():
    context = zmq.Context()
    s = context.socket(zmq.SUB)
    s.connect("tcp://127.0.0.1:6000")

    # Se nenhum tópico for passado, assina todos
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        print(f"{GRAY}Assinando apenas o tópico:{RESET} {GREEN}{topic}{RESET}")
        s.setsockopt_string(zmq.SUBSCRIBE, topic)
    else:
        print(f"{GRAY}Assinando TODOS os tópicos.{RESET}")
        s.setsockopt_string(zmq.SUBSCRIBE, "")

    print(f"{GRAY}Subscriber iniciado. Aguardando mensagens...{RESET}\n")

    try:
        while True:
            msg = s.recv_string()
            
            # separar o tópico da mensagem
            parts = msg.split(" ", 1)
            topic = parts[0]
            conteudo = parts[1] if len(parts) > 1 else "(sem conteúdo)"

            hora = datetime.now().strftime("%H:%M:%S")

            print(
                f"{YELLOW}[{hora}]{RESET} "
                f"{GREEN}[{topic}]{RESET} "
                f"{CYAN}{conteudo}{RESET}"
            )

    except KeyboardInterrupt:
        print(f"\n{GRAY}Encerrando subscriber...{RESET}")
    finally:
        s.close()
        context.term()

if __name__ == "__main__":
    main()
