import csv
import random
from datetime import datetime, timedelta

def generate_sample_data():
    categories = ["餐饮", "交通", "娱乐", "购物", "工资"]
    types = ["支出", "收入"]
    os.makedirs("data", exist_ok=True)  # 确保data文件夹存在
    with open("data/ledger.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "type", "amount", "note"])
        for i in range(20):
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            category = random.choice(categories)
            type_ = "收入" if category == "工资" else random.choice(types)
            amount = round(random.uniform(10, 500), 2) if type_ == "支出" else round(random.uniform(1000, 8000), 2)
            note = f"测试数据{i+1}"
            writer.writerow([date, category, type_, amount, note])
    print("✅ 示例数据已生成到 data/ledger.csv")

if __name__ == "__main__":
    import os
    generate_sample_data()