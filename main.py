# -*- coding: utf-8 -*-
import requests as req
import parsel
import re
from wordcloud import WordCloud
from PIL import Image, ImageFont
import jieba
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

# 定义字典存储词频
word_freq = {}

def clean_cookie(cookie_str):
    """彻底清理 Cookie 字符串"""
    # 1. 移除所有换行符和缩进
    cookie_str = cookie_str.replace('\n', '').replace('\r', '').replace('\t', '')
    
    # 2. 移除开头和结尾的空白字符
    cookie_str = cookie_str.strip()
    
    # 3. 移除所有非 ASCII 字符
    cookie_str = re.sub(r'[^\x00-\x7F]', '', cookie_str)
    
    # 4. 移除 Cookie 值中的多余空格
    cookie_str = re.sub(r'\s+', ' ', cookie_str)
    
    return cookie_str

def get_weibo_data(url, params, headers):
    """爬取微博数据并提取内容"""
    try:
        response = req.get(url=url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        selector = parsel.Selector(response.text)
        
        # 检查是否被反爬
        if "security" in response.url or "验证" in response.text:
            print("触发反爬机制，请更新Cookie或稍后再试")
            return False
        
        cards = selector.css('.card-wrap')
        if not cards:
            print("未找到微博卡片，可能页面结构已变化")
            return False
        
        for card in cards:
            # 提取微博文本内容
            text_elements = card.css('.txt::text').getall()
            content = ''.join(text_elements).strip()
            
            if not content:
                continue
                
            # 提取点赞数
            like_count = card.css('.woo-like-count::text').get()
            hot = int(like_count) if like_count and like_count.isdigit() else 1
            
            # 分词并统计词频（带权重）
            words = jieba.lcut(content)
            for word in words:
                if len(word) > 1:  # 过滤单字
                    word_freq[word] = word_freq.get(word, 0) + hot
        
        return True
    
    except Exception as e:
        print(f"请求出错: {str(e)}")
        return False

def generate_wordcloud():
    """生成词云图"""
    if not word_freq:
        print("没有有效数据生成词云")
        return
    
    try:
        # 使用西交校徽作为蒙版
        mask = np.array(Image.open('校徽.png'))
        print("成功加载校徽图片作为蒙版")
    except Exception as e:
        print(f"校徽图片加载失败: {str(e)}，使用矩形词云")
        mask = None
    
    
    # 创建词云对象
    wc = WordCloud(
        font_path="SourceHanSansSC-Regular.otf",
        mask=mask,
        background_color='white',
        max_words=500,
        max_font_size=200,
        random_state=42,
        width=1200,
        height=800,
        collocations=False,
        contour_width=5,
        contour_color='steelblue'
    )
    
    # 生成词云
    try:
        wc.generate_from_frequencies(word_freq)
        print("词云生成成功")
    except Exception as e:
        print(f"词云生成失败: {str(e)}")
        return
    
    # 显示和保存词云
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    chinese_font = FontProperties(fname='SourceHanSansSC-Regular.otf', size=16)
    plt.title('西安交通大学微博话题词云', fontproperties=chinese_font)
    
    output_file = 'xi_an_jiaotong_wordcloud.jpg'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"词云已保存为: {output_file}")
    except Exception as e:
        print(f"保存词云失败: {str(e)}")
    
    plt.show()

if __name__ == '__main__':
    # ====== 粘贴新的微博Cookie ======
    RAW_COOKIE = "ALF=02_1753541002; SUB=_2A25FWSzaDeRhGeBL7lcT8yfJyziIHXVmFyASrDV8PUNbmtANLRjekW9NRuplu5rKzb7nECZYJ9Ka1uELB8uGlaD7; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5XWYCnSfmk9w1hjFkhIUYn5JpX5KzhUgL.FoqfSK-Ee0.fehB2dJLoI7Ux-rHDTHY_; WBPSESS=G38cFasltDxlmwrgTv_Ic9_NcDOoUrTt1ckAKsqdUMfyxqrsigkUKm1rEt7eAAXHOZ96YZtmElOZt2B2gUSHGstgvLGc8qmCpAmEiU4MEybZ0U8x3WKEcDHkgDbUwzUOH4_mDVOBfl-v9OdqReZzrg==; PC_TOKEN=83a8eabdcc; XSRF-TOKEN=Nm32NXFuhyYvt8OKGsz44JNM; SCF=AkdFAWn7HVUKBlHw0Z6YEUnIDLWcLteS_foKXgNVhjBybhLFhWdYaVLJ1Nx-UIqZKjVEIeNLKcCQ2NP3Jk3biAA."
    
    # 清理Cookie
    CLEANED_COOKIE = clean_cookie(RAW_COOKIE)
    print(f"清理后的Cookie长度: {len(CLEANED_COOKIE)} 字符")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Cookie': CLEANED_COOKIE,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://s.weibo.com/'
    }
    
    # 添加专业词典
    jieba.add_word("西安交通大学")
    jieba.add_word("西交大")
    jieba.add_word("创新港")
    jieba.add_word("兴庆校区")
    jieba.add_word("钱学森班")
    
    url = "https://s.weibo.com/realtime"
    
    # 爬取数据
    successful_pages = 0
    for page in range(1, 5):
        print(f"正在爬取第 {page} 页...", end='', flush=True)
        params = {
            "q": "西安交通大学",
            "rd": "realtime",
            "tw": "realtime",
            "Refer": "weibo_realtime",
            "page": page
        }
        
        if get_weibo_data(url, params, headers):
            successful_pages += 1
            print("成功")
        else:
            print("失败")
        
        # 随机延迟防止被封
        delay = random.uniform(2, 5)
        time.sleep(delay)
        
        # 每10页保存一次进度
        if page % 10 == 0:
            print(f"已爬取 {successful_pages}/{page} 页数据")
    
    print(f"爬取完成，成功获取 {successful_pages} 页数据")
    
    # 生成词云
    if word_freq:
        print("开始生成词云...")
        print(f"共收集 {len(word_freq)} 个词汇")
        generate_wordcloud()
    else:
        print("没有有效数据生成词云")
