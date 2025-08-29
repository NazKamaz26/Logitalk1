import socket
import threading
import time

SERVER_HOST = '4.tcp.eu.ngrok.io'
SERVER_PORT = 18592

def connect():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_HOST, SERVER_PORT))
            name = input("Enter your name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            sock.send(name.encode())
            print(f"✅ Connected as: {name}")
            return sock
        except Exception as e:
            print(f"⚠️ Connection failed: {e}. Retrying in 2s...")
            time.sleep(2)

def send_messages(sock):
    try:
        while True:
            msg = input()
            if msg.lower() == 'exit':
                sock.send(f"{msg}".encode())
                print("🚫 Disconnected from chat.")
                sock.close()
                break
            sock.send(msg.encode())
    except Exception as e:
        print(f"❌ Receive error: {e}")
        sock.close()

def receive_messages(sock):
    try:
        while True:
            message = sock.recv(1024).decode().strip()
            if not message:
                print("🚫 Server closed connection.")
                break
            print(message)
    except:
        print(f"👋 Bye-bye!")
    finally:
        sock.close()

# Запуск клієнта
client_socket = connect()

# Потік для надсилання повідомлень
threading.Thread(target=send_messages, args=(client_socket,), daemon=True).start()

# Головний цикл прийому
receive_messages(client_socket)
