# Tests each folder/module and logs any failures
import os, subprocess

folders = ['ai_modules', 'penny_strategies', 'options_strategies', 'news_sentiment', 'execution', 'logs']
for folder in folders:
    for f in os.listdir(os.path.join(os.path.dirname(__file__), folder)):
        if f.endswith('.py'):
            path = os.path.join(folder, f)
            print(f"\U0001F50D Testing {path}")
            try:
                subprocess.run(["python3", path], cwd=os.path.dirname(__file__), check=True)
            except Exception:
                print(f"\u274C Failed: {path}")
