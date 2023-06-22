# CSV Converter

## 概要
このプログラムは、CSVファイルのカラムの順序を別のCSVファイル(map.csv)に基づいて変換します。
このプログラムはPython 3で動作します。

## 構成
このプログラムは、以下のフォルダ構造となっています。

```
csv_converter
├── input (変換したいCSVファイルを格納)
├── output (変換後のCSVファイルを出力)
├── csv_converter.py (プログラムファイル)
├── csv_converter.bat (実行用バッチ)
├── map.csv (カラムの順序を指定する定義ファイル)
└── readme.md (本書)
```

## 使用方法
1. 'map.csv'を作成します。このCSVファイルでは、最初の行に新しいカラム名を、2行目には元のCSVの対応するカラムのインデックスを指定します。
変換後のcsvで値を空にしたいカラムは「NaN」を指定します。
以下はmap.csvの例です。

```csv
new_col_1,new_col_2,new_col_3,new_col_4,new_col_5
NaN,0,1,NaN,2
```

この例では、新しいCSVのnew_col_2に元のCSVの1番目のカラム、new_col_3に元のCSVの2番目のカラム、new_col_5に元のCSVの3番目のカラムを設定します。
new_col_1と、new_col_4は空白となります。

2. 変換したいCSVファイルをinputフォルダに配置します。
CSVファイルの文字エンコードは「utf-8」と「shift-jis」に対応しています。

3. csv_converter.bat を起動します。

4. プログラムが正常に終了すると、outputフォルダに変換されたCSVファイルが出力されます。
変換されたCSVファイルの文字エンコードは、読み込んだ元のファイルの文字エンコードを引き継ぎます。
※同名のファイルが存在する場合は上書きされます。

## 必要なライブラリ
このプロジェクトを実行するには以下のPythonライブラリが必要です：

* pandas
* logging
* os
