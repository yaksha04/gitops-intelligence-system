import os, subprocess, requests
from dotenv import load_dotenv
load_dotenv()

def get_code_diff():
    result = subprocess.run("git diff HEAD~1 HEAD", capture_output=True, text=True, shell=True)
    diff = result.stdout
    return diff[:6000] if diff else "Sample diff for demo purposes."

def review_with_gemini(diff: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY not found in .env file."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt = f"""You are a senior DevOps engineer doing a code review.
Analyze this git diff and provide:
1. Security Issues (if any)
2. Potential Bugs (if any)
3. What looks good
4. Top 2-3 improvement suggestions
Keep it short and actionable. Use bullet points.

Git Diff:
{diff}"""
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        if response.status_code == 200:
            return data['choices'][0]['message']['content']
        return f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

def post_github_comment(review, pr_number=None):
    print("AI CODE REVIEW:"); print(review)

if __name__ == "__main__":
    diff = get_code_diff()
    review = review_with_gemini(diff)
    post_github_comment(review)
