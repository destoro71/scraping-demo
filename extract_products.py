import pandas as pd
from bs4 import BeautifulSoup
import os

def main():
    # 入力ファイルと出力ファイルの名前
    input_file = 'test_products.html'
    output_file = 'products.csv'

    print(f"処理を開始します: {input_file} を読み込み中...")

    try:
        # 入力ファイルが存在するか確認
        if not os.path.exists(input_file):
            print(f"エラー: ファイル '{input_file}' が現在のフォルダに見つかりません。")
            return

        # 1. HTMLファイルを読み込む
        # 日本語が含まれる可能性があるため encoding='utf-8' を指定
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 2. BeautifulSoupを使ってHTML構造を解析
        soup = BeautifulSoup(html_content, 'html.parser')

        # 抽出したデータを格納するリスト
        data_list = []

        # 3. 商品情報の抽出
        # 一般的な構造として class="product" を持つ要素を探します。
        # HTMLの構造が異なる場合は、この 'div' や class_='product' の部分を修正してください。
        products = soup.find_all('div', class_='product')
        
        # もし div.product が見つからない場合、もう少し広めに探してみる（例: liタグなど）
        if not products:
             products = soup.find_all(class_='product')

        for product in products:
            # 商品名の取得
            # <h2>, <h3> などの見出しタグ、または class="name" / class="title" を持つ要素を探す
            name_tag = product.find(['h2', 'h3', 'h4', 'div', 'p'], class_=['name', 'title', 'product-name'])
            # クラス名指定で見つからない場合は、単に最初に見つかった見出しタグを採用する
            if not name_tag:
                 name_tag = product.find(['h2', 'h3', 'h4'])
            
            # テキストを抽出（タグが見つからない場合は '不明' とする）
            name = name_tag.get_text(strip=True) if name_tag else '不明'

            # 価格の取得
            # class="price", "cost" などを持つ要素を探す
            price_tag = product.find(['span', 'div', 'p'], class_=['price', 'cost', 'amount'])
            
            # テキストを抽出
            price = price_tag.get_text(strip=True) if price_tag else '不明'

            # リストに追加
            data_list.append({
                '商品名': name,
                '価格': price
            })

        # データが見つからなかった場合のメッセージ
        if not data_list:
            print("警告: 商品データが見つかりませんでした。HTMLのクラス名(product, price等)が正しいか確認してください。")

        # 4. pandasを使ってCSVに出力
        df = pd.DataFrame(data_list)
        
        # CSVファイルとして保存
        # encoding='utf-8-sig' にすることでExcelで開いた際の文字化けを防ぐ
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        # 完了メッセージ（要件通り）
        print("完了しました。products.csvを作成しました。")

    except FileNotFoundError:
        print("エラー: ファイルが見つかりませんでした。")
    except Exception as e:
        # その他の予期せぬエラーを捕捉
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
