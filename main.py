import os
import openai
from dotenv import load_dotenv
from agent import Agent
from researcher import Researcher
from conversation import ConversationManager

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def main():
    print("AI Assistant is running...")
    cm = ConversationManager()

    agents = {
        "1": {"name": "Code Generation Agent", "agent": Agent(system_prompt="You are a world-class software developer. You write clean, efficient, and well-documented code.")},
        "2": {"name": "Creative Writer Agent", "agent": Agent(system_prompt="You are a creative writer. You can write poems, stories, and scripts.")},
        "3": {"name": "Researcher Agent", "agent": Researcher()}
    }

    while True:
        print("\nSelect an option:")
        print("1. Start a new conversation")
        print("2. Load a conversation")
        print("Type 'exit' or 'quit' to end.")
        
        choice = input("Your choice: ")

        if choice.lower() in ["exit", "quit"]:
            break
        
        if choice == "1":
            print("\nSelect an agent:")
            for key, value in agents.items():
                print(f"{key}. {value['name']}")
            
            agent_choice = input("Your choice: ")

            if agent_choice.lower() in ["exit", "quit"]:
                break

            if agent_choice in agents:
                agent_info = agents[agent_choice]
                agent = agent_info["agent"]
                agent_name = agent_info["name"]
                
                while True:
                    prompt = input("You: ")
                    if prompt.lower() in ["exit", "quit"]:
                        cm.save_conversation(agent_name, agent.history)
                        break
                    
                    if isinstance(agent, Researcher):
                        response = agent.research(prompt)
                    else:
                        response = agent.chat(prompt)
                    print(f"AI: {response}")
            else:
                print("Invalid choice.")

        elif choice == "2":
            conversations = cm.list_conversations()
            if not conversations:
                print("No saved conversations found.")
                continue
            
            print("\nSelect a conversation to load:")
            for i, conv in enumerate(conversations):
                print(f"{i+1}. {conv}")
            
            conv_choice = input("Your choice: ")
            try:
                conv_index = int(conv_choice) - 1
                if 0 <= conv_index < len(conversations):
                    filename = os.path.join(cm.save_dir, conversations[conv_index])
                    history = cm.load_conversation(filename)
                    
                    # This is a simplified way to resume. A more robust implementation
                    # would be needed to associate the conversation with the correct agent.
                    print("\n--- Conversation Resumed ---")
                    for message in history:
                        print(f"{message['role']}: {message['content']}")
                    print("--- End of Conversation ---")

                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()