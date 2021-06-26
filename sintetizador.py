import pyttsx3

tts = pyttsx3.init()

def hablar(texto):
  tts.say(texto)
  tts.runAndWait()
