import os
import time
from misskey import Misskey
import google.generativeai as genai

# 環境変数から設定を読み込み
MK_DOMAIN = os.getenv("MK_DOMAIN")
MK_TOKEN = os.getenv("MK_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# キャラ設定
CHARACTER_SETTING = """好きに回答してください
"""

# 初期化
mk = Misskey(MK_DOMAIN, i=MK_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    try:
        my_id = mk.i()['id']
        # メンション取得
        mentions = mk.notes_mentions(limit=10)
        for note in mentions:
            # ボット除外
            if note['user'].get('isBot') or note['user']['id'] == my_id:
                print(f"Skipping bot or self: {note['user']['username']}")
                continue

            # AIへの入力（メンション部分を除去）
            user_input = note['text'].replace(f"@{mk.i()['username']}", "").strip()
            
            # Geminiで返信内容を生成
            reply_prompt = f"{CHARACTER_SETTING}\n相手の言葉: {user_input}\nこれに対して75文字以内で返信して。"
            reply_text = model.generate_content(reply_prompt).text.strip()[:75]
            
            # 返信を実行
            mk.notes_create(text=reply_text, reply_id=note['id'])
            print(f"Replied to {note['user']['username']}")
            
    except Exception as e:
        print(f"リプライエラー: {e}")

    # --- 独り言の処理 ---
    print("投稿を生成中です...")
    try:
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
        - タイムラインの話題に触れてもいいし、全体的な雰囲気に文句を言ってもいい。
        - ハッシュタグや絵文字は最小限に。
        - 挨拶ではなく、今この瞬間の「それっぽい独り言」にすること。
        """
        
        response = model.generate_content(prompt)
        post_content = response.text.strip()[:75]
        
        # 3. Misskeyに投稿
        mk.notes_create(text=post_content)
        print(f"Posted: {post_content}")
        
    except Exception as e:
        print(f"独り言エラー: {e}")

# --- 実行 ---
if __name__ == "__main__":
    main()
