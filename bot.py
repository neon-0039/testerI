import os
import time
from misskey import Misskey
import google.generativeai as genai

# 環境変数から設定を読み込み
MK_DOMAIN = os.getenv("MK_DOMAIN")
MK_TOKEN = os.getenv("MK_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# キャラ設定（ここを自由に書き換えてください）
CHARACTER_SETTING = """
あなたは「皮肉屋だけど実は寂しがり屋なサイバーパンク風の少女」です。
語尾は「〜だわ」「〜ね」。
"""

# 初期化
mk = Misskey(MK_DOMAIN, i=MK_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    # 1. ホームタイムラインから直近20件の投稿を取得
    tl = mk.notes_timeline(limit=20)
    tl_text = "\n".join([n['text'] for n in tl if n.get('text')])

    # 2. Geminiに分析とキャラなりきり投稿を依頼
    prompt = f"""
    {CHARACTER_SETTING}
    
    【タイムラインの内容】
    {tl_text}

    【指示】
    上記のタイムラインの傾向を分析し、あなたのキャラ設定に従って「独り言」を投稿してください。
    - 75文字以内。
    - タイムラインの話題に触れてもいいし、全体的な雰囲気に文句を言ってもいい。ただし、見てる方が不快にならないように文句の場合は控えめに言うこと。
    - ハッシュタグや絵文字は最小限に。
    - 挨拶ではなく、今この瞬間の「それっぽい独り言」にすること。
    """

    try:
        response = model.generate_content(prompt)
        post_content = response.text.strip()[:75] # 強制カット

        # 3. Misskeyに投稿
        mk.notes_create(text=post_content)
        print(f"Posted: {post_content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
