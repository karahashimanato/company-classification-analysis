import requests
from datetime import datetime, timedelta
import time
import os



# 設定情報
API_KEY = "7aab7a8baca04e8bbf37995024e913a1"
BASE_URL = "https://api.edinet-fsa.go.jp/api/v2/documents.json"

START_DATE = datetime(2025, 4, 1)
END_DATE = datetime(2026, 3, 31)
# パラメータの設定 (仕様書 3-1-1 参照)

current_date = START_DATE

SAVE_DIR = "../data/edinet_data"

# もし保存先フォルダがなければ作成する[cite: 1]
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
    print(f"ディレクトリ '{SAVE_DIR}' を作成しました。")

while current_date <= END_DATE:
    remaining_days = (END_DATE - current_date).days
    print(f"残り {remaining_days} 日分を処理中... ({current_date.strftime('%Y-%m-%d')})")
    date_str = current_date.strftime("%Y-%m-%d")
    print(f"---{date_str}のデータを取得中---")

    params = {
        "date": date_str,      # ファイル日付
        "type": "2",               # 提出書類一覧及びメタデータを取得
        "Subscription-Key":API_KEY # 発行したAPIキー
    }

    try:
        # APIリクエスト送信 (仕様書 3-1-1 参照)
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # エラーチェック
        
        data = response.json()
        document_list = [
    "内国投資信託受益証券", "外国会社報告書", "内国信託受益証券等", 
    "内国投資証券", "外国投資証券", "外国投資信託受益証券",
    "特定目的会社", "投資法人", "組合契約"
]
        # 取得した書類をループで回して「有価証券報告書」を探す
        # 120 は「有価証券報告書」の書類種別コード[cite: 1]
        for doc in data.get("results", []):
            description = doc.get("docDescription") or ""

            is_asr = doc.get("docTypeCode") == "120"
            has_excluded_keyword = any(keyword in description for keyword in document_list)
            if  is_asr and not has_excluded_keyword:
                print(f"書類名: {doc.get('docDescription')}")
                print(f"提出者: {doc.get('filerName')}")
                print(f"書類管理番号 (docID): {doc.get('docID')}")
                print("-" * 30)

                # --- ループ内（if not is_excluded: の中）の処理 ---
                doc_id = doc.get('docID')
                # 保存先のフルパスを作成 (例: "edinet_data/S100XXXX.zip")
                file_path = os.path.join(SAVE_DIR, f"{doc_id}.zip")

                # ダウンロード用のURL[cite: 1]
                get_url = f"https://api.edinet-fsa.go.jp/api/v2/documents/{doc.get('docID')}"
                get_params = {"type": "1", "Subscription-Key": API_KEY}
                res_doc = requests.get(get_url, params=get_params)

                # 取得に成功（Content-Typeがバイナリ）したら保存[cite: 1]
                if res_doc.headers.get("Content-Type") == "application/octet-stream":
                    with open(file_path, "wb") as f:
                        f.write(res_doc.content)
                        print(f"  --> 保存完了: {doc.get('docID')}.zip")
                        time.sleep(1) # サーバーへの負荷軽減[cite: 1]

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    # 重要：サーバーに負荷をかけないよう、次のリクエストまで少し待つ
    time.sleep(1)     
    #1日進める
    current_date += timedelta(days=1)
