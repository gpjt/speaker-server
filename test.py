import soundfile as sf
import sounddevice as sd
data, samplerate = sf.read("day-i-die.wav")
sd.play(data, samplerate)
input("Hit enter when done")
