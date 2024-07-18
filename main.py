import face_recognition
import os
import sys
import cv2
import numpy as np
import mysql.connector
import json
from unidecode import unidecode


# Função para calcular a confiança do reconhecimento facial
def confianca_rosto(distancia_rosto, limiar_correspondencia_rosto=0.6):
    intervalo = (1.0 - limiar_correspondencia_rosto)
    valor_linear = (1.0 - distancia_rosto) / (intervalo * 2.0)

    if distancia_rosto > limiar_correspondencia_rosto:
        return str(round(valor_linear * 100, 2)) + '%'
    else:
        valor = (valor_linear + ((1.0 - valor_linear) * ((valor_linear - 0.5) * 2) ** 0.2)) * 100  
        return str(round(valor, 2)) + '%'


# Classe para reconhecimento facial
class ReconhecimentoFacial:
    localizacoes_rosto = []
    marcacoes_rosto = []
    nomes_rosto = []
    marcacoes_rostos_conhecidos = []  # Lista de marcações de rostos conhecidos
    nomes_rostos_conhecidos = []  # Lista de nomes de rostos conhecidos
    contatos_rostos_conhecidos = []  # Lista de contatos de rostos conhecidos
    processar_frame_atual = True

    def __init__(self):
        self.carregar_rostos()

    # Carregar os rostos conhecidos do banco de dados, junto com os nomes e contatos
    def carregar_rostos(self):
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Joooao16@',
                database='rec_facial'
            )
            cursor = db.cursor()
            
            # Pegar os rostos conhecidos da tabela faces do banco de dados
            cursor.execute('SELECT * FROM faces')
            colunas = cursor.fetchall()
            
            for pessoa in colunas:
                self.nomes_rostos_conhecidos.append(pessoa[1].title())
                self.contatos_rostos_conhecidos.append(pessoa[2])
                self.marcacoes_rostos_conhecidos.append(json.loads(pessoa[3]))
                
        except mysql.connector.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')
            
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()


    # Método para executar o reconhecimento facial
    def executar_reconhecimento(self):
        captura_video = cv2.VideoCapture(0)

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

                self.nomes_rosto = []
                for marcacao_rosto in self.marcacoes_rosto:
                    correspondencias = face_recognition.compare_faces(self.marcacoes_rostos_conhecidos, marcacao_rosto)
                    nome = 'Desconhecido'
                    confianca = ''

                    distancias_rosto = face_recognition.face_distance(self.marcacoes_rostos_conhecidos, marcacao_rosto)
                    indice_melhor_correspondencia = np.argmin(distancias_rosto)  # Indice da foto mais parecida na lista

                    if correspondencias[indice_melhor_correspondencia]:
                        nome = self.nomes_rostos_conhecidos[indice_melhor_correspondencia]
                        confianca = confianca_rosto(distancias_rosto[indice_melhor_correspondencia])

                    self.nomes_rosto.append(f'{nome} {confianca}')

            # Exibir os resultados
            self.processar_frame_atual = not self.processar_frame_atual
            for (topo, direita, baixo, esquerda), nome in zip(self.localizacoes_rosto, self.nomes_rosto):
                topo *= 4
                direita *= 4
                baixo *= 4
                esquerda *= 4

                cv2.rectangle(frame, (esquerda, topo), (direita, baixo + 20), (255, 0, 0), 2)
                cv2.rectangle(frame, (esquerda, baixo + 20), (direita, baixo - 15), (255, 0, 0), -1)
                cv2.putText(frame, nome, (esquerda + 5, baixo + 5), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            os.environ['QT_STYLE_OVERRIDE'] = 'Windows'  # Ajustar o estilo da janela para não dar erro em sistemas GTK
            cv2.imshow('Reconhecimento Facial', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        captura_video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    rf = ReconhecimentoFacial()
    rf.executar_reconhecimento()
