# Reconhecimento facial

Projeto de reconhecimento facial para uso no Mundo SENAI 2024. Utilizando as bibliotecas face_recognition e OpenCV do Python 3.10, reconhece a face do visitante e mostra na tela.
Baixa as marcações faciais do banco de dados MySQL e compara com a pessoa que está sendo mostrada para ele através da câmera.

## Utilização

#### Linux
Testado em distribuições com base Debian/Ubuntu.
É necessário o Python 3.10.x (de preferência com venv) e um banco de dados compatível com MySQL.
```bash
git clone https://github.com/joaovrsoares/reconhecimento-facial.git && cd reconhecimento-facial/
pip install -r requirements.txt
```
É necessário ajustar nos scripts o domínio de acesso ao banco de dados.
#### Windows
Ainda não testado, mas pode depender de ferramentas de compilação C++ para a biblioteca dlib.

## A fazer
- [ ] Arquivo separado para armazenar o login de acesso ao banco de dados, e incluir no .gitignore. Mais seguro e menos trabalho editando cada login separado.
- [ ] Variável 'contato' ainda é placeholder, precisa ser utilizada. A ideia é enviar uma mensagem via aplicativo para a pessoa assim que for identificada.
- [ ] Interface web para uso no Mundo SENAI.
