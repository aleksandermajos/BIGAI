from transformers import BarkModel
import torch
from transformers import AutoProcessor
import torch
from transformers import set_seed
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from bark import SAMPLE_RATE, generate_audio, preload_models

model = BarkModel.from_pretrained("suno/bark-small")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)
processor = AutoProcessor.from_pretrained("suno/bark-small")

text_prompt = """
Jak ciepła i cicha jest
noc sierpniowa ,
w którą listki leciutko,
wiatr muska.
Drzewa szumią cicho -
jakby od niechcenia.
A niebo się pyszni
"""
inputs = processor(text_prompt).to(device)

def measure_latency_and_memory_use(model, inputs, nb_loops = 1):

  # define Events that measure start and end of the generate pass
  start_event = torch.cuda.Event(enable_timing=True)
  end_event = torch.cuda.Event(enable_timing=True)

  # reset cuda memory stats and empty cache
  torch.cuda.reset_peak_memory_stats(device)
  torch.cuda.empty_cache()
  torch.cuda.synchronize()

  # get the start time
  start_event.record()

  # actually generate
  for _ in range(nb_loops):
        # set seed for reproductibility
        set_seed(0)
        output = model.generate(**inputs, do_sample = True, fine_temperature = 0.4, coarse_temperature = 0.8)

  # get the end time
  end_event.record()
  torch.cuda.synchronize()

  # measure memory footprint and elapsed time
  max_memory = torch.cuda.max_memory_allocated(device)
  elapsed_time = start_event.elapsed_time(end_event) * 1.0e-3

  print('Execution time:', elapsed_time/nb_loops, 'seconds')
  print('Max memory footprint', max_memory*1e-9, ' GB')

  return output

with torch.inference_mode():
  speech_output = measure_latency_and_memory_use(model, inputs, nb_loops = 1)
  write_wav("pl4.wav", SAMPLE_RATE, speech_output)