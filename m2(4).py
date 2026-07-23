#成员二收支录入模块
import csv
import os
from datetime import datetime

# ---------- 配置 ----------
CSV_FILE = "data/ledger.csv"                # 与成员3保持一致
HEADERS = ["日期", "类别", "收入", "支出", "备注"]   # 列名完全匹配成员3读取的字段
# -------------------------


def add_record():
    """交互式添加一条收支记录"""
    print("\n=== 新增收支记录 ===")

    # 1. 日期（默认今天）
    while True:
        date_str = input("请输入日期 (YYYY-MM-DD，留空则使用今天): ").strip()
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
            break
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("日期格式错误，请重新输入！")

    # 2. 类别（预设常用类别）
    categories = ["餐饮", "交通", "娱乐", "购物", "其他"]
    print(f"可选类别: {', '.join(categories)}")
    while True:
        category = input("请输入类别: ").strip()
        if category:
            break
        print("类别不能为空！")

    # 3. 金额（正数校验）
    while True:
        amount_str = input("请输入金额 (正数): ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("金额必须为正数！")
                continue
            break
        except ValueError:
            print("金额必须是数字！")

    # 4. 类型（收入/支出）
    while True:
        type_input = input("请输入类型 (收入/支出): ").strip()
        if type_input in ["收入", "支出"]:
            break
        print("类型只能为 '收入' 或 '支出'！")

    # 5. 备注（可选）
    note = input("请输入备注 (可选): ").strip()

    # 6. 根据类型填充收入/支出列（只填其中一列，另一列置 0）
    income = amount if type_input == "收入" else 0
    expense = amount if type_input == "支出" else 0

    # 7. 追加写入 CSV
    with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, f"{income:.2f}", f"{expense:.2f}", note])

    print("✅ 记录添加成功！")

