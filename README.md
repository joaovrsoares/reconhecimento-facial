# Reconhecimento facial

Projeto de reconhecimento facial para uso no Mundo SENAI 2024. Utilizando as bibliotecas face_recognition e OpenCV do Python 3.10, reconhece a face do visitante e mostra na tela.<br>
Baixa as marcações faciais do banco de dados MySQL e compara com a pessoa que está sendo mostrada para ele através da câmera.<br>
No futuro enviará uma mensagem via aplicativo para esse contato que é pedido na captura. Por enquanto é placeholder.<br>

## Utilização

#### Linux
Testado em distribuições com base Debian/Ubuntu.
É necessário o Python 3.10.x (de preferência com venv) e um banco de dados compatível com MySQL.
```bash
git clone https://github.com/joaovrsoares/reconhecimento-facial.git && cd reconhecimento-facial/
pip install -r requirements.txt
```
#### Windows
Ainda não testado, mas pode depender de ferramentas de compilação C++ para a biblioteca dlib.