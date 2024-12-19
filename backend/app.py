import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import torch

def transcribe_audio(audio_path):
    # Carrega o modelo
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    
    # EXTREMAMENTE IMPORTANTE: O áudio deve ser carregado com uma taxa de 16kHz
    audio_input, sampling_rate = librosa.load(audio_path, sr=16000)
    
    input_features = processor(
        audio_input,
        sampling_rate=sampling_rate,
        return_tensors="pt"
    ).input_features

    # Pega os IDs da linguagem e da Task
    predicted_ids = model.generate(
        input_features,
        language="portuguese",
        task="transcribe"
    )
    
    transcription = processor.batch_decode(
        predicted_ids,
        skip_special_tokens=True
    )[0]
    
    return transcription

# Configuração da interface com Streamlit
st.title("Transcrição de Áudio com Whisper")
st.write("Faça upload de um arquivo de áudio para transcrever.")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo de áudio (MP3, WAV, etc.)", type=["mp3", "wav"])

if uploaded_file:
    # Salva o arquivo temporariamente
    temp_audio_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
    with open(temp_audio_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.write("Transcrevendo o áudio... Isso pode levar alguns segundos.")
    
    try:
        transcription = transcribe_audio(temp_audio_path)
        st.success("Transcrição concluída!")
        st.text_area("Transcrição", transcription, height=200)
    except Exception as e:
        st.error(f"Erro durante a transcrição: {str(e)}")
