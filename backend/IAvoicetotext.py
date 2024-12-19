from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import soundfile as sf
import librosa

def transcribe_audio(audio_path):
    # Codigo para carregar o modelo
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

if __name__ == "__main__":
    audio_file = "C:/Users/Rafius/Documents/Freelas/IAGladston/common_voice_pt_40918540.mp3"  # Caminho do aúdio
    
    try:
        result = transcribe_audio(audio_file)
        print("Transcrição:")
        print(result)
    except Exception as e:
        print(f"Erro durante a transcrição: {str(e)}")