import csv
import os
from datetime import datetime
import m2
import m4
import statistics

DATA_DIR = "data"
LEDGER_FILE = os.path.join(DATA_DIR, "ledger.csv")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.txt")

# 初始化数据目录和文件
def init():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["日期", "类别", "收入", "支出", "备注"]) 






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
            m2.add_record()
        elif choice == "2":
            statistics.main() 
        elif choice == "3":
            statistics.main() 
        elif choice == "4":
            m4.set_monthly_budget()       
        elif choice == "5":
            m4.export_records_detail()  
        elif choice == "6":
            break
        else:
            print("输入有误，请重试")

if __name__ == "__main__":
    main()