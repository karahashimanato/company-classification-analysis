import zipfile
import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import unicodedata
DATA_DIR = "../data/edinet_data"
OUTPUT_CSV = "edinet_analysis_data.csv"

def main():
    all_data = [] #全社のデータをためるリスト

    print("解析処理を開始しました...")
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".zip"):
            zip_path = os.path.join(DATA_DIR, filename)

            with zipfile.ZipFile(zip_path, 'r') as z:
                xbrl_files =  [f for f in z.namelist() if f.endswith(".xbrl") and "PublicDoc" in f]

                for xbrl_file in xbrl_files:
                    with z.open(xbrl_file) as f:
                        data_dict = analyze_content(f.read())
                        data_dict["filename"] = filename
                        all_data.append(data_dict)
                        print(f"解析完了: {data_dict['company_name']}")

    if all_data:
        df = pd.DataFrame(all_data)
        df = df[["company_name", "business_description", "business_risks", "filename"]]
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"\n すべてのデータを {OUTPUT_CSV} に保存")
    else:
        print("保存するデータが見つかりませんでした。")


def analyze_content(html_content):

    soup = BeautifulSoup(html_content, "lxml-xml")

    targets = {
        "company_name" : "CompanyNameCoverPage",
        "business_description" : "DescriptionOfBusinessTextBlock",
        "business_risks" : "BusinessRisksTextBlock"
    }
    res = {}
    for key, tag_suffix in targets.items():
        section = soup.find(lambda tag: tag.name.endswith(tag_suffix))
    
        if section:
            res[key] = clean_text(section.get_text())
        else:
            res[key] = None
    return res

    
def clean_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'<.*?>', '', text) # HTMLタグ除去
    
    # 【 】 や記号だけをスペースに変える（数字や文字は守る）
    text = re.sub(r'[【】※]', ' ', text)
    
    # 改行を消して、空白を1つにまとめる
    text = " ".join(text.split())
    return text.strip()

if __name__ == "__main__":
    main()
    
