import os
import time
import json
import cv2
import mysql.connector
import face_recognition


def salvar_rosto(nome, foto):
    try:  # Conectar ao banco de dados, se existir o schema 'rec_facial'
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Joooao16@',
            database='rec_facial'
        )
        db.close()

    except mysql.connector.Error as e:

        # Se não existir o schema 'rec_facial', criar o schema e a tabela 'faces'
        if e.errno == 1049:
            print("Criando banco de dados 'rec_facial'...")
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Joooao16@'
            )
            cursor = db.cursor()
            cursor.execute('CREATE DATABASE rec_facial')
            cursor.execute('USE rec_facial')
            cursor.execute('''
            CREATE TABLE faces (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                nome        VARCHAR(100),
                contato     VARCHAR(100),
                face        TEXT NOT NULL
            );
            ''')
            cursor.close()
            db.close()
            print("Banco de dados 'rec_facial' criado")

        # Se ocorrer outro erro, exibir a mensagem e encerrar o programa
        else:
            print(f'Erro ao conectar ao banco de dados: {e}')
            exit()

    try:  # Conectar ao banco de dados
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Joooao16@',
            database='rec_facial'
        )
        cursor = db.cursor()

        # Inserir imagem no MySQL
        sql = '''
        INSERT INTO faces 
            (nome, contato, face) 
        VALUES 
            (%s, %s, %s);
            '''
        cursor.execute(sql, (nome, contato, foto))
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as e:
        print(f'Erro ao salvar imagem no banco de dados: {e}')


# Inicializar a câmera
camera = cv2.VideoCapture(0)
print("Pressione 'C' para capturar a imagem, e 'Q' para sair")

while True:
    # Capturar um frame da câmera (captura um por vez)
    verificador, frame = camera.read()
    if not verificador:
        print('Erro ao capturar a imagem')
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

        nome = input("Digite o primeiro nome: ").title()
        contato = input("Digite o contato: ")

        try:
            # Pegar as marcações da face da pessoa, identificando ela
            marcacao_rosto = json.dumps(face_recognition.face_encodings(frame)[0].tolist())

            # Salvar a imagem no banco de dados
            salvar_rosto(nome, marcacao_rosto)

            print("Imagem enviada para o banco de dados com sucesso")
            break

        except Exception as e:
            print(f"Erro ao salvar a imagem no banco de dados: {e}")
            break

    # Sair do loop se a tecla 'Q' for pressionada
    elif key == ord('q') or key == ord('Q'):
        camera.release()
        cv2.destroyAllWindows()
        break
