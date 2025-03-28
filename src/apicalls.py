

class Gemma3:

    def get_genai_path(self):
        return '/v1/chat/completions'

    def get_metrics_path(self):
        return '/metrics'

    def build_request_data(self, user_prompt, max_tokens):
        data = {
            "model": "google/gemma-3-1b-it",
            "messages": [
                {
                "role": "user",
                "content": user_prompt
                }
            ],
            "max_tokens": max_tokens

        }
        return data


class Llama3:

    def get_genai_path(self):
        return '/v1/completions'

    def get_metrics_path(self):
        return '/metrics'

    def build_request_data(self, user_prompt, max_tokens):
        data = {
            "model": "meta-llama/Meta-Llama-3-8B",

            "model": "meta-llama/Meta-Llama-3-8B",
            "prompt": user_prompt, 
            "use_beam_search": False, 
            "max_tokens": max_tokens,
            "temperature":1.0
        }
        return data



models = { 'gemma3-1b': Gemma3(),
           'llama3-8b': Llama3() }

def get_model(modelstr):

    if not modelstr in models.keys():
        raise ValueError(f'model {modelstr} does not have an apicall definition. check apicalls.py')

    return models[modelstr]

def get_available_models():
    print (list(models.keys()))

if __name__ == "__main__":
    get_available_models()
