import os
import time
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
# モデル名を明示的に指定
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    try:
        # 自分の情報を取得
        me = mk.i()
        my_id = me['id']
        my_username = me['username']

        # 1. メンション取得 (notes_mentionsをnotesメソッド経由に修正)
        # サーバーによって仕様が異なるため、より汎用的な取得方法にします
        mentions = mk.notes(mentions=True, limit=10)
        
        for note in mentions:
            # ボット除外
            if note['user'].get('isBot') or note['user']['id'] == my_id:
                continue

            # AIへの入力（メンション部分を除去）
            user_input = note.get('text', "").replace(f"@{my_username}", "").strip()
            if not user_input:
                continue
            
            # Geminiで返信内容を生成
            reply_prompt = f"{CHARACTER_SETTING}\n相手の言葉: {user_input}\nこれに対して75文字以内で返信して。"
            response = model.generate_content(reply_prompt)
            reply_text = response.text.strip()[:75]
            
            # 返信を実行
            mk.notes_create(text=reply_text, reply_id=note['id'])
            print(f"Replied to {note['user']['username']}")
            
    except Exception as e:
        print(f"リプライエラー。早急に対処お願いします: {e}")

    # --- 独り言の処理 ---
    print("投稿を生成中です...")
    try:
        # 1. タイムライン取得
        tl = mk.notes_timeline(limit=20)
        tl_text = "\n".join([n['text'] for n in tl if n.get('text')])
        
        # 2. Geminiに投稿を依頼
        prompt = f"""
        {CHARACTER_SETTING}
        【タイムラインの内容】
        {tl_text}
        【指示】
        上記のタイムラインの傾向を分析し、あなたのキャラ設定に従って「独り言」を投稿してください。
        - 75文字以内。
        - 挨拶ではなく、今この瞬間の「それっぽい独り言」にすること。
        """
        
        response = model.generate_content(prompt)
        post_content = response.text.strip()[:75]
        
        # 3. Misskeyに投稿
        mk.notes_create(text=post_content)
        print(f"Posted: {post_content}")
        
    except Exception as e:
        print(f"投稿エラー。早急に対処お願いします: {e}")

# --- 実行 ---
if __name__ == "__main__":
    main()
