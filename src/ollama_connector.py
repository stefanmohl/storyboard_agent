import requests
import json
import sys

baseurl="http://localhost:11434/api/"

# Change the settings you want for a model. You can find the docs at:
# https://github.com/ollama/ollama/blob/main/docs/modelfile.md
model_settings={
    "model": "mistral:7b",
    "system": "You are part of a question and answering system. You will respond to messages, sometimes machine generated, so you will follow the instructions carefully and with perfect precision. Each time you respond, you will carefully look through the whole history of the conversation to see if it is making progress. If you find that your responses are not helping the system make progress, you will give an analysis of why the system is stuck. Later on, you will be given that analysis back and you will find a way to progress based on that analysis.",
    "options": {
#        "mirostat": 1,
#        "mirostat_eta": 0.6,
#        "mirostat_tau": 0.8,
#        "num_ctx": 1024,
#        "num_gqa": 1,
#        "num_gpu": 1,
#        "num_thread": 8,
#        "repeat_last_n": 33,
#        "repeat_penalty": 1.2,
        "temperature": 0.8,
        "seed": 42,
#        "stop": ["\n", "user:"],
#        "tfs_z": 0.5,
#        "num_predict": 100,
#        "top_k": 20,
#        "top_p": 0.9,
#        "typical_p": 0.7,
#        "num_keep": 5,
#        "presence_penalty": 1.5,
#        "frequency_penalty": 1.0,
#        "penalize_newline": True,
#        "numa": False,
#        "num_batch": 2,
#        "main_gpu": 0,
#        "low_vram": False,
#        "f16_kv": True,
#        "vocab_only": False,
#        "use_mmap": True,
#        "use_mlock": False,
#        "rope_frequency_base": 1.1,
#        "rope_frequency_scale": 0.8,
    }
#    "stream": False,
}

url = baseurl + 'chat'

test_messages = {
    "messages": [
        {"role": "user", "content": "why is the sky blue?"},
        {"role": "assistant", "content": "due to rayleigh scattering."},
        {"role": "assistant", "content": "The Earth's atmosphere scatters short-wavelength light, such as blue and violet light, more than longer wavelengths like red, orange, and yellow. When we look up at the sky, we see it appearing blue because of this scattering process. However, during sunrise or sunset, the sky can appear red, pink, or orange due to the presence of more longer wavelengths in the path of the sunlight as it passes through more of the Earth's atmosphere."},
        {"role": "user", "content": "how is that different than mie scattering?"},
    ]
}

{
    'snippets': [],
    'texts': [],
    'result': ""
}

def storyboard2ollama(storyboard):
    messages = []
    for exchange in storyboard:
        messages += [{'role': 'user', 'content': '\n'.join(exchange['texts'])}] if exchange['texts'] else ""
        messages += [{'role': 'assistant', 'content': exchange['result']}] if exchange['result'] else ""
    return {'messages': messages}

def generate(messages):
    ollama_messages = storyboard2ollama(messages)
    request_params= { **model_settings, **ollama_messages }
    full_text = ""
    #print(f"{messages}")
    #print(f"{ollama_messages}")
    with requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(request_params), stream=True) as response:
        for line in response.iter_lines():
            if line:  # filter out keep-alive newlines
                token = json.loads(line.decode('utf-8'))['message']['content']
                print(token, end='')
                sys.stdout.flush()
                full_text += token
    print()
    #print(f'response is: {len(full_text)}:"{full_text}"')
    return full_text

if __name__ == '__main__':
    print(generate(test_messages))
