import sys
import argparse
import os
from dotenv import load_dotenv
from agent import Agent
from llm_factory import get_llm
import pandas

# .env loading is a must
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Nightwatch: The Simple Agent Engine")
    parser.add_argument("alert", help="Tell the agent what to investigate")
    parser.add_argument("--provider", help="Switch LLM (e.g. mock, gemini, groq, openai)")
    args = parser.parse_args()

    # Manual override for the provider
    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider

    # 1. Grab the "brain"
    try:
        llm = get_llm()
        name = os.environ.get("LLM_PROVIDER", "mock").upper()
        print(f"--- Nightwatch Active (using {name}) ---")
    except Exception as e:
        print(f"Fatal error during setup: {e}")
        sys.exit(1)

    # 2. Fire up the agent
    investigator = Agent(llm=llm)
    try:
        investigator.run(args.alert)
    except KeyboardInterrupt:
        print("\nStopping investigation.")
    except Exception as e:
        print(f"\nSomething went wrong: {e}")

if __name__ == "__main__":
    main()
