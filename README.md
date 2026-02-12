# SNJ 受発注検索システム

新日本海商事の受発注管理台帳をClaude Code on the Webで検索可能にするリポジトリ。

## セットアップ

```bash
pip install pandas openpyxl
```

## 使い方

### データ更新
1. 最新の `受発注管理台帳.xlsx` を `data/raw/` に配置
2. `python scripts/extract.py` を実行

### 検索
```bash
python scripts/search.py product "エゾシカ"     # 商品検索
python scripts/search.py case "日新堂"          # 案件検索
python scripts/search.py detail "2601-1001"     # 案件詳細
python scripts/search.py supplier "北見"         # 仕入先検索
python scripts/search.py credit "ホロニック"      # 与信確認
python scripts/search.py summary                # 全体サマリー
```

### Claude Code on the Webでの利用
自然言語で質問するだけでOK:
- 「ハッカ油の仕入価格を教えて」
- 「日新堂の案件一覧を見せて」
- 「水産カテゴリの商品を全部出して」
- 「与信残高を確認して」
