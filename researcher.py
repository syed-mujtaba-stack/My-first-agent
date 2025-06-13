from duckduckgo_search import DDGS
from agent import Agent

class Researcher(Agent):
    def __init__(self, model: str = "openai/gpt-3.5-turbo", system_prompt: str = "You are a world-class researcher. You provide concise and accurate summaries of your findings."):
        super().__init__(model, system_prompt)

    def research(self, query: str):
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
        
        summary_prompt = f"Summarize the following search results for the query '{query}':\n\n"
        for result in results:
            summary_prompt += f"- {result['title']}: {result['body']}\n"
            
        return self.chat(summary_prompt)