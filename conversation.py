import json
import os

class ConversationManager:
    def __init__(self, save_dir="conversations"):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_conversation(self, agent_name, history):
        filename = os.path.join(self.save_dir, f"{agent_name}_{len(os.listdir(self.save_dir)) + 1}.json")
        with open(filename, "w") as f:
            json.dump(history, f, indent=4)
        print(f"Conversation saved to {filename}")

    def load_conversation(self, filename):
        with open(filename, "r") as f:
            return json.load(f)

    def list_conversations(self):
        return [f for f in os.listdir(self.save_dir) if f.endswith(".json")]