import cv2  # Puxa o opencv
import mediapipe as mp  # Puxa o mediapipe como "mp"

# Inicializar o OpenCV e a webcam
camera = cv2.VideoCapture(0)  # 0 é o ID da webcam

# Inicializar o MediaPipe e os módulos de desenho e reconhecimento facial
desenho = mp.solutions.drawing_utils
reconhecimento_api = mp.solutions.face_detection
reconhecimento_detector = reconhecimento_api.FaceDetection()

while True:
    # Ler as informações da webcam
    verificador, frame = camera.read()
    if not verificador:  # Se não conseguir ler a imagem, para o loop
        break

    # Processar o frame com o MediaPipe para reconhecimento facial
    rostos = reconhecimento_detector.process(frame)
    if rostos.detections:
        for rosto in rostos.detections:
            # Desenhar o retângulo do rosto
            desenho.draw_detection(frame, rosto)

    # Inverter a câmera e exibir o frame na tela
    frame = cv2.flip(frame, 1)
    cv2.imshow('Reconhecimento facial', frame)

    # Esperar 5ms a cada atualização de frame (para não travar)
    # Quando apertar a tecla 'q', para o loop
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

camera.release()  # Desligar a webcam
