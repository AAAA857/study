# Import the base64 encoding library.
import base64

# Pass the audio data to an encoding function.
def encode_audio(audio_file):
    with open(audio_file, "rb") as f:
        encoded_content = base64.b64encode(f.read())

    with open(file="./1.txt",mode='wb') as w:
        w.write(encoded_content)



if __name__ == '__main__':
    print(encode_audio(audio_file=r"E:\中石油\16k16bit.wav"))