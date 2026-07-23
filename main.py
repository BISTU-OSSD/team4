import csv
import os
from datetime import datetime

DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "ledger.csv")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.txt")

# 初始化数据目录和文件
def init():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "type", "amount", "note"])

# ========== 成员2 实现 ==========
def add_record():
    """录入收支记录"""
    # TODO: 输入金额、分类、日期、备注，写入CSV
    pass

# ========== 成员3 实现 ==========
def query_records():
    """按日期/分类筛选并打印"""
    # TODO: 筛选逻辑 + 表格打印
    pass

def statistics():
    """统计总收支和结余"""
    # TODO: 读取全部数据，计算汇总
    pass

# ========== 成员4 实现 ==========
def set_budget():
    """设置月度预算"""
    # TODO: 写入BUDGET_FILE
    pass

def check_budget():
    """检查是否超支，打印警告"""
    # TODO: 读取预算 + 本月支出累计
    pass

def export_report():
    """导出统计报表为CSV"""
    # TODO: 生成报表文件
    pass

# ========== 主菜单 ==========
def main():
    init()
    while True:
        print("\n===== 个人记账小工具 =====")
        print("1. 录入收支")
        print("2. 查询筛选")
        print("3. 查看统计")
        print("4. 设置预算")
        print("5. 导出报表")
        print("6. 退出")
        choice = input("请选择操作: ")
        if choice == "1":
            add_record()
        elif choice == "2":
            query_records()
        elif choice == "3":
            statistics()
        elif choice == "4":
            set_budget()
        elif choice == "5":
            export_report()
        elif choice == "6":
            break
        else:
            print("输入有误，请重试")

if __name__ == "__main__":
    main()