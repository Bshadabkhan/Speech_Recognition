#audio file formats
# .mp3
# .flac
# .wav

import wave

object = wave.open("file_example_WAV_1MG.wav","rb") # rb:-read-binary
print ("Number of channels",  object.getnchannels())
print ("Sample width",object.getsampwidth())
print ("frame rate", object.getframerate())
print ("Number of frames", object.getnframes())
print("parameters",object.getparams())

t_audio = object.getnframes() / object.getframerate()
print(t_audio)

frames = object.readframes(-1) 
print(type(frames),type(frames[0]))
print(len(frames) / 2)
object.close()

object_new = wave.open("patrick_new.wav","wb")

object_new.setnchannels(1)
object_new.setsampwidth(2)
object_new.setframerate(16000.0)

object_new.writeframes(frames)

object_new.close()