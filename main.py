import face_recognition
import os
import sys
import cv2
import numpy as np
import mysql.connector
from PIL import Image
import requests
from io import BytesIO
from unidecode import unidecode
import json

path_marcacoes = 'encodings.json'

# Função para calcular a confiança do reconhecimento facial
def confianca_rosto(distancia_rosto, limiar_correspondencia_rosto=0.6):
    intervalo = (1.0 - limiar_correspondencia_rosto)
    valor_linear = (1.0 - distancia_rosto) / (intervalo * 2.0)

    if distancia_rosto > limiar_correspondencia_rosto:
        return str(round(valor_linear * 100, 2)) + '%'
    else:
        valor = (valor_linear + ((1.0 - valor_linear) * ((valor_linear - 0.5) * 2) ** 0.2)) * 100  
        return str(round(valor, 2)) + '%'

# Função para encontrar a câmera correta, num range de 0-50
# Adicionada por que o ubuntu muda o index da câmera com certa frequência
def encontrar_camera():
    for index in range(0, 50):
        captura_video = cv2.VideoCapture(index)
        if captura_video.isOpened():
            print(f'Câmera encontrada com index {index}.\n----------')
            print("Para fechar, pressione 'q'.\nPara buscar novos rostos do banco de dados, segure 'e' pressionado.")
            return captura_video
        captura_video.release()
    sys.exit('Câmera não encontrada.')

