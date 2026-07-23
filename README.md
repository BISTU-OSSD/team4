# 个人命令行记账小工具

> 5人小组 · 3天工期 · Python + CSV存储 · 适配课程开源协作全流程

## 功能清单
- ✅ 新增收支记录（金额/分类/日期/备注）
- ✅ 按日期/分类查询统计（总收入/总支出/结余）
- ✅ 月度预算设置与超支提醒（控制台弹窗）
- ✅ 统计结果导出为CSV报表
- ✅ 所有数据本地化存储（data/ledger.csv）

## 技术栈
- Python 3.8+（仅用内置库：csv, datetime, os）
- 数据存储：CSV文件（无需数据库）
- 协作平台：GitHub（Issues + PR + Release）

## 快速开始
```bash
# 1. 克隆仓库
git clone https://github.com/BISTU-OSSD/team4.git

# 2. 进入项目目录
cd team4

# 3. 生成测试数据
python seed_data.py

# 4. 启动程序
python main.py