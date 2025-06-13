import openai

class Agent:
    def __init__(self, model: str = "openai/gpt-3.5-turbo", system_prompt: str = "You are a helpful assistant."):
        self.model = model
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": self.system_prompt}]

    def chat(self, prompt: str):
        self.history.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
        )
        message = response.choices[0].message
        self.history.append(message)
        return message.content