# Classe para todo o restante do código
class ReconhecimentoFacial:
    localizacoes_rosto = []
    marcacoes_rosto = []
    nomes_rosto = []
    marcacoes_rostos_conhecidos = []  # Lista de marcações de rostos conhecidos
    nomes_rostos_conhecidos = []  # Lista de nomes de rostos conhecidos
    processar_frame_atual = True

    def __init__(self):
        self.carregar_rostos()

    # Carregar os rostos conhecidos do banco de dados, com os nomes e contatos
    def carregar_rostos(self):
        marcacoes = self.carregar_marcacoes_do_json()
        ids_no_json = set(marcacoes.keys())
        ids_no_banco = set()

        try:
            # Preencher com o login do mysql/mariadb
            db = mysql.connector.connect(
                host='host',
                port=3306,
                user='user',
                password='password',
                database='database'
            )
            cursor = db.cursor()
            cursor.execute('SELECT * FROM tabela') # Preencher com o nome da tabela
            colunas = cursor.fetchall()
            
            """
            O banco de dados que usei contém as seguintes colunas que são usadas nesse script:
            
            pessoa[0]: coluna com o ID
            pessoa[1]: coluna com o nome
            pessoa[5]: coluna com o path interno da imagem, usado depois ao passar a url base + esse path
            """

            for pessoa in colunas:
                print(f'Processando rosto do visitante {pessoa[0]} ({pessoa[1]}).')
                pessoa_id = str(pessoa[0])
                ids_no_banco.add(pessoa_id)
                
                if pessoa_id in marcacoes:
                    self.nomes_rostos_conhecidos.append(unidecode(pessoa[1].title()))
                    self.marcacoes_rostos_conhecidos.append(marcacoes[pessoa_id])
                else:
                    self.nomes_rostos_conhecidos.append(unidecode(pessoa[1].title()))
                    self.carregar_e_processar_imagem(pessoa, marcacoes)
            
            # Remover marcações faciais que não estão no banco de dados
            ids_para_remover = ids_no_json - ids_no_banco
            for id_remover in ids_para_remover:
                del marcacoes[id_remover]

            self.salvar_marcacoes_no_json(marcacoes)
        except mysql.connector.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')
            sys.exit()
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # Puxa as imagens da web
    def carregar_e_processar_imagem(self, pessoa, marcacoes):
        pessoa_id = str(pessoa[0])
        self.foto_url = f'https://exemplo.com/mundosenai/{pessoa[5]}'
        try:
            self.foto_get = requests.get(self.foto_url)
            if self.foto_get.status_code == 200:  # Verifica se o download foi bem-sucedido
                img = Image.open(BytesIO(self.foto_get.content))
                self.foto_np = np.array(img)  # Converte a imagem para numpy array
                self.foto_np_convertida = cv2.cvtColor(self.foto_np, cv2.COLOR_BGR2RGB)
                self.marcacoes_foto_pessoa = face_recognition.face_encodings(self.foto_np_convertida)
                if self.marcacoes_foto_pessoa:
                    encoding = self.marcacoes_foto_pessoa[0].tolist()
                    self.marcacoes_rostos_conhecidos.append(encoding)
                    marcacoes[pessoa_id] = encoding
                else:
                    print(f'Nenhum rosto encontrado na imagem de {pessoa[1]}.')
            else:
                print(f'Erro ao baixar a imagem de {pessoa[1]}. Código de status: {self.foto_get.status_code}')
        except Exception as e:
            print(f"An unexpected error occurred during image download: {e}")

    def carregar_marcacoes_do_json(self):
        if os.path.exists(path_marcacoes):
            with open(path_marcacoes, 'r') as f:
                return json.load(f)
        return {}

    def salvar_marcacoes_no_json(self, marcacoes):
        with open(path_marcacoes, 'w') as f:
            json.dump(marcacoes, f)

    # Método para executar o reconhecimento facial
    def executar_reconhecimento(self):
        captura_video = encontrar_camera()
        captura_video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        captura_video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not captura_video.isOpened():
            sys.exit('Fonte de vídeo não encontrada')

        while True:
            ret, frame = captura_video.read()

            # Só processar cada outro frame do video para economizar processamento
            if self.processar_frame_atual:
                frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Reduzir o tamanho do frame para 1/4
                frame_pequeno_rgb = frame_pequeno[:, :, ::-1]  # Converter a imagem de BGR para RGB

                # Encontrar todos os rostos no frame atual
                self.localizacoes_rosto = face_recognition.face_locations(frame_pequeno_rgb)
                self.marcacoes_rosto = face_recognition.face_encodings(frame_pequeno_rgb, self.localizacoes_rosto)

                # Para cada rosto, comparar e identificar
                self.nomes_rosto = []
                for marcacao_rosto in self.marcacoes_rosto:
                    correspondencias = face_recognition.compare_faces(self.marcacoes_rostos_conhecidos, marcacao_rosto)
                    nome = 'Sem cadastro!'
                    confianca = ''

                    distancias_rosto = face_recognition.face_distance(self.marcacoes_rostos_conhecidos, marcacao_rosto)
                    indice_melhor_correspondencia = np.argmin(distancias_rosto)  # Indice da foto mais parecida na lista

                    if correspondencias[indice_melhor_correspondencia]:
                        nome = self.nomes_rostos_conhecidos[indice_melhor_correspondencia]
                        confianca = confianca_rosto(distancias_rosto[indice_melhor_correspondencia])

                    self.nomes_rosto.append(f'{nome} {confianca}')

            # Exibir um quadrado em torno do visitante identificado com o seu nome
            self.processar_frame_atual = not self.processar_frame_atual
            for (topo, direita, baixo, esquerda), nome in zip(self.localizacoes_rosto, self.nomes_rosto):
                topo *= 4
                direita *= 4
                baixo *= 4
                esquerda *= 4

                cv2.rectangle(frame, (esquerda, topo), (direita, baixo + 20), (255, 0, 0), 1)
                cv2.rectangle(frame, (esquerda, baixo + 20), (direita, baixo - 15), (255, 0, 0), -1)
                cv2.putText(frame, nome, (esquerda + 5, baixo + 5), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            os.environ['QT_STYLE_OVERRIDE'] = 'Windows'  # Ajustar o estilo da janela para não dar erro em sistemas GTK
            cv2.imshow('Reconhecimento Facial', frame)  # Mostrar o frame na tela

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' para fechar
                break
            if cv2.waitKey(1) & 0xFF == ord('r'):  # 'r' para recarregar
                self.carregar_rostos()
                print('Rostos recarregados com sucesso.')

        captura_video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    rf = ReconhecimentoFacial()
    rf.executar_reconhecimento()