import streamlit as st
import speech_recognition as sr

def transcribe_speech(recognizer, audio, api, language):
    try:
        if api == 'Google':
            text = recognizer.recognize_google(audio, language=language) 
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

    file_output = st.empty()
    language = st.selectbox("Select Language", ["en-US", "es-ES", "fr-FR"])
    api = st.selectbox("Select Speech Recognition API", ["Google", "Bing", "Amazon", "Watson"])
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        st.checkbox("Pause/Resume Recognition")  # Logic to pause/resume recognition

        while True:
            st.write("Listening...")
            audio = recognizer.listen(source)

            try:
                text = transcribe_speech(recognizer, audio)
                file_output.text_area("Transcribed Text", text)

                if st.button("Save to File"):
                    with open("transcribed_text.txt", "w") as file:
                        file.write(text)
                        st.write("Text saved to transcribed_text.txt")

            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
