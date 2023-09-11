import streamlit as st
import googletrans
from googletrans import Translator
from gtts import gTTS
from IPython.display import Audio
from PIL import Image
import base64
import playsound
import os
import datetime
import speech_recognition as sr
print(googletrans.LANGCODES)
# page layout and icon
st.set_page_config(
        page_title="Vina Translator",
        page_icon="voice",
        layout="centered",
    )
# # remove space at the top
st.markdown("""<style> 
                .block-container {
                    padding-top: 2.5%; 
                    padding-bottom: 0%;
                    }
            </style>""", unsafe_allow_html=True
)

# Home Container
home = st.container()


# home container
with home:
    foreground = Image.open('translate_img.png')
    st.image(foreground)
    tab1, tab2= st.tabs(["Text_to_Speech", "Speech to Speech"])
    font_css = """ 
    <style>
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
        margin-top:30px;
        padding-bottom:25px;
        margin-right:20px;
        margin-left:15px;
        font-size: 20px;
    }
    </style>
    """
# translator
with tab1:
    translate_con = st.container()
    with translate_con:
        from_language, to_language = st.columns(2)
        with from_language:
            first_lang = st.selectbox("From-(Choose Language)", options=(googletrans.LANGUAGES.values()))
        with to_language:
            second_lang = st.selectbox("To-(Choose Language)", options=(googletrans.LANGUAGES.values()))
        # instantiate translator
        translator = Translator()
        # get key from value in language dictionary
        for first_id, first_key in googletrans.LANGUAGES.items():
            if first_key == first_lang:
                initial_lang = first_id

        for second_id, second_key in googletrans.LANGUAGES.items():
            if second_key == second_lang:
                dest_lang = second_id
        # get text
        input_text = st.text_input('Translate', 'Hello World')
        # translation
        translated = translator.translate(input_text,src=first_lang, dest=dest_lang, slow=False)
        # result
        st.write('Translated Text:')
        st.code(translated.text, language="markdown")

        # Text To Speech
        speech = gTTS(text=translated.text,lang=dest_lang, slow=False)
        speech.save('Translated_audio.mp3')
        sound_file = 'Translated_audio.mp3'

        def autoplay_audio(file_path: str):
            with open(file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio controls autoplay="false">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                st.markdown(
                    md,
                    unsafe_allow_html=True,
                )
            return md

        # def play_music():
        #     audio_file = open('Translated_audio.mp3', "rb")
        #     audio_bytes = audio_file.read()
        #     st.audio(audio_bytes, format='audio/mp3') 

        def play_audio():
            os.remove("Translated_audio.mp3")
            date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = "Translated_audio"+date_string+".mp3"
            speech = gTTS(text=translated.text,lang=dest_lang, slow=False)
            speech.save(filename)
            sound_file = filename
            boom = playsound.playsound(sound_file)
            os.remove(filename)

        # play_audio()

        st.button('Translated Audio', on_click=play_audio)
with tab2:
    voice_con = st.container()
    with voice_con:

        # Lets add voice translation
        st.write('Voice to Voice Translation')
        say_col ,trans_col = st.columns([1,.2]) 
        def ready_again():
            with say_col:
                st.code("Say Something", language='markdown')
        def voice_to_voice(): 
            # obtain audio from the microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            # write audio to a WAV file
            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())
            audio_file_ = sr.AudioFile("microphone-results.wav")
            with audio_file_ as source:
                audio_file = r.record(source, duration = 10.0)
                result = r.recognize_google(audio_data=audio_file)                
                with say_col:
                    st.code("Did You Say:"+ f'{result}', language="markdown")
                    st.write("Translation:")
                    voice_translated = translator.translate(result,src=first_lang, dest=dest_lang, slow=False)
                    st.code(voice_translated.text, language='markdown')

                    voice_date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                    voice_file = "Voice_audio"+voice_date_string+".mp3"
                    voice = gTTS(text=voice_translated.text,lang=dest_lang, slow=False)
                    voice.save(voice_file)
                    boom2 = playsound.playsound(voice_file)
                    os.remove(voice_file)
        def master_callback():
            ready_again()
            voice_to_voice()
        st.button('Record', on_click=master_callback)
