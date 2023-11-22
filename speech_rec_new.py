import streamlit as st
import speech_recognition as sr
import pyaudio
import wave

def transcribe_speech(recognizer, audio, api, language):
    try:
        if api == 'Google':
            text = recognizer.recognize_google(audio, language=language)  # Google Speech Recognition
        elif api == 'Bing':
            text = recognizer.recognize_sphinx(audio, language=language)
        elif api == 'Amazon':
            text = recognizer.recognize_amazon(audio, language=language)
        elif api == "Watson":
            text = recognizer.recognize_ibm(audio, language=language)
        else:
            text = "Invalid API selected."

        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from the service; {e}"

def main():
    st.title("Speech Recognition App")

    language = st.selectbox("Select Language", ["en-US", "es-ES"])
    api = st.selectbox("Select Speech Recognition API", ["Google", "Bing", "Amazon", "Watson"])
    recording = False

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with st.expander("Recognition Controls"):
        if st.button("Start Recording"):
            recording = True
            st.write("Recording...")

        if st.button("Stop Recording"):
            recording = False
            st.write("Recording Stopped.")

    if recording:
        try:
            with microphone as source:
                audio = recognizer.listen(source)
            text = transcribe_speech(recognizer, audio, api, language)
            st.write("Transcribed Text:")
            st.write(text)

            if st.button("Save to File"):
                with open("transcribed_text.txt", "w") as file:
                    file.write(text)
                    st.write("Text saved to transcribed_text.txt")

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
