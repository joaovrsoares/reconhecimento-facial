const camera = document.getElementById('camera');
navigator.mediaDevices.getUserMedia({video: true})
    .then(streamDaCamera => {
        camera.srcObject = streamDaCamera;
    })
    .catch(erro => {
        console.error("Erro ao abrir a câmera: ", erro);
    });