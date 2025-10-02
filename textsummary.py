import torch
import gradio as gr

# Use a pipeline as a high-level helper
from transformers import pipeline

model_path = "C:/Users/danie/.cache/huggingface/hub/models--sshleifer--distilbart-cnn-12-6/snapshots/a4f8f3ea906ed274767e9906dbaede7531d660ff"
#path in files

text_summary = pipeline("summarization", model= model_path, torch_dtype = torch.bfloat16)
#other pipelines like translation, question-answering
#torch.bfloat16 uses less memory

#wall of text goes in these quotes
text = """The sounds that are heard in everyday life are not characterized by a single frequency. Instead, they consist of a sum of pure sine frequencies, each one at a different amplitude. When humans hear these frequencies simultaneously, we can recognize the sound. This is true for both "non-musical" sounds (e.g. water splashing, leaves rustling, etc.) and for "musical sounds" (e.g. a piano note, a bird's tweet, etc.). This set of parameters (frequencies, their relative amplitudes, and how the relative amplitudes change over time) are encapsulated by the timbre of the sound. Fourier analysis is the technique that is used to determine these exact timbre parameters from an overall sound signal; conversely, the resulting set of frequencies and amplitudes is called the Fourier series of the original sound signal.

In the case of a musical note, the lowest frequency of its timbre is designated as the sound's fundamental frequency. For simplicity, we often say that the note is playing at that fundamental frequency (e.g. "middle C is 261.6 Hz"),[3] even though the sound of that note consists of many other frequencies as well. The set of the remaining frequencies is called the overtones (or the harmonics, if their frequencies are integer multiples of the fundamental frequency) of the sound.[4] In other words, the fundamental frequency alone is responsible for the pitch of the note, while the overtones define the timbre of the sound. The overtones of a piano playing middle C will be quite different from the overtones of a violin playing the same note; that's what allows us to differentiate the sounds of the two instruments. There are even subtle differences in timbre between different versions of the same instrument (for example, an upright piano vs. a grand piano).

Additive synthesis aims to exploit this property of sound in order to construct timbre from the ground up. By adding together pure frequencies (sine waves) of varying frequencies and amplitudes, we can precisely define the timbre of the sound that we want to create. """


print(text_summary(text))

def summary (input):
    output = text_summary(input)
    return output(0)['summary_text']

gr.close_all()

#demo = gr.Interface(fn = summary, inputs = "text", outputs = "text")
demo = gr.Interface(fn = summary, 
                    inputs = [gr.Textbox(label = "Input text to summarize.", lines = 6)], 
                    outputs = [gr.Textbox(label = "Summarized text.", lines = 4)],
                    title = "AI Text Summarizer", 
                    description = "This application is used to SUMMARIZE the given text. ") 
demo.launch()