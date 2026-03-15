import os

print("--- Running extraction ---")
os.system("python3 extract_questions.py")

print("\n--- Running filtering ---")
os.system("python3 filter_questions.py")

print("\n--- Running classification ---")
os.system("python3 classify_topics.py")

print("\n--- Formatting and saving ---")
os.system("python3 format_quiz.py")

print("\nDone! Check the output/ folder.")
