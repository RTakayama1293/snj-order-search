#!/usr/bin/env python3
"""受発注管理台帳.xlsx → 検索用CSVに変換"""
import pandas as pd
import os, sys

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
XLSX = os.path.join(RAW_DIR, '受発注管理台帳.xlsx')

def clean_cols(df):
    df.columns = [str(c).replace('\n', '').strip() for c in df.columns]
    return df

def save(df, name):
    df.to_csv(f'{OUT_DIR}/{name}.csv', index=False, encoding='utf-8')
    print(f"{name}.csv: {len(df)} rows")

def extract_all():
    if not os.path.exists(XLSX):
        print(f"ERROR: {XLSX} not found"); sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    xls = pd.ExcelFile(XLSX)

    df = pd.read_excel(xls, sheet_name='仕入先マスタ', header=0)
    save(clean_cols(df), 'suppliers')

    df = pd.read_excel(xls, sheet_name='商品マスタ', header=1)
    save(clean_cols(df), 'products')

    df = pd.read_excel(xls, sheet_name='案件番号採番', header=1)
    save(clean_cols(df), 'case_numbers')

    df = pd.read_excel(xls, sheet_name='顧客与信管理', header=1)
    save(clean_cols(df), 'credit')

    df = pd.read_excel(xls, sheet_name='案件明細', header=1)
    save(clean_cols(df), 'case_details')

    df = pd.read_excel(xls, sheet_name='案件追跡表', header=None, skiprows=2)
    df_main = df.iloc[:, :32]
    header = [str(c).replace('\n', '').strip() for c in df_main.iloc[0].fillna('')]
    df_main = df_main.iloc[1:]
    df_main.columns = header
    save(df_main, 'case_tracking')

    df = pd.read_excel(xls, sheet_name='入力ルール用シート', header=0)
    save(clean_cols(df), 'input_rules')

    print("\n✅ All CSVs generated")

if __name__ == '__main__':
    extract_all()
