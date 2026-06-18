import argparse
import json
import os
import time
import re
from pathlib import Path

# Try importing the gemini package, if it fails, instruct the user to install it.
try:
    from google import genai
except ImportError:
    print("Error: The 'google-genai' package is not installed.")
    print("Please install it by running: pip install google-genai")
    exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate curriculum datasets using Google Gemini AI.")
    parser.add_argument('--grade', required=True, help="Target grade (e.g., 'grade12')")
    parser.add_argument('--subject', required=True, help="Target subject (e.g., 'mathematics')")
    parser.add_argument('--topic', required=True, help="Specific topic (e.g., 'Calculus')")
    parser.add_argument('--count', type=int, default=50, help="Total number of questions to generate")
    parser.add_argument('--batch-size', type=int, default=50, help="Questions per API request")
    parser.add_argument('--api-key', help="Gemini API Key (can also use GEMINI_API_KEY env var)")
    parser.add_argument('--output-file', help="Optional custom output filename (e.g., paper1_calculus.json)")
    return parser.parse_args()

def extract_json_from_response(text):
    """Attempt to extract a JSON array from the response text."""
    # Find the first '[' and last ']'
    start_idx = text.find('[')
    end_idx = text.rfind(']')

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = text[start_idx:end_idx+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse extracted JSON: {e}")
            return None
    return None

def update_map_json(grade, subject, topic, filename):
    map_path = Path('map.json')
    if map_path.exists():
        with open(map_path, 'r') as f:
            try:
                map_data = json.load(f)
            except json.JSONDecodeError:
                map_data = {}
    else:
        map_data = {}

    if grade not in map_data:
        map_data[grade] = {}

    if subject not in map_data[grade]:
        map_data[grade][subject] = []

    # Check if file already mapped for this subject
    file_exists = False
    for entry in map_data[grade][subject]:
        if entry.get('file') == filename:
            file_exists = True
            break

    if not file_exists:
        map_data[grade][subject].append({
            "file": filename,
            "label": topic
        })

        with open(map_path, 'w') as f:
            json.dump(map_data, f, indent=2)
        print(f"Updated map.json with {filename} under {grade}/{subject}")

def generate_questions(grade, subject, topic, batch_size, client):
    prompt = f"""
You are an expert curriculum developer and teacher for South African schools.
Your task is to generate {batch_size} unique, high-quality multiple-choice questions for Grade {grade} {subject} on the topic of "{topic}".

STRICT REQUIREMENTS FOR EACH QUESTION:
1. It must have EXACTLY 1 correct answer (field: "answer").
2. It must have AT LEAST 6 unique, plausible distractors (field: "distractors"). The distractors MUST NOT include the correct answer.
3. The format MUST be a strict JSON array of objects.
4. DO NOT include any markdown formatting, conversational text, or code block backticks in your output. JUST the raw JSON array.
5. Provide a brief explanation for the correct answer in the "explanation" field.

OUTPUT FORMAT:
[
  {{
    "question": "What is the derivative of x^2?",
    "answer": "2x",
    "distractors": ["x", "2", "x^2", "0", "2x^2", "1/2 x^2", "x^3/3"],
    "explanation": "Using the power rule, bring down the exponent and subtract 1 from the power."
  }},
  ...
]

Generate {batch_size} questions now:
"""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text

        questions = extract_json_from_response(text)
        if questions is None:
            # Try raw parsing if no brackets found (in case AI returned just the array)
            try:
                questions = json.loads(text)
            except json.JSONDecodeError:
                print("Failed to parse response as JSON. Raw response:")
                print(text)
                return []

        if isinstance(questions, list):
            return questions
        else:
            print("Response was JSON but not a list.")
            return []

    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            print(f"Rate limit hit: {error_msg}")
            # Try to extract "retry in X.Xs"
            match = re.search(r'retry in ([\d\.]+)s', error_msg)
            if match:
                wait_time = float(match.group(1))
                return {"error": "rate_limit", "wait_time": wait_time}
            else:
                return {"error": "rate_limit", "wait_time": 60.0}
        print(f"Error during API call: {e}")
        return []

def main():
    args = parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key must be provided via --api-key or GEMINI_API_KEY environment variable.")
        exit(1)

    client = genai.Client(api_key=api_key)

    # Setup directories
    subject_dir = args.subject.lower().replace(' ', '_')
    grade_dir = args.grade.lower().replace(' ', '')

    out_dir = Path('dataset') / grade_dir / subject_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine filename
    if args.output_file:
        filename = args.output_file
    else:
        clean_topic = re.sub(r'[^a-z0-9_]', '', args.topic.lower().replace(' ', '_'))
        filename = f"{clean_topic}.json"

    filepath = out_dir / filename

    all_questions = []

    # Load existing if any
    if filepath.exists():
        with open(filepath, 'r') as f:
            try:
                all_questions = json.load(f)
                print(f"Loaded {len(all_questions)} existing questions from {filepath}")
            except json.JSONDecodeError:
                print(f"Warning: {filepath} exists but is not valid JSON. Starting fresh.")

    remaining = args.count - len(all_questions)

    if remaining <= 0:
        print(f"Target count of {args.count} already reached. Exiting.")
        update_map_json(grade_dir, subject_dir, args.topic, filename)
        return

    print(f"Generating {remaining} questions in batches of {args.batch_size}...")

    while remaining > 0:
        current_batch_size = min(remaining, args.batch_size)
        print(f"Requesting {current_batch_size} questions...")

        batch_questions = generate_questions(args.grade, args.subject, args.topic, current_batch_size, client)

        if isinstance(batch_questions, dict) and batch_questions.get("error") == "rate_limit":
            wait_time = batch_questions.get("wait_time", 60.0) + 1.0 # Add 1s buffer
            print(f"Rate limited. Waiting for {wait_time:.1f} seconds before retrying...")
            time.sleep(wait_time)
            continue

        if not batch_questions:
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue

        valid_questions = []
        for q in batch_questions:
            # Validate format
            if 'question' in q and 'answer' in q and 'distractors' in q:
                if isinstance(q['distractors'], list) and len(q['distractors']) >= 6:
                    valid_questions.append(q)
                else:
                    print(f"Warning: Question skipped. Not enough distractors: {q.get('question')[:30]}...")
            else:
                 print(f"Warning: Question skipped. Missing required fields.")

        if valid_questions:
            all_questions.extend(valid_questions)
            remaining -= len(valid_questions)
            print(f"Successfully added {len(valid_questions)} questions. Total: {len(all_questions)}. Remaining: {remaining}")

            # Save progress
            with open(filepath, 'w') as f:
                json.dump(all_questions, f, indent=2)
        else:
            print("No valid questions in this batch. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        if remaining > 0:
             print("Waiting 5 seconds before next request...")
             time.sleep(5)

    print(f"Finished generating questions. Total: {len(all_questions)} saved to {filepath}")
    update_map_json(grade_dir, subject_dir, args.topic, filename)

if __name__ == "__main__":
    main()
