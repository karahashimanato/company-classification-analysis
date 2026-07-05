from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def corporate_arithmetic(df:pd.DataFrame, tfidf_matrix, target_name:str, plus_name=None, minus_name=None, top_n=10):
    try:
        target_idx = df[df["company_name"] ==  target_name].index[0]
        vec = tfidf_matrix[target_idx].toarray()

        formula_str = target_name
        if minus_name:
            minus_idx = df[df["company_name"] == minus_name].index[0]
            vec = vec - tfidf_matrix[minus_idx].toarray()
            formula_str += f" - {minus_name}"

        if plus_name:
            plus_idx = df[df["company_name"] == plus_name].index[0]
            vec = vec + tfidf_matrix[plus_idx].toarray()
            formula_str += f" + {plus_name}"

        sim = cosine_similarity(vec, tfidf_matrix)

        sim_indices = sim[0].argsort()[::-1]

        print(f"--- 計算式: {formula_str} ---")
        count = 0
        for idx in sim_indices:
            name = df.iloc[idx]["company_name"]

            if name not in [target_name, minus_name, plus_name]:
                print(f"{count+1}位： {name}(類似度:{sim[0][idx]:.3f})")
                count += 1
            if count >= top_n:
                break
    except IndexError:
        print("指定された企業名がデータ内に見つかりませんでした。")

def concept_arithmetic(target_name: str, minus_concept: str, plus_concept: str, embeddings, test_df, model, top_n = 10):
    try:
        # 1. ターゲット企業の「行番号（整数）」を取得
        target_row_idx = test_df.index.get_loc(target_name)
        target_vec = embeddings[target_row_idx].reshape(1, -1)
        
        # 2. 引きたい概念をベクトル化
        minus_vec = model.encode([f"query: {minus_concept}"])
        plus_vec = model.encode([f"query: {plus_concept}"])
        
        # 3. ベクトル演算
        result_vec = target_vec - (minus_vec * 0.8) + (plus_vec * 0.8)
        
        # 4. 全企業との類似度を計算
        sims = cosine_similarity(result_vec, embeddings)[0]
        
        # 5. 結果表示用のDataFrameを作成
        df_res = test_df.copy()
        df_res['calc_score'] = sims
        
        # 自分以外の企業をスコア順にソートして返す
        return df_res[df_res.index != target_name].sort_values('calc_score', ascending=False).head(top_n)

    except KeyError:
        print(f"指定された企業名『{target_name}』がデータ内に見つかりませんでした。")
        return None

def quick_search(query_text, model, embeddings, df, top_n=10):
    # E5モデルのルール通り "query: " を付与してベクトル化
    query_vec = model.encode([f"query: {query_text}"])
    
    # コサイン類似度を計算
    sims = cosine_similarity(query_vec, embeddings)[0]
    
    # 結果格納用のデータフレームを作成
    # 元のdfのインデックス（企業名）を引き継ぎます
    df_result = pd.DataFrame(index=df.index)
    df_result['score'] = sims
    
    # スコアの高い順にソートして返す
    return df_result.sort_values('score', ascending=False).head(top_n)