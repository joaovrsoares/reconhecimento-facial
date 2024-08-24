# Reconhecimento facial

Projeto de reconhecimento facial para uso no Mundo SENAI 2024. Utilizando as bibliotecas face_recognition e OpenCV do Python 3.10, reconhece a face do visitante e mostra na tela.
Baixa a foto do banco de dados MySQL, gera marcações faciais e compara com a pessoa que está sendo mostrada para ele através da câmera.

## Utilização

#### Linux
Testado em distribuições com base Ubuntu 22.04.
É necessário o Python 3.10.x (de preferência com venv) e um banco de dados compatível com MySQL.
```bash
git clone https://github.com/joaovrsoares/reconhecimento-facial.git && cd reconhecimento-facial/
pip install -r requirements.txt
```
É necessário ajustar no script o domínio de acesso ao banco de dados e configurar de acordo.
#### Windows
Ainda não testado, mas pode depender de ferramentas de compilação C++ para a biblioteca dlib.