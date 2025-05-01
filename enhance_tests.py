import os
import json
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Directory to store test files
output_dir = "test"
os.makedirs(output_dir, exist_ok=True)

def get_unique_filename(base_name):
    """Generate a unique filename by adding a suffix if needed."""
    name, ext = os.path.splitext(base_name)
    candidate = f"{name}_test{ext}"
    counter = 1
    while os.path.exists(os.path.join(output_dir, candidate)):
        candidate = f"{name}_test_{counter}{ext}"
        counter += 1
    return candidate

def call_chatgpt(prompt):
    """Send the prompt to OpenAI and return the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for cheaper and faster output
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return None

def main():
    with open("prompts.json", "r") as f:
        prompts = json.load(f)

    for prompt_data in prompts:
        file_path = prompt_data["file_path"]
        prompt = prompt_data["prompt"]

        print(f"Processing: {file_path}")

        response = call_chatgpt(prompt)
        if not response:
            print(f"Skipping due to error: {file_path}")
            continue

        # Determine output filename
        base_name = os.path.basename(file_path)
        test_filename = get_unique_filename(base_name)
        test_path = os.path.join(output_dir, test_filename)

        with open(test_path, "w") as out_file:
            out_file.write(response)

        print(f"Test written to: {test_path}")

if __name__ == "__main__":
    main()
