import csv
import os
from datetime import datetime


# ===================== 通用工具函数 =====================
def read_records(file_path: str = "bill.csv") -> list:
    """读取账单记录，适配 日期,类别,收入,支出,备注 格式，数值判断避免0.00误判"""
    records = []
    if not os.path.exists(file_path):
        return records
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                "日期": row["日期"],
                "分类": row["类别"],
                "备注": row["备注"]
            }
            # 转成数值判断，兼容0、0.00、空值
            income_str = row["收入"].strip()
            expense_str = row["支出"].strip()
            income_val = float(income_str) if income_str else 0.0
            expense_val = float(expense_str) if expense_str else 0.0

            if income_val > 0:
                record["收支类型"] = "收入"
                record["金额"] = income_val
            elif expense_val > 0:
                record["收支类型"] = "支出"
                record["金额"] = expense_val
            else:
                continue  # 跳过无金额的无效行
            records.append(record)
    return records


def read_budget(file_path: str = "budget.csv") -> list:
    """读取所有月份的预算配置"""
    budget_list = []
    if not os.path.exists(file_path):
        return budget_list
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["预算金额"] = float(row["预算金额"])
            budget_list.append(row)
    return budget_list


def write_budget(budget_list: list, file_path: str = "budget.csv") -> None:
    """写入预算配置到文件，覆盖原有内容"""
    headers = ["年份", "月份", "预算金额"]
    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(budget_list)


# ===================== 月度预算提醒功能 =====================
def set_monthly_budget() -> None:
    """设置指定月份的预算，已有则覆盖"""
    try:
        year = int(input("请输入年份（如2026）："))
        month = int(input("请输入月份（1-12）："))
        amount = float(input("请输入月度预算金额："))

        if month < 1 or month > 12:
            print("❌ 输入无效，月份必须在1-12之间")
            return
        if amount <= 0:
            print("❌ 预算金额必须大于0")
            return

        budget_list = read_budget()
        updated = False
        for item in budget_list:
            if int(item["年份"]) == year and int(item["月份"]) == month:
                item["预算金额"] = amount
                updated = True
                break
        if not updated:
            budget_list.append({"年份": year, "月份": month, "预算金额": amount})

        write_budget(budget_list)
        print(f"✅ {year}年{month}月预算设置成功，金额：{amount:.2f} 元")

    except ValueError:
        print("❌ 输入格式错误，请输入有效数字")


def calc_monthly_expense(year: int, month: int) -> float:
    """计算指定月份的总支出"""
    records = read_records()
    total_expense = 0.0
    target_month = f"{year}-{month:02d}"

    for record in records:
        if record["收支类型"] == "支出" and record["日期"].startswith(target_month):
            total_expense += record["金额"]
    return total_expense


def check_budget_alert(year: int, month: int) -> None:
    """检查指定月份预算状态，超额则发出提醒"""
    budget_list = read_budget()
    budget_amount = None

    for item in budget_list:
        if int(item["年份"]) == year and int(item["月份"]) == month:
            budget_amount = item["预算金额"]
            break

    if budget_amount is None:
        print(f"ℹ️ 未查询到 {year}年{month}月的预算设置")
        return

    current_expense = calc_monthly_expense(year, month)
    remain = budget_amount - current_expense

    print(f"\n----- {year}年{month}月预算状态 -----")
    print(f"月度预算：{budget_amount:.2f} 元")
    print(f"已支出：{current_expense:.2f} 元")
    if remain >= 0:
        print(f"剩余预算：{remain:.2f} 元")
    else:
        print(f"⚠️ 已超出预算！超出金额：{abs(remain):.2f} 元")
    print("----------------------------------\n")


# ===================== CSV数据导出功能 =====================
def export_records_detail() -> None:
    """导出全部账单明细为CSV文件"""
    records = read_records()
    if not records:
        print("❌ 暂无账单数据，无法导出")
        return

    file_name = f"{datetime.now().strftime('%Y-%m')}_账单明细.csv"
    headers = ["日期", "收支类型", "分类", "金额", "备注"]

    with open(file_name, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"✅ 账单明细导出成功，文件已保存为：{file_name}")


def export_statistics_summary() -> None:
    """导出收支统计汇总（总收支+分类支出）为CSV文件"""
    records = read_records()
    if not records:
        print("❌ 暂无账单数据，无法导出")
        return

    total_income = 0.0
    total_expense = 0.0
    category_stat = {}

    for record in records:
        if record["收支类型"] == "收入":
            total_income += record["金额"]
        else:
            total_expense += record["金额"]
            cate = record["分类"]
            category_stat[cate] = category_stat.get(cate, 0) + record["金额"]

    balance = total_income - total_expense

    export_data = [
        {"项目": "总收入", "金额": round(total_income, 2)},
        {"项目": "总支出", "金额": round(total_expense, 2)},
        {"项目": "结余", "金额": round(balance, 2)},
        {"项目": "—— 分类支出明细 ——", "金额": ""},
    ]
    for cate, amount in category_stat.items():
        export_data.append({"项目": f"{cate}支出", "金额": round(amount, 2)})

    file_name = f"{datetime.now().strftime('%Y-%m')}_收支统计汇总.csv"
    headers = ["项目", "金额"]

    with open(file_name, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writehea