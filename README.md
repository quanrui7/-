# 微博词云分析系统

## 功能描述
本系统实现以下核心功能：
1. 微博数据爬取：自动登录微博并爬取指定话题的实时数据
2. 数据预处理：清洗数据、中文分词、词频统计
3. 词云生成：创建基于校徽轮廓的词云图
4. 可视化展示：显示并保存高质量词云图片

## 安装配置说明

### 系统要求
- Python 3.7+
- macOS / Windows / Linux

### 安装步骤
1. 安装依赖：
- pip install -r requirements.txt
2. 准备资源文件：
- 确保 校徽.png 在项目根目录
- 确保 SourceHanSansSC-Regular.otf 在项目根目录

### 配置说明
1. 获取微博Cookie：
- 登录微博网页版
- 按F12打开开发者工具 → Network选项卡
- 刷新页面 → 复制任意请求的Cookie值
2. 编辑 main.py：
- 在以下位置粘贴你的Cookie：RAW_COOKIE = "在此粘贴你的Cookie"

## 输入/输出格式
### 输入
- 微博Cookie（身份验证）
- 搜索关键词（代码中默认为"西安交通大学"）
- 爬取页数（代码中默认为50页）
### 输出
- 控制台实时爬取进度
- 词云图文件：xi_an_jiaotong_wordcloud.jpg
- 统计信息：爬取页数、收集词汇量

## 截图
- 图1
<img width="602" alt="截屏2025-06-27 02 13 05" src="https://github.com/user-attachments/assets/c19fa3ae-9f73-4249-bc16-9df7c0c8c67b" />

- 图2
<img width="680" alt="截屏2025-06-27 17 51 46" src="https://github.com/user-attachments/assets/f9c794b0-e1da-4b3f-916d-c75f311053d3" />


## requirements.txt
- requests==2.31.0
- parsel==1.8.1
- jieba==0.42.1
- wordcloud==1.9.3
- pillow==10.2.0
- numpy==1.26.4
- matplotlib==3.8.3
