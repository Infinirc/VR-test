import streamlit as st
import pandas as pd
import requests
from io import StringIO

def load_csv_from_github(url):
    """
    從 GitHub URL 加載 CSV 文件。
    """
    response = requests.get(url)
    if response.status_code == 200:
        csv_content = response.content.decode('utf-8')
        data = pd.read_csv(StringIO(csv_content))
        return data
    else:
        st.error("無法從 GitHub 加載數據。")
        return pd.DataFrame()

def calculate_operations_with_descriptions(worksheet_df, codebook_df):
    """
    計算每個 tid 的操作次數並關聯中文描述。
    """
    # 計算每個 tid 的操作次數
    operation_counts = worksheet_df['tid'].value_counts().reset_index()
    operation_counts.columns = ['tid', '操作次數']
    
    # 將操作次數與代號表中的中文描述關聯
    merged_df = pd.merge(operation_counts, codebook_df, left_on='tid', right_on='tid(命名規則 <單元>XX)', how='left')
    
    # 選擇需要顯示的列，這裡假設 '內容' 列包含中文描述
    result_df = merged_df[['tid', '操作次數', '內容']]
    return result_df

def main():
    st.title("學生每個 tid 的操作次數及描述")

    # 從 GitHub 加載代號表.csv
    github_csv_url = "https://raw.githubusercontent.com/Infinirc/VR-test/main/%E4%BB%A3%E8%99%9F%E8%A1%A8.csv"
    codebook_df = load_csv_from_github(github_csv_url)

    # 上傳工作表.csv
    uploaded_file = st.file_uploader("請上傳工作表.csv", type='csv')
    if uploaded_file is not None:
        worksheet_df = pd.read_csv(uploaded_file)
        
        # 計算每個 tid 的操作次數並獲取對應的中文描述
        operations_with_descriptions = calculate_operations_with_descriptions(worksheet_df, codebook_df)
        
        # 展示結果
        st.write("每個 tid 的操作次數及描述：", operations_with_descriptions)

if __name__ == "__main__":
    main()
