import time
import cv2
import os


# Inicializar a câmera
camera = cv2.VideoCapture(0)
print("Pressione 'C' para capturar a imagem, e 'Q' para sair")

while True:
    # Capturar um frame da câmera (captura um por vez)
    verificador, frame = camera.read()
    if not verificador:
        print("Erro ao capturar a imagem")
        break

    # Exibir o frame capturado
    os.environ['QT_STYLE_OVERRIDE'] = 'Windows'  # Ajustar o estilo da janela para não dar erro em sistemas GTK
    cv2.imshow('Captura do rosto', frame)

    # Aguardar a tecla 'C' ser pressionada para capturar a imagem
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c') or key == ord('C'):
        time.sleep(1)  # Aguardar 1 segundo para a pessoa ver a foto

        camera.release()  # Parar a captura de imagem
        cv2.destroyAllWindows()  # Fechar a janela da câmera

        nome = input("Digite o primeiro nome: ").upper()

        try:
            if not os.path.exists('fotos'):
                os.makedirs('fotos')
            caminho_imagem = os.path.join('fotos', f'{nome}.jpg')  # Caminho para salvar a imagem
            cv2.imwrite(caminho_imagem, frame)  # Salvar a imagem
            print(f"Imagem salva em {caminho_imagem}")

            break
        except Exception as e:
            print(f"Erro ao salvar a imagem no banco de dados: {e}")
            break

    # Sair do loop se a tecla 'Q' for pressionada
    elif key == ord('q') or key == ord('Q'):
        camera.release()
        cv2.destroyAllWindows()
        break