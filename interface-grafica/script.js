document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const fullName = document.getElementById('nome-completo').value;
    const username = document.getElementById('usuario').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('senha').value;

    // Simular um processo de criação de conta
    console.log('Account created successfully!', { nomeCompleto, usuario, email, senha });
    alert('Account created successfully!');
});
