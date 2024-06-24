import os
import sys
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def is_ffmpeg_in_path():
    for path in os.environ["PATH"].split(os.pathsep):
        ffmpeg_path = os.path.join(path, "ffmpeg")
        if os.path.isfile(ffmpeg_path) or os.path.isfile(ffmpeg_path + ".exe"):
            return True
    return False

def is_ffprobe_in_path():
    for path in os.environ["PATH"].split(os.pathsep):
        ffprobe_path = os.path.join(path, "ffprobe")
        if os.path.isfile(ffprobe_path) or os.path.isfile(ffprobe_path + ".exe"):
            return True
    return False

if not is_ffmpeg_in_path():
    print("ffmpeg is not found in PATH. Please install FFmpeg and add its bin directory to the PATH.")
    sys.exit(1)

if not is_ffprobe_in_path():
    print("ffprobe is not found in PATH. Please install FFmpeg and add its bin directory to the PATH.")
    sys.exit(1)

# Function to recognize speech
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)
    print("Recognizing...")
    response = {"success": True, "error": None, "transcription": None}

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="en-US")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

# Function to translate text
def translate_text(text, src_lang='en', dest_lang='hi'):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

# Function to convert text to speech and play it
def speak_text(text, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("output.mp3")
        audio = AudioSegment.from_mp3("output.mp3")
        play(audio)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure that ffmpeg is installed and added to your system PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def answer_question(question):
    faq = {
        "what is the procedure to open a bank account": "To open a bank account, you need to visit the bank with your ID proof, address proof, and passport-sized photographs. Fill out the account opening form and submit the necessary documents.",
        "what are the bank working hours": "Our bank operates from 9 AM to 5 PM, Monday to Friday. On Saturdays, we are open from 9 AM to 1 PM.",
        "how can i apply for a loan": "To apply for a loan, visit our bank and fill out the loan application form. Provide the necessary documents, such as income proof and ID proof. Our representative will guide you through the process.",
        "what is the interest rate on savings account": "The interest rate on savings accounts varies. Please visit our bank or check our website for the latest rates.",
        "how can i get a new checkbook": "To get a new checkbook, you can request one online through our banking portal, visit the bank, or contact our customer service.",
        "what is the minimum balance required in savings account": "The minimum balance required for a savings account varies by account type. Please refer to our website or visit the bank for specific details.",
        "how can i update my contact information": "To update your contact information, you can log in to our online banking portal, visit the bank, or call our customer service.",
        "how can i block my lost debit card": "If you have lost your debit card, immediately contact our customer service or use our mobile app to block the card.",
        "how can i activate internet banking": "To activate internet banking, visit our website, click on the 'Register' link, and follow the instructions. You will need your account number and registered mobile number.",
        "what documents are required for a home loan": "Documents required for a home loan include proof of identity, proof of address, income proof, bank statements, and property documents.",
        "how can i check my account balance": "You can check your account balance through our mobile app, internet banking, by visiting an ATM, or calling our customer service.",
        "what are the charges for an international money transfer": "Charges for international money transfers vary based on the amount and destination. Please refer to our website or visit the bank for specific details.",
        "how can i change my atm pin": "To change your ATM PIN, visit any of our ATMs, log in with your card and current PIN, and follow the instructions to change your PIN.",
        "how can i open a fixed deposit account": "To open a fixed deposit account, visit our bank or use our online banking portal. You will need your account details and the amount you wish to deposit.",
        "how can i close my bank account": "To close your bank account, visit the bank with your ID proof and account details. Fill out the account closure form and submit it to the bank representative.",
        "what is the process to update kyc details": "To update your KYC details, visit the bank with your ID proof, address proof, and passport-sized photographs. Fill out the KYC update form and submit the documents.",
        "how can i get a bank statement": "You can get a bank statement through our mobile app, internet banking, or by visiting the bank.",
        "what are the different types of accounts available": "We offer various types of accounts including savings accounts, current accounts, fixed deposits, and recurring deposits.",
        "how can i apply for a credit card": "To apply for a credit card, visit our bank or apply online through our website. You will need your ID proof, address proof, and income proof.",
        "what is the overdraft facility": "An overdraft facility allows you to withdraw more money than you have in your account up to a specified limit. This is subject to approval and interest charges."
    }

    question = question.lower()
    return faq.get(question, "I'm sorry, I don't have an answer to that question. Please contact our customer service for more assistance.")

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Introduce the assistant
    introduction = "Hi, I am Dhwani, an AI chatbot assistant that handles your banking problemsand i am created by team L-MAC. Tell me, how can I help you?"
    print(introduction)
    speak_text(introduction, 'en')

    while True:
        print("\nAsk a question in English:")
        speech_result = recognize_speech_from_mic(recognizer, microphone)

        if speech_result["transcription"]:
            print(f"You said: {speech_result['transcription']}")

            # Check if the transcription is a predefined question
            answer = answer_question(speech_result["transcription"])
            print(f"Answer: {answer}")

            # Announce the answer
            announcement = "The answer is:"
            print(announcement)
            speak_text(announcement, 'en')

            # Translate and speak the answer
            translated_answer = translate_text(answer, 'en', 'hi')
            print(f"Translated to Hindi: {translated_answer}")
            speak_text(translated_answer, 'hi')
        elif speech_result["error"]:
            print(f"Error: {speech_result['error']}")

        print("Do you want to ask another question? (yes/no)")
        continue_response = recognize_speech_from_mic(recognizer, microphone)
        if continue_response["transcription"]:
            if continue_response["transcription"].lower() != "yes":
                print("Exiting the assistant.")
                break
        else:
            print("Sorry, I didn't catch that. Please say 'yes' to continue or 'no' to exit.")

if __name__ == "__main__":
    main()







