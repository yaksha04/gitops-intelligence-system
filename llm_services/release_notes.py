import os, subprocess, requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
os.makedirs('releases', exist_ok=True)

def get_recent_commits():
    result = subprocess.run("git log --oneline -20", capture_output=True, text=True, shell=True)
    commits = result.stdout.strip()
    if not commits:
        commits = """a1b2c3d feat: add user authentication
b2c3d4e fix: resolve payment timeout
c3d4e5f feat: dashboard real-time updates
d4e5f6g docs: update API documentation"""
    return commits

def generate_notes_with_gemini(commits: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY not found in .env file."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt = f"""Generate professional release notes in markdown format.
Format:
# Release v1.0.0 - {datetime.now().strftime('%B %d, %Y')}
## New Features
- ...
## Bug Fixes
- ...
## Summary
One paragraph.

Commits:
{commits}"""
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        if response.status_code == 200:
            return data['choices'][0]['message']['content']
        return f"Error: {data.get('error', {}).get('message', 'Unknown')}"
    except Exception as e:
        return f"Error: {str(e)}"

def generate_release_notes():
    commits = get_recent_commits()
    notes = generate_notes_with_gemini(commits)
    filename = f"releases/RELEASE_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(filename, 'w') as f:
        f.write(notes)
    print(f"Saved: {filename}\n{notes}")
    return notes

if __name__ == "__main__":
    generate_release_notes()
