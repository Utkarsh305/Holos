import os
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
from playsound import playsound

dotenv_path = './key.env'
load_dotenv(dotenv_path=dotenv_path)

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the API key
client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content":
             "You are an intelligent assistant."}]

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)
    print ("Processing...")
      #client = OpenAI()
    with open("microphone-results.wav", "wb") as f:
      f.write(audio.get_wav_data())

    with open("microphone-results.wav", "rb") as f:
      transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=f,
      response_format="text",
      )
      print(transcript)

    message = transcript

    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = client.chat.completions.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
    reply = chat.choices[0].message.content 
    print(f"ChatGPT: {reply}") 
    messages.append({"role": "assistant", "content": reply}) 

    speech_filepath = "./speech.wav"
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=reply
    )

    response.stream_to_file(speech_filepath)
    # os.system("afplay " + speech_filepath)
    playsound(speech_filepath)
    print('playing sound using  playsound')
#docker exec -it -d server-db-3 python3 -m jupyterlab --no-browser --ip=0.0.0.0 --port=5000 --allow-root --NotebookApp.token=''



docker exec -it -d server-db-3 python3 -m jupyterlab --no-browser --ip=0.0.0.0 --port=5000 --allow-root --NotebookApp.token=''
