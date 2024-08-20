from scapy.all import sniff, IP, TCP, UDP, ICMP
import hashlib
import joblib
import pandas as pd

captured_data = []

# Función para determinar el estado de la conexión (conn_state)
def determine_conn_state(packet):
    if TCP in packet:
        flags = packet[TCP].flags
        if flags == 0x02:  # SYN
            return "S0"  # SYN enviado, no respuesta aún
        elif flags == 0x12:  # SYN-ACK
            return "S1"  # SYN enviado, SYN-ACK recibido
        elif flags == 0x10:  # ACK (durante la conexión)
            return "SF"  # Conexión establecida y terminada correctamente
        elif flags == 0x14:  # RST-ACK
            return "RSTR"  # El servidor envió un RST después de recibir SYN
        elif flags == 0x04:  # RST
            return "RSTO"  # El servidor envió un RST después de la conexión establecida
        elif flags == 0x01:  # FIN
            return "SH"  # El cliente envió un FIN y luego cerró la conexión
        elif flags & 0x04 and not flags & 0x02:  # RST sin SYN (RST después de la conexión)
            return "RSTOS0"  # No se recibió respuesta tras el SYN, pero se recibió un RST
        elif flags == 0x18:  # PSH-ACK
            return "S2"  # SYN-ACK fue enviado y recibido, pero no se recibió ACK
        elif flags == 0x04 and flags == 0x12:  # RST-ACK (con SYN-ACK)
            return "RSTRH"  # El servidor envió un RST en respuesta al SYN-ACK
        elif flags == 0x04 and flags == 0x01:  # FIN-RST
            return "REJ"  # Conexión rechazada, el servidor envió RST
    return "OTH"  # Cualquier otro estado

# Función para construir la historia de la conexión (history)
def determine_history(packet, history=""):
    if TCP in packet:
        flags = packet[TCP].flags
        if flags & 0x02:  # SYN
            history += "S" if "S" not in history else "s"
        if flags & 0x10:  # ACK
            history += "A" if "A" not in history else "a"
        if flags & 0x01:  # FIN
            history += "F" if "F" not in history else "f"
        if flags & 0x04:  # RST
            history += "R" if "R" not in history else "r"
    if packet.haslayer(IP) and len(packet[IP].payload) > 0:
        if "D" not in history and packet[IP].src != None:
            history += "D"  # Datos enviados
        else:
            history += "d"  # Datos recibidos
    return history

# Función para determinar si una IP es local
def is_local(ip):
    if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172.16.") or ip.startswith("172.31."):
        return True
    return False

# Callback de paquetes para capturar y procesar
def packet_callback(packet):
    history = ""
    data = {
        'ts': packet.time,
        'uid': hashlib.md5(str(packet.time).encode()).hexdigest(),
        'id.orig_h': packet[IP].src if IP in packet else None,
        'id.orig_p': packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else None),
        'id.resp_h': packet[IP].dst if IP in packet else None,
        'id.resp_p': packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else None),
        'proto': determine_proto(packet),
        'service': determine_service(packet),
        'duration': packet.time - packet.time,  # Placeholder, ya que la duración requiere múltiples paquetes.
        'orig_bytes': len(packet[IP].payload) if IP in packet else 0,
        'resp_bytes': len(packet[IP].payload) if IP in packet else 0,
        'conn_state': determine_conn_state(packet),
        'local_orig': is_local(packet[IP].src) if IP in packet else None,
        'local_resp': is_local(packet[IP].dst) if IP in packet else None,
        'missed_bytes': 0,  # Placeholder.
        'history': determine_history(packet, history),
        'orig_pkts': 1,  # Considerando 1 paquete por captura.
        'orig_ip_bytes': len(packet[IP]) if IP in packet else 0,
        'resp_pkts': 1,  # Considerando 1 paquete por captura.
        'resp_ip_bytes': len(packet[IP]) if IP in packet else 0,
        'tunnel_parents': None,  # Placeholder.
    }
    captured_data.append(data)

    # Imprimir o almacenar los datos capturados

# Guardar el modelo entrenado en un archivo

# Función para determinar el servicio basado en los puertos
def determine_service(packet):
    if packet.haslayer(TCP):
        if packet[TCP].sport == 80 or packet[TCP].dport == 80:
            return "http"
        elif packet[TCP].sport == 443 or packet[TCP].dport == 443:
            return "https"
        elif packet[TCP].sport == 22 or packet[TCP].dport == 22:
            return "ssh"
        # Añade otros servicios según sea necesario
    elif packet.haslayer(UDP):
        if packet[UDP].sport == 53 or packet[UDP].dport == 53:
            return "dns"
        elif packet[UDP].sport == 67 or packet[UDP].dport == 68:
            return "dhcp"
    return "other"

# Función para determinar el protocolo
def determine_proto(packet):
    if TCP in packet:
        return "tcp"
    elif UDP in packet:
        return "udp"
    elif ICMP in packet:
        return "icmp"
    else:
        return "Other"  # O puedes retornar "other" si prefieres tener un valor predeterminado

# Iniciar captura de paquetes
sniff(filter="ip", prn=packet_callback, timeout=60)
df = pd.DataFrame(captured_data)
joblib.dump(df, 'captured_data.pkl')
df.head()