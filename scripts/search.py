#!/usr/bin/env python3
"""受発注管理台帳 検索CLI

Usage:
  python search.py product <keyword>           商品名・特徴・仕入先で検索
  python search.py product --supplier <name>   仕入先で絞り込み
  python search.py product --category <cat>    大分類で絞り込み
  python search.py product --id <product_id>   商品IDで完全一致検索
  python search.py case <keyword>              案件番号・顧客名・商材で検索
  python search.py detail <case_number>        案件明細の詳細表示
  python search.py supplier <keyword>          仕入先検索
  python search.py credit <keyword>            与信情報検索
  python search.py summary                     全体サマリー
"""
import pandas as pd
import sys, os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', 100)

def load(name):
    return pd.read_csv(os.path.join(DATA_DIR, f'{name}.csv'), encoding='utf-8', dtype=str)

def search_product(args):
    df = load('products')
    if '--id' in args:
        pid = args[args.index('--id') + 1]
        mask = df['商品連番'].str.contains(pid, case=False, na=False)
    elif '--supplier' in args:
        kw = args[args.index('--supplier') + 1]
        mask = df['仕入先'].str.contains(kw, case=False, na=False)
    elif '--category' in args:
        kw = args[args.index('--category') + 1]
        mask = df['大分類'].str.contains(kw, case=False, na=False)
    else:
        kw = ' '.join([a for a in args if not a.startswith('--')])
        if not kw: print("キーワードを指定してください"); return
        mask = pd.Series(False, index=df.index)
        for col in ['商品名', '商品特徴', '仕入先', '大分類', '小分類', '商品連番', 'JANコード']:
            if col in df.columns:
                mask = mask | df[col].str.contains(kw, case=False, na=False)

    results = df[mask]
    if results.empty: print("該当なし"); return

    display_cols = ['商品連番', '大分類', '小分類', '仕入先', '商品名', '単位', '容量',
                    '仕入単価', '国内定価（15％）', '海外定価（20％）', '温度帯', '賞味期限', 'EEZO掲載可否']
    existing = [c for c in display_cols if c in results.columns]
    print(f"\n商品検索結果: {len(results)}件\n")
    print(results[existing].to_string(index=False))

    if len(results) <= 5:
        for _, row in results.iterrows():
            print(f"\n--- {row.get('商品名', 'N/A')} ---")
            feat = row.get('商品特徴')
            if pd.notna(feat): print(f"  特徴: {feat}")
            note_col = [c for c in df.columns if '申し送り' in str(c)]
            if note_col and pd.notna(row.get(note_col[0])):
                print(f"  申し送り: {row[note_col[0]]}")

def search_case(args):
    df_track = load('case_tracking')
    df_detail = load('case_details')

    kw = ' '.join([a for a in args if not a.startswith('--')])
    if not kw: print("キーワードを指定してください"); return

    mask_track = pd.Series(False, index=df_track.index)
    for col in ['案件番号', '顧客名', '仕入先', '商材', '担当']:
        if col in df_track.columns:
            mask_track = mask_track | df_track[col].str.contains(kw, case=False, na=False)
    results = df_track[mask_track]
    if not results.empty:
        display_cols = ['案件番号', '顧客名', '仕入先', '商材', '担当', '支払い条件',
                        '見積', '受注', '発注', '出荷', '着荷', '売上計上', '売上入金']
        existing = [c for c in display_cols if c in results.columns]
        print(f"\n案件追跡: {len(results)}件\n")
        print(results[existing].to_string(index=False))

    mask_detail = pd.Series(False, index=df_detail.index)
    for col in ['案件番号', '顧客名', '仕入先', '商品名', '商品ID']:
        if col in df_detail.columns:
            mask_detail = mask_detail | df_detail[col].str.contains(kw, case=False, na=False)
    detail_results = df_detail[mask_detail]
    if not detail_results.empty:
        display_cols = ['案件番号', '顧客名', '商品ID', '仕入先', '商品名',
                        '仕入価格', '販売価格（売値）', '数量', '単位']
        existing = [c for c in display_cols if c in detail_results.columns]
        print(f"\n案件明細: {len(detail_results)}件\n")
        print(detail_results[existing].to_string(index=False))

    if results.empty and detail_results.empty: print("該当なし")

