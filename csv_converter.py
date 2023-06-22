import logging
import os
import pandas as pd


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("start")

    input_folder = 'input'
    output_folder = 'output'
    map_file = 'map.csv'

    # map_df は、元のデータフレームのカラムインデックスを値に持ち、
    # 新しいカラム名をラベルに持つことで、データの変換を指定するファイル
    map_df, _ = read_csv(map_file)

    # 変換対象となるcsvファイルの一覧
    csv_files = read_input_files(input_folder)

    for file_name in csv_files:
        # inputフォルダのcsv内容を読み取り、outputフォルダにcsvを生成する
        logging.info("converting : " + file_name)
        df, encoding = read_csv(os.path.join(input_folder, file_name))
        converted_df = convert_data(df, map_df)
        write_csv(output_folder, file_name, converted_df, encoding)
        logging.info("completed  : " + file_name)

    logging.info("finish")


def read_input_files(input_folder: str) -> list[str]:
    """
    inputフォルダ内の全てのCSVファイルを取得する
    """
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    return csv_files


def read_csv(file_path: str) -> tuple[pd.DataFrame, str]:
    """
    CSVファイルを読み取り、データフレーム型で取得する
    データはすべて文字列で取得する（"001"のような表記を数値として解釈することを防ぐため）
    """
    try:
        # ファイルを utf-8 で読み込みます
        encoding = 'utf-8'
        df = pd.read_csv(file_path, dtype=str, encoding=encoding)
    except UnicodeDecodeError:
        # utf-8 での読み込みに失敗した場合
        # ファイルを shift-jis で読み込みます
        encoding = 'shift-jis'
        df = pd.read_csv(file_path, dtype=str, encoding=encoding)

    return df, encoding


def convert_data(df: pd.DataFrame, map_df: pd.DataFrame) -> pd.DataFrame:
    """
    入力データフレーム(df)のカラム順序をmap_dfに基づいて変更します。

    map_dfでカラムのインデックスが指定されていない場所では、新しいデータフレームに空のカラムが作成されます。
    また、指定されたインデックスが元のデータフレームのカラム数を超えている場合はエラーが発生します。

    入力データフレームに対して変換を適用した後、新しいデータフレームを返します。
    """
    # 新しいカラムの順序を取得する
    new_columns = map_df.columns.tolist()
    new_order = []
    for val in map_df.iloc[0].tolist():
        if pd.isna(val):
            new_order.append(None)
        else:
            idx = int(val)
            if idx >= len(df.columns):
                raise ValueError(f"入力データフレームに存在しない列番号（{idx}）が map.csv に含まれています。")
            new_order.append(idx)

    # 新しいデータフレームを作成する
    converted_df = pd.DataFrame(columns=new_columns)

    # 新しいデータフレームに値を設定する
    for col_name, old_index in zip(new_columns, new_order):
        if old_index is None:
            # map.csvでカラムの番号が指定されていない場所に、空白を設定
            converted_df[col_name] = ""
        else:
            # 指定されたカラムに、対応するデータの列をコピーする
            converted_df[col_name] = df.iloc[:, old_index]

    return converted_df


def write_csv(output_folder: str, file_name: str, df: pd.DataFrame, encoding: str):
    """
    出力フォルダに新たなCSVファイルを書き出す
    """
    df.to_csv(os.path.join(output_folder, file_name), index = False, encoding=encoding)


if __name__ == "__main__":
    main()