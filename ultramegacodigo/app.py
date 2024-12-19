import streamlit as st
from IAvoicetotext import transcribe_audio
import tempfile
import os

st.title("Transcrição Audio to Text")

uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=['mp3', 'wav'])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    if st.button('Transcrever Aúdio'):
        try:
            with st.spinner('Transcrevendo...'):
                result = transcribe_audio(tmp_file_path)
                
                st.success("Transcrição completa")
                st.write("Texto:")
                st.write(result)
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")
        finally:
            os.unlink(tmp_file_path)