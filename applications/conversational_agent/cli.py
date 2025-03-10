from agent import ConversationalAgent
from prompts import PREDEFINED_PROMPTS
import argparse
from datetime import datetime

HELP_MESSAGE = """
Available commands:
- 'quit' : Exit the application
- 'history' : Display conversation history
- 'prompt' : Display current system prompt
- 'set_prompt' : Set a new system prompt
- 'use_prompt <type>' : Use a predefined prompt (types: teacher, french, coder, writer)
- 'list_prompts' : Display available predefined prompts
- 'reset' : Reset the conversation
- 'list_sessions' : List all available sessions
- 'switch_session <session_id>' : Switch to another session
- 'help' : Display this help message
"""

def main():
    parser = argparse.ArgumentParser(description='Conversational AI Agent')
    parser.add_argument('--session', default='default_user', help='Session ID for the conversation')
    parser.add_argument('--system-prompt', help='Initial system prompt')
    parser.add_argument('--prompt-type', choices=list(PREDEFINED_PROMPTS.keys()), help='Use a predefined prompt type')
    parser.add_argument('--db-path', default='conversations.db', help='Path to the database file')
    args = parser.parse_args()

    current_session = args.session
    
    # Select initial prompt
    initial_prompt = None
    if args.prompt_type:
        initial_prompt = PREDEFINED_PROMPTS[args.prompt_type]
    elif args.system_prompt:
        initial_prompt = args.system_prompt

    agent = ConversationalAgent(system_prompt=initial_prompt, db_path=args.db_path)
    print(f"Agent initialized (session: {current_session}). Type 'help' to see available commands.")
    
    while True:
        user_input = input(f"\n[{current_session}] You: ").strip()
        command_parts = user_input.lower().split()
        
        if user_input.lower() == 'quit':
            break
            
        elif user_input.lower() == 'help':
            print(HELP_MESSAGE)
            
        elif user_input.lower() == 'history':
            history = agent.get_conversation_history(current_session)
            for msg_type, content in history:
                print(f"{msg_type}: {content}")
                
        elif user_input.lower() == 'list_sessions':
            sessions = agent.list_sessions()
            print("\nAvailable sessions:")
            for session_id, prompt, last_updated in sessions:
                print(f"- {session_id} (Last activity: {last_updated})")
                print(f"  Prompt: {prompt[:50]}...")
                
        elif command_parts[0] == 'switch_session' and len(command_parts) > 1:
            new_session = command_parts[1]
            current_session = new_session
            print(f"Switched to session: {current_session}")
            
        elif user_input.lower() == 'prompt':
            current_prompt = agent._get_system_prompt(current_session)
            print(f"\nCurrent system prompt:\n{current_prompt}")
            
        elif user_input.lower() == 'set_prompt':
            new_prompt = input("Enter new system prompt: ")
            agent.set_system_prompt(new_prompt, current_session)
            print("System prompt updated.")
            
        elif user_input.lower() == 'list_prompts':
            print("\nAvailable predefined prompts:")
            for prompt_type, prompt_text in PREDEFINED_PROMPTS.items():
                print(f"\n- {prompt_type}:")
                print(f"  {prompt_text}")
                
        elif command_parts[0] == 'use_prompt' and len(command_parts) > 1:
            prompt_type = command_parts[1]
            if prompt_type in PREDEFINED_PROMPTS:
                agent.set_system_prompt(PREDEFINED_PROMPTS[prompt_type], current_session)
                print(f"System prompt changed to: {prompt_type}")
            else:
                print(f"Prompt type '{prompt_type}' not found. Use 'list_prompts' to see available types.")
            
        elif user_input.lower() == 'reset':
            agent.reset_conversation(current_session)
            print("Conversation reset.")
            
        else:
            response = agent.chat(user_input, current_session)
            print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main()
