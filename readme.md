# Reconhecimento Facial com OpenCV e MediaPipe
Este projeto demonstra a implementação de um sistema de reconhecimento facial utilizando as bibliotecas OpenCV e MediaPipe em Python.
O sistema capta imagens de uma webcam, detecta rostos presentes e desenha retângulos ao redor deles.<br>
O script `main.py` inicializa a webcam e processa cada frame capturado em tempo real. Utiliza-se a biblioteca MediaPipe
para detectar rostos nos frames e a biblioteca OpenCV para manipulação de imagens e exibição dos resultados.
Para fechar, basta pressionar 'q'.

## Pré-requisitos
Para executar este projeto, é necessário o Python e as bibliotecas OpenCV e MediaPipe:
```bash
sudo apt install python3 python3-pip
pip install -r requirements.txt
```