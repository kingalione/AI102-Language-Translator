from dotenv import load_dotenv
from datetime import datetime
import os
#from playsound import playsound

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config, translation_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)
        translation_config.speech_recognition_language = 'de-DE'
        translation_config.add_target_language('tr-TR')
        print('Ready to translate from',translation_config.speech_recognition_language)
        
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        print('Ready to use speech service in:', speech_config.region)

        Translate()

    except Exception as ex:
        print(ex)

def Translate():
    translation = ''

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations['tr']
    print(translation)

    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    responseSsml = " \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
            <voice name='tr-TR-EmelNeural'> \
                {} \
                <break strength='weak'/> \
            </voice> \
        </speak>".format(translation)
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()

    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

if __name__ == "__main__":
    main()