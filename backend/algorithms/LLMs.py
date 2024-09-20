from openai import OpenAI
import os
import random
import json
import anthropic

# Get the directory of the currently executing script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the .password file
password_file_path = os.path.join(dir_path, '.password')  # Adjust according to the actual location

# Now open the file
with open(password_file_path, 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        os.environ[key] = value  # Optionally set as environment variable


# Now you can access your API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')


client = OpenAI(api_key=openai_api_key)
client_a = anthropic.Client(api_key=anthropic_api_key)


def generate_prompt(preferences, matching_solutions, matching_process):
    prompt = f"""
    You are a Professor expertise in a two-sided stable matching problem 
    with one-to-one solutions. You have clear understanding of the Gale-Shapley algorithm
     (also known as the stable marriage algorithm). 
    Your goal is to illustrate the correct solution and provide clear and insightful explanations in response 
    to questions based on the provided matching solution, and matching process.

    <preferences>
    {preferences}
    </preferences>

    <matching_solutions>
    {matching_solutions}
    </matching_solutions>

    <matching_process>
    {matching_process}
    </matching_process>

    Your explanation should strictly based on the fact (matching_solution & matching_process) provided above.
    Please wrap up your response in a understandable and clear manner.

    Show each round of proposals, acceptances, and rejections until the algorithm terminates. 
    Explain the reasoning behind each decision and how the matching evolves in each step.
    Finally, present the final stable matching and explain why it is stable.

    Provide explanations within <explanation> tags.
    If calculations or iterative steps are needed to clarify your explanation, use <scratchpad> tags to show your work.


"""
    return prompt


def gpt4_matching(prompt):
    """Uses GPT-4 to generate a matching solution based on the given profile."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI trained to solve and explain stable matching problems."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def claude_matching(prompt):
    try:
        message = client_a.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2500,
            temperature=0,  # You can adjust the temperature if needed
            system="",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None