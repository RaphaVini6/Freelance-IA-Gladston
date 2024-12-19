document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const audioFile = document.getElementById("audio-file").files[0];
    const resultDiv = document.getElementById("result");

    if (!audioFile) {
        alert("Por favor, selecione um arquivo de áudio.");
        return;
    }

    resultDiv.innerHTML = `<div class="c-loader"></div><span>Processando...</span>`;
    resultDiv.classList.add("loading");

    const formData = new FormData();
    formData.append("audio", audioFile);

    try {
        const response = await fetch("http://127.0.0.1:5000/transcribe", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Erro ao processar o áudio.");

        const data = await response.json();
        resultDiv.classList.remove("loading");
        resultDiv.innerHTML = `<strong>Transcrição:</strong> ${data.transcription}`;
    } catch (error) {
        resultDiv.classList.remove("loading");
        resultDiv.innerHTML = `<span style="color: red;">Erro: ${error.message}</span>`;
    }
});
