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
mk = Misskey(MK_DOMAIN, i=MK_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# 修正：404エラーを回避する最新のモデル指定
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    try:
        # 1. 自分の情報を取得
        me = mk.i()
        my_id = me['id']
        my_username = me['username']

        # 2. メンション取得
        try:
            mentions = mk.notes_mentions(limit=10)
        except Exception as e:
            print(f"メンション取得に失敗しました（スキップします）: {e}")
            mentions = []
        
        for note in mentions:
            if note['user'].get('isBot') or note['user']['id'] == my_id:
                continue

            user_input = note.get('text')
            if not user_input:
                continue
                
            user_input = user_input.replace(f"@{my_username}", "").strip()
            
            reply_prompt = f"{CHARACTER_SETTING}\n相手の言葉: {user_input}\nこれに対して75文字以内で返信してください。"
            
            # AI返信生成
            response = model.generate_content(reply_prompt)
            reply_text = response.text.strip()[:75]
            
            # Misskeyにリプライを投稿
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
        
        # AI独り言生成
        response = model.generate_content(prompt)
        post_content = response.text.strip()[:75]
        
        # 4. Misskeyにホーム投稿
        mk.notes_create(text=post_content)
        print(f"Posted: {post_content}")
        
    except Exception as e:
        print(f"投稿エラー。早急に対処お願いします: {e}")

# --- 実行 ---
if __name__ == "__main__":
    main()
