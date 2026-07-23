import csv
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# ---------- 配置（与录入模块一致） ----------
CSV_FILE = "bill.csv"
HEADERS = ["日期", "类别", "收入", "支出", "备注"]
PRESET_CATEGORIES = ["餐饮", "交通", "娱乐", "购物", "工资", "医疗", "教育", "其他"]
# --------------------------------------------

def load_bills() -> List[Dict]:
    """加载所有账单，返回字典列表，日期转为datetime，金额转为float"""
    bills = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # 检查表头是否匹配
            if reader.fieldnames != HEADERS:
                print(f"⚠️ 文件表头不匹配，预期 {HEADERS}，实际 {reader.fieldnames}")
                print("   请确保第一行是表头，若没有请手动添加。")
                return []
            for row in reader:
                # 转换日期
                try:
                    row['_date_obj'] = datetime.strptime(row['日期'], '%Y-%m-%d')
                except (ValueError, KeyError):
                    print(f"⚠️ 跳过日期格式错误的行：{row}")
                    continue
                # 转换金额
                row['_income'] = float(row.get('收入', 0) or 0)
                row['_expense'] = float(row.get('支出', 0) or 0)
                bills.append(row)
    except FileNotFoundError:
        print(f"❌ 数据文件 {CSV_FILE} 不存在！请先录入数据。")
    return bills

def filter_bills(bills: List[Dict],
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 category: Optional[str] = None) -> List[Dict]:
    """按日期范围和类别筛选"""
    filtered = bills
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        filtered = [b for b in filtered if b['_date_obj'] >= start]
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        filtered = [b for b in filtered if b['_date_obj'] <= end]
    if category:
        filtered = [b for b in filtered if b['类别'].lower() == category.lower()]
    return filtered

def compute_statistics(bills: List[Dict]) -> Tuple[float, float, float]:
    total_income = sum(b['_income'] for b in bills)
    total_expense = sum(b['_expense'] for b in bills)
    balance = total_income - total_expense
    return total_income, total_expense, balance

def print_bills_table(bills: List[Dict], title: str = "账单明细"):
    """打印表格"""
    if not bills:
        print("\n📭 没有符合条件的记录。")
        return
    rows = []
    for b in bills:
        rows.append([
            b['日期'],
            b['类别'],
            f"{b['_income']:.2f}" if b['_income'] else "",
            f"{b['_expense']:.2f}" if b['_expense'] else "",
            b.get('备注', '')
        ])
    col_widths = [len(h) for h in HEADERS]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    print(f"\n{'='*20} {title} {'='*20}")
    def print_line():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    print_line()
    header_line = "| " + " | ".join(HEADERS[i].ljust(col_widths[i]) for i in range(len(HEADERS))) + " |"
    print(header_line)
    print_line()
    for row in rows:
        data_line = "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + " |"
        print(data_line)
    print_line()

def print_summary(total_income: float, total_expense: float, balance: float):
    print(f"\n{'='*20} 统计汇总 {'='*20}")
    print(f"💰 总收入：{total_income:>10.2f}")
    print(f"💸 总支出：{total_expense:>10.2f}")
    print(f"📊 结余  ：{balance:>10.2f}")
    print("="*55)

def get_date_input(prompt: str) -> Tuple[bool, Optional[str]]:
    """
    返回 (是否取消, 日期字符串或None)
    - 若用户输入 q，返回 (True, None) 表示取消整个查询
    - 若直接回车，返回 (False, None) 表示不限
    - 若输入有效日期，返回 (False, date_str)
    """
    val = input(prompt).strip()
    if val.lower() == 'q':
        return True, None
    if not val:
        return False, None
    try:
        datetime.strptime(val, '%Y-%m-%d')
        return False, val
    except ValueError:
        print("❌ 日期格式错误，请使用 YYYY-MM-DD。")
        return False, None

def main():
    print("\n========== 数据查询统计模块 ==========")
    bills = load_bills()
    if not bills:
        input("按回车键退出...")
        return

    print(f"📂 共加载 {len(bills)} 条记录。\n")

    # 获取筛选条件
    print("--- 设置筛选条件（回车表示不限，输入 q 取消查询） ---")
    cancel, start = get_date_input("起始日期 (YYYY-MM-DD): ")
    if cancel:
        print("已取消查询。")
        input("按回车键退出...")
        return

    cancel, end = get_date_input("结束日期 (YYYY-MM-DD): ")
    if cancel:
        print("已取消查询。")
        input("按回车键退出...")
        return

    # 选择类别
    print("\n筛选类别（留空表示不限）:")
    print("  0. 全部（不限）")
    for i, cat in enumerate(PRESET_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    print("  (也可直接输入自定义类别)")
    category = None
    while True:
        choice = input("请输入序号或类别名称: ").strip()
        if choice.lower() == 'q':
            print("已取消查询。")
            input("按回车键退出...")
            return
        if not choice:
            category = None
            break
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                category = None
                break
            if 1 <= idx <= len(PRESET_CATEGORIES):
                category = PRESET_CATEGORIES[idx - 1]
                break
            else:
                print(f"❌ 序号超出范围 (1~{len(PRESET_CATEGORIES)})")
                continue
        else:
            category = choice.strip()
            break

    # 执行筛选
    filtered = filter_bills(bills, start, end, category)

    # 生成标题
    title = f"筛选结果（共 {len(filtered)} 条）"
    if start and end:
        title += f" | {start} ~ {end}"
    elif start:
        title += f" | 从 {start} 起"
    elif end:
        title += f" | 至 {end} 止"
    if category:
        title += f" | 类别: {category}"

    # 打印明细和统计
    print_bills_table(filtered, title)
    total_income, total_expense, balance = compute_statistics(filtered)
    print_summary(total_income, total_expense, balance)

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
