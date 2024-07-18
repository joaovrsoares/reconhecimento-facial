const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const bcrypt = require('bcrypt');

const app = express();
const port = 3000;

// Configuração do Body Parser
app.use(bodyParser.urlencoded({ extended: true }));

// Conexão com o Banco de Dados
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root', // seu usuário MySQL
    password: '', // sua senha MySQL
    database: 'stackinverse'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Conectado ao banco de dados MySQL!');
});

// Rota para o Formulário de Cadastro
app.post('/register', async (req, res) => {
    const { nomeCompleto, usuario, email, senha } = req.body;

    // Criptografar a Senha
    const hashedPassword = await bcrypt.hash(password, 10);

    const user = { nomeCompleto: nomeCompleto, usuario, email, senha: hashedPassword };

    const sql = 'INSERT INTO users SET ?';
    db.query(sql, user, (err, result) => {
        if (err) throw err;
        console.log('Usuário registrado:', result);
        res.send('Usuário registrado com sucesso!');
    });
});

// Iniciar o Servidor
app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});

