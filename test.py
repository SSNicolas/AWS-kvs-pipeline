import cv2

# URL do fluxo RTSP
rtsp_url = "rtsp://admin:smartsigma7@192.168.10.160:554/Streaming/channels/101"

# Abre a conexão com a câmera RTSP
cap = cv2.VideoCapture(rtsp_url)

# Verifica se a conexão foi bem-sucedida
if not cap.isOpened():
    print("Erro ao conectar à câmera RTSP")
    exit()

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    # Se a captura foi bem-sucedida
    if ret:
        cv2.imshow('Video', frame)

        # Pressione 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Falha ao capturar frame")
        break

# Libera a captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()
