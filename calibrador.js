import socket
import threading
import re

# Script que se inyecta en las respuestas HTTP
INJECTION_SCRIPT = '''
<script>
(function() {
    window.AimbotConfig = {
        enabled: true,
        autoAim: false,
        anguloMaxArriba: 60,
        anguloMaxAbajo: -45,
        sensibilidad: 3.0
    };
    
    console.log("[✓] Aimbot inyectado en Free Fire");
    
    // Interceptar llamadas de mirada
    const originalSetRotation = window.setRotation || function() {};
    window.setRotation = function(x, y) {
        x = Math.max(window.AimbotConfig.anguloMaxAbajo, 
                     Math.min(x, window.AimbotConfig.anguloMaxArriba));
        return originalSetRotation(x, y);
    };
})();
</script>
'''

def modificar_respuesta_http(datos):
    """Inyecta script en respuestas HTML"""
    datos_str = datos.decode('utf-8', errors='ignore')
    
    # Si es HTML, inyectar script antes del </head>
    if '<head>' in datos_str or '</head>' in datos_str:
        datos_str = datos_str.replace('</head>', f'{INJECTION_SCRIPT}</head>')
        return datos_str.encode()
    
    return datos

def proxy_bidireccional(cliente_socket, servidor_host, puerto):
    try:
        # Conectar al servidor real
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.connect((servidor_host, puerto))
        
        # Recibir y modificar datos del cliente
        datos_cliente = cliente_socket.recv(4096)
        servidor_socket.sendall(datos_cliente)
        
        # Recibir y modificar respuesta del servidor
        datos_servidor = servidor_socket.recv(4096)
        datos_servidor = modificar_respuesta_http(datos_servidor)
        cliente_socket.sendall(datos_servidor)
        
        # Transferencia bidireccional continua
        while True:
            datos = cliente_socket.recv(4096)
            if not datos:
                break
            servidor_socket.sendall(datos)
            
            datos = servidor_socket.recv(4096)
            if not datos:
                break
            datos = modificar_respuesta_http(datos)
            cliente_socket.sendall(datos)
    
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        cliente_socket.close()
        servidor_socket.close()

def iniciar_proxy_avanzado():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('127.0.0.1', 8888))
    servidor.listen(10)
    
    print("[*] Proxy avanzado escuchando en 127.0.0.1:8888")
    
    try:
        while True:
            cliente, addr = servidor.accept()
            print(f"[→] Conexión desde {addr}")
            
            hilo = threading.Thread(
                target=proxy_bidireccional,
                args=(cliente, 'freefire.com', 80),
                daemon=True
            )
            hilo.start()
    except KeyboardInterrupt:
        print("\n[*] Proxy detenido")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_proxy_avanzado()