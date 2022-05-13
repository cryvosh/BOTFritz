import pyaudio
import audioop
import numpy as np

frames = 512
WIDTH = 2
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

device_info = p.get_default_output_device_info()
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1

if not is_wasapi:
    print ("Default output device does not support WASAPI loopback mode.")

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer = 512)

def get_sound():
    data = stream.read(frames)
    lsampe = audioop.tomono(data, 2, 1, 0)
    rsample = audioop.tomono(data, 2, 0, 1)

    temp_l = np.frombuffer(lsampe, np.int16).astype(np.float)
    temp_r = np.frombuffer(rsample, np.int16).astype(np.float)

    lrms = np.sqrt((temp_l*temp_l).sum()/len(temp_l))
    rrms = np.sqrt((temp_r * temp_r).sum() / len(temp_r))

    return (lrms, rrms)

