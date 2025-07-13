import os
import openai
import json
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"🔥 Your task: Write a viral YouTube Shorts script about: '{topic}'\n\n"
        "✨ SCRIPT RULES:\n"
        "1. Write 10 to 15 lines max.\n"
        "2. Each line must be 1 short punchy sentence — max 20 words.\n"
        "3. Each line must be a bold opinion, hot take, or shocking idea — make viewers want to comment.\n"
        "4. Use phrases like: 'Hot take:', 'What if...', 'Let’s be real...', 'No one talks about...', 'Imagine if...'\n"
        "5. Only mention real, famous, canon characters/items/powers from the anime/game.\n"
        "6. DO NOT write a story or summary — ONLY spicy takes people can argue about.\n"
        "7. The last line must invite comments — e.g., 'Agree or nah?', 'Drop your take in the comments.'\n\n"
        "🎯 KEYWORD RULES:\n"
        "- Each line must have a keyword: a real, official name, item, or power from the topic.\n"
        "- 1 to 3 words max.\n"
        "- No generic or emotional words. Must be search-friendly.\n"
        "- Must be unique per line.\n"
        "✅ Examples: 'Naruto Sage Mode', 'Gojo Infinity', 'Zoro Three Swords'\n\n"
        "✨ FORMAT:\n"
        "{\n"
        "  \"script\": [\n"
        "    {\"sentence\": \"Your short line.\", \"keyword\": \"Your official keyword.\"},\n"
        "    ...\n"
        "  ],\n"
        "  \"mood\": \"<one-word mood for music>\",\n"
        "  \"title\": \"<punchy YouTube title>\",\n"
        "  \"description\": \"<short YouTube description>\",\n"
        "  \"tags\": [\"<tag1>\", \"<tag2>\", ...]\n"
        "}\n\n"
        "Return RAW JSON only. No explanations. No extra text."
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a genius YouTube Shorts scriptwriter. "
                        "You create short, viral, controversial takes about anime/games with powerful keywords for GIF search."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
        )

        raw = response['choices'][0]['message']['content'].strip()
        print("🪵 RAW RESPONSE:\n", raw)

        match = re.search(r"\{[\s\S]+\}", raw)
        if not match:
            print("⚠️ No valid JSON object found in response.")
            return None

        cleaned_json = match.group(0)

        cleaned_json = re.sub(r",\s*([}\]])", r"\1", cleaned_json)
        cleaned_json = cleaned_json.replace("“", "\"").replace("”", "\"")
        cleaned_json = cleaned_json.replace("‘", "'").replace("’", "'")

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            f.write(cleaned_json)

        return json.loads(cleaned_json)

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
