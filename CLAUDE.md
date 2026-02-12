# 新日本海商事 受発注検索システム

## 概要
受発注管理台帳（Excel）から商品情報・案件情報・仕入先情報を検索するためのClaude Code環境。

## データ構造

### data/raw/
- `受発注管理台帳.xlsx` — 元ファイル（編集禁止）

### data/processed/ — 検索用CSV（`scripts/extract.py`で生成）
| ファイル | 内容 | 主キー | レコード数目安 |
|---------|------|--------|-------------|
| products.csv | 商品情報（価格・分類・特徴・JANコード等） | 商品連番 | ~1,100 |
| suppliers.csv | 仕入先の連絡先・支払条件 | 仕入先コード | ~90 |
| case_numbers.csv | 案件番号と顧客の紐付け | 案件番号 | ~150 |
| case_details.csv | 案件ごとの商品・価格・数量明細 | 案件番号+No | ~200 |
| case_tracking.csv | 案件の進捗ステータス（見積→受注→発注→出荷→入金） | 案件番号 | ~12 |
| credit.csv | 顧客の与信限度額・売掛残高 | 顧客名 | ~4 |
| input_rules.csv | 分類・担当者コード等のマスタ | - | ~24 |

## 検索の実行方法

### 基本: `scripts/search.py` を使う

```bash
# 商品検索（名前・特徴・仕入先で部分一致）
python scripts/search.py product "ハッカ"
python scripts/search.py product --supplier "北見ハッカ"
python scripts/search.py product --category "水産"

# 案件検索（案件番号・顧客名・商材で検索）
python scripts/search.py case "日新堂"
python scripts/search.py case "2601-1001"

# 仕入先検索
python scripts/search.py supplier "にんにく"

# 与信確認
python scripts/search.py credit "日新堂"

# 案件詳細
python scripts/search.py detail "2601-1001"

# 全体サマリー
python scripts/search.py summary
```

### 高度な分析: pandasで直接操作

```python
import pandas as pd
products = pd.read_csv('data/processed/products.csv')
cases = pd.read_csv('data/processed/case_details.csv')
```

## データ更新フロー

1. 新しいExcelを `data/raw/受発注管理台帳.xlsx` に上書き配置
2. `python scripts/extract.py` を実行 → processed/ のCSVが再生成される
3. `git add . && git commit -m "データ更新 YYYY-MM-DD" && git push`

## 案件番号の採番ルール
`YYMM-NNNN-担当コード支店コード`
- YY: 年2桁, MM: 月2桁
- NNNN: 月内連番（1001から）
- 担当コード: S=杉田, T=田嶋, H=蜂巣, A=永井, K=門永
- 支店コード: 01=大阪, 02=小樽

## 商品IDの採番ルール
`PRD_SNJ_[仕入先コード3文字]_[シリアル4桁]_[枝番2桁]`

## 注意事項
- CSVはUTF-8（BOMなし）
- 案件追跡表のガントチャート列（日付列）はCSV抽出対象外
- 帳票テンプレート（見積書・発注書・納品書・請求書）はExcel側で案件番号入力で自動生成されるため、CSVには含まない
- 金額計算はExcel側の数式に依存するため、CSV上の計算列は参考値
