import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ---------- 配置区 ----------
CSV_FILE = "bill.csv"                # CSV 文件名
DATE_COL = "日期"                    # 日期列名
CATEGORY_COL = "类别"                # 类别列名
INCOME_COL = "收入"                  # 收入列名
EXPENSE_COL = "支出"                 # 支出列名
# 如果你的 CSV 只用一列金额，请将 INCOME_COL 和 EXPENSE_COL 设为同一列名，
# 并额外增加一个“类型”列来区分，或者用正负号。下面代码按“收入”和“支出”两列设计。
# -----------------------------

def load_bills(filename: str) -> List[Dict]:
    """从 CSV 文件加载账单数据，自动处理日期解析"""
    bills = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 将日期字符串转为 datetime 对象，便于比较
            try:
                row['_date_obj'] = datetime.strptime(row[DATE_COL], '%Y-%m-%d')
            except ValueError:
                # 如果日期格式不同，可以修改格式化字符串，或跳过
                print(f"警告：日期格式错误，跳过记录 {row}")
                continue
            # 转换金额为 float，若为空则视为 0
            income = float(row.get(INCOME_COL, 0) or 0)
            expense = float(row.get(EXPENSE_COL, 0) or 0)
            row['_income'] = income
            row['_expense'] = expense
            bills.append(row)
    return bills

def filter_bills(bills: List[Dict],
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 category: Optional[str] = None) -> List[Dict]:
    """
    按日期范围和类别筛选账单
    - start_date/end_date: 格式 'YYYY-MM-DD'
    - category: 类别名称（精确匹配）
    """
    filtered = bills
    # 日期筛选
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        filtered = [b for b in filtered if b['_date_obj'] >= start]
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        filtered = [b for b in filtered if b['_date_obj'] <= end]
    # 类别筛选（不区分大小写）
    if category:
        filtered = [b for b in filtered if b[CATEGORY_COL].lower() == category.lower()]
    return filtered

def compute_statistics(bills: List[Dict]) -> Tuple[float, float, float]:
    """计算总收入、总支出、结余"""
    total_income = sum(b['_income'] for b in bills)
    total_expense = sum(b['_expense'] for b in bills)
    balance = total_income - total_expense
    return total_income, total_expense, balance

def print_table(bills: List[Dict], title: str = "账单明细"):
    """以表格形式打印筛选后的账单（使用简单对齐）"""
    if not bills:
        print("没有符合条件的记录。")
        return

    # 表头
    headers = ["日期", "类别", "收入", "支出", "备注"]
    # 计算每列最大宽度
    col_widths = [len(h) for h in headers]
    for b in bills:
        # 取各字段的字符串长度
        row_vals = [
            b[DATE_COL],
            b[CATEGORY_COL],
            f"{b['_income']:.2f}" if b['_income'] else "",
            f"{b['_expense']:.2f}" if b['_expense'] else "",
            b.get("备注", "")
        ]
        for i, val in enumerate(row_vals):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # 打印分隔线
    def print_line():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")

    # 打印标题
    print(f"\n{'='*20} {title} {'='*20}")

    # 打印表头
    print_line()
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    print(header_line)
    print_line()

    # 打印数据行
    for b in bills:
        row_vals = [
            b[DATE_COL],
            b[CATEGORY_COL],
            f"{b['_income']:.2f}" if b['_income'] else "",
            f"{b['_expense']:.2f}" if b['_expense'] else "",
            b.get("备注", "")
        ]
        row_line = "| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row_vals)) + " |"
        print(row_line)
    print_line()

def print_summary(total_income: float, total_expense: float, balance: float):
    """打印统计汇总"""
    print(f"\n{'='*20} 统计汇总 {'='*20}")
    print(f"总收入：{total_income:>10.2f}")
    print(f"总支出：{total_expense:>10.2f}")
    print(f"结余  ：{balance:>10.2f}")
    print("="*50)

# ---------- 主程序（交互式示例） ----------
def main():
    # 1. 加载数据
    try:
        bills = load_bills(CSV_FILE)
    except FileNotFoundError:
        print(f"错误：找不到文件 {CSV_FILE}，请确认文件存在。")
        return

    print(f"已加载 {len(bills)} 条账单记录。")

    # 2. 用户输入筛选条件（这里使用硬编码示例，你可以改为 input()）
    # 为了演示，我们设置一个筛选示例：2026-07-01 到 2026-07-10，只查看“餐饮”类别
    print("\n--- 筛选条件（示例）---")
    start = input("请输入起始日期 (YYYY-MM-DD，留空表示不限): ").strip() or None
    end = input("请输入结束日期 (YYYY-MM-DD，留空表示不限): ").strip() or None
    cat = input("请输入类别（留空表示不限）: ").strip() or None

    # 3. 执行筛选
    filtered = filter_bills(bills, start, end, cat)

    # 4. 打印明细
    print_table(filtered, title=f"筛选结果（共 {len(filtered)} 条）")

    # 5. 计算并打印统计
    total_income, total_expense, balance = compute_statistics(filtered)
    print_summary(total_income, total_expense, balance)

if __name__ == "__main__":
    main()