def search_case_detail(args):
    case_num = args[0] if args else ''
    if not case_num: print("案件番号を指定してください"); return

    df_track = load('case_tracking')
    df_detail = load('case_details')

    track = df_track[df_track['案件番号'].str.contains(case_num, case=False, na=False)]
    detail = df_detail[df_detail['案件番号'].str.contains(case_num, case=False, na=False)]

    if not track.empty:
        print(f"\n案件追跡情報:")
        for _, row in track.iterrows():
            print(f"  案件番号: {row.get('案件番号')}")
            print(f"  顧客: {row.get('顧客名')} / 仕入先: {row.get('仕入先')}")
            print(f"  商材: {row.get('商材')} / 担当: {row.get('担当')}")
            print(f"  支払条件: {row.get('支払い条件')}")
            print(f"  見積: {row.get('見積')} -> 受注: {row.get('受注')}")
            print(f"  発注: {row.get('発注')} -> 出荷: {row.get('出荷')} -> 着荷: {row.get('着荷')}")
            print(f"  売上計上: {row.get('売上計上')} / 売上入金: {row.get('売上入金')}")
            print()

    if not detail.empty:
        print(f"\n明細 ({len(detail)}行):")
        display_cols = ['No', '商品ID', '仕入先', '商品名', '仕入価格', '販売価格（売値）', '数量', '単位', '税率']
        existing = [c for c in display_cols if c in detail.columns]
        print(detail[existing].to_string(index=False))

    if track.empty and detail.empty: print(f"案件 '{case_num}' が見つかりません")

def search_supplier(args):
    df = load('suppliers')
    kw = ' '.join(args)
    if not kw: print(df.to_string(index=False)); return
    mask = pd.Series(False, index=df.index)
    for col in df.columns:
        mask = mask | df[col].str.contains(kw, case=False, na=False)
    results = df[mask]
    if results.empty: print("該当なし"); return
    print(f"\n仕入先検索結果: {len(results)}件\n")
    print(results.to_string(index=False))

def search_credit(args):
    df = load('credit')
    kw = ' '.join(args)
    if not kw: print(df.to_string(index=False)); return
    mask = df['顧客名'].str.contains(kw, case=False, na=False)
    results = df[mask]
    if results.empty: print("該当なし"); return
    print(f"\n与信情報:\n")
    for _, row in results.iterrows():
        print(f"  顧客名: {row.get('顧客名')}")
        print(f"  区分: {row.get('区分')} / 調査機関: {row.get('調査機関')} / 評点: {row.get('評点/格付')}")
        print(f"  与信限度額: {row.get('与信限度額')} / 現在売掛残高: {row.get('現在売掛残高')}")
        print(f"  残与信枠: {row.get('残与信枠')} / 支払条件: {row.get('支払条件')}")
        print()

def show_summary():
    files = {'products': '商品', 'suppliers': '仕入先', 'case_numbers': '案件',
             'case_details': '明細行', 'case_tracking': '追跡案件', 'credit': '与信顧客'}
    print("\nデータサマリー\n")
    for f, label in files.items():
        df = load(f)
        print(f"  {label}: {len(df)}件 ({f}.csv)")

    products = load('products')
    if '大分類' in products.columns:
        print(f"\n商品カテゴリ別:")
        for cat, count in products['大分類'].value_counts().items():
            print(f"  {cat}: {count}品")

    cases = load('case_numbers')
    if '担当者' in cases.columns:
        print(f"\n担当者別案件数:")
        for person, count in cases['担当者'].value_counts().items():
            if pd.notna(person): print(f"  {person}: {count}件")

def main():
    if len(sys.argv) < 2: print(__doc__); return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        'product': search_product, 'case': search_case,
        'detail': search_case_detail, 'supplier': search_supplier,
        'credit': search_credit, 'summary': lambda _: show_summary(),
    }
    if cmd in commands: commands[cmd](args)
    else: print(f"不明なコマンド: {cmd}\n"); print(__doc__)

if __name__ == '__main__':
    main()
