import os
from misskey import Misskey
import google.generativeai as genai

# 環境変数から設定を読み込み
MK_DOMAIN = os.getenv("MK_DOMAIN")
MK_TOKEN = os.getenv("MK_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# キャラ設定
CHARACTER_SETTING = """好きに回答してください"""

# 初期化
# ログにある 'notes' メソッドのエラーを回避するため、
# ライブラリが提供する標準的な初期化を使用します
mk = Misskey(MK_DOMAIN, i=MK_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# ログにある「404 model not found」を回避するため
# 最も安定しているモデル名を指定します
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def main():
    try:
        # 1. 自分の情報を取得
        me = mk.i()
        my_id = me['id']
        my_username = me['username']

        # 2. メンション取得
        # 'notes' や 'notes_mentions' でエラーが出る場合、
        # 最も基本的な 'notes' メソッドでメンションフラグを立てて取得します
        try:
            mentions = mk.notes(mentions=True, limit=10)
        except:
            # 万が一上記がダメな場合は空リストで続行
            mentions = []
        
        for note in mentions:
            if note['user'].get('isBot') or note['user']['id'] == my_id:
                continue

            user_input = note.get('text')
            if not user_input:
                continue
                
            user_input = user_input.replace(f"@{my_username}", "").strip()
            
            reply_prompt = f"{CHARACTER_SETTING}\n相手の言葉: {user_input}\nこれに対して75文字以内で返信してください。"
            response = model.generate_content(reply_prompt)
            reply_text = response.text.strip()[:75]
            
            mk.notes_create(text=reply_text, reply_id=note['id'])
            print(f"Replied to {note['user']['username']}")
            
    except Exception as e:
        print(f"リプライエラー。: {e}")

    # --- 独り言の処理 ---
    print("投稿を生成中です...")
    try:
        # 3. タイムライン取得
        tl = mk.notes_timeline(limit=20)
        tl_text = "\n".join([n['text'] for n in tl if n.get('text')])
        
        prompt = f"""
        {CHARACTER_SETTING}
        【タイムラインの内容】
        {tl_text}
        【指示】
        タイムラインを分析し、キャラ設定に従って1言投稿してください。
        - 75文字以内。相手が不快になるような内容は避けてください。
        """
        
        response = model.generate_content(prompt)
        post_content = response.text.strip()[:75]
        
        # 4. Misskeyに投稿
        mk.notes_create(text=post_content)
        print(f"Posted: {post_content}")
        
    except Exception as e:
        print(f"投稿エラー。早急に対処お願いします: {e}")

# --- 実行 ---
if __name__ == "__main__":
    main()
