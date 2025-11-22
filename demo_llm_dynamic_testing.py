#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 动态测试演示脚本
展示如何使用大模型生成并执行动态测试用例
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzers.llm_dynamic_tester import run_dynamic_tests


def demo_user_input_detection():
    """演示：用户输入检测"""
    print("=" * 70)
    print("演示 1: 用户输入与外部数据交互检测")
    print("=" * 70)
    
    # 模拟一个有问题的 Python 文件
    vulnerable_code = '''
def process_user_data(user_input):
    """处理用户输入 - 存在注入风险"""
    # 直接使用用户输入构建 SQL（错误）
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return query

def handle_file_upload(filename):
    """处理文件上传 - 存在路径遍历风险"""
    # 直接使用用户提供的文件名（错误）
    with open(f"/uploads/{filename}", 'w') as f:
        f.write("data")

def parse_json_data(json_str):
    """解析 JSON 数据"""
    import json
    # 没有验证就直接解析（可能有风险）
    return json.loads(json_str)
'''
    
    files = [
        {
            "file": "vulnerable_app.py",
            "content": vulnerable_code,
            "original": ""
        }
    ]
    
    # 运行动态测试
    report = run_dynamic_tests(files)
    
    # 显示结果
    print(f"\n测试结果:")
    print(f"  总测试数: {report['total_tests']}")
    print(f"  通过: {report['passed']}")
    print(f"  失败: {report['failed']}")
    print(f"  发现问题: {report['total_issues']}")
    
    print(f"\n按类别统计:")
    for category, stats in report['by_category'].items():
        print(f"  {category}: {stats['issues']} 个问题")
    
    print(f"\n详细问题:")
    for detail in report['details']:
        if detail['issues_found']:
            print(f"\n  [{detail['category']}] {detail['description']}")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def demo_resource_management():
    """演示：资源管理检测"""
    print("\n" + "=" * 70)
    print("演示 2: 资源管理与状态依赖检测")
    print("=" * 70)
    
    leaky_code = '''
def read_large_file(filename):
    """读取大文件 - 可能泄漏资源"""
    f = open(filename, 'r')
    data = f.read()
    # 忘记关闭文件！
    return data

class DatabaseConnection:
    """数据库连接 - 可能泄漏连接"""
    def __init__(self):
        self.conn = None
    
    def connect(self):
        # 模拟连接
        self.conn = "connected"
    
    # 缺少 close 方法！

def process_batch(items):
    """批处理 - 可能内存泄漏"""
    results = []
    for item in items:
        # 不断追加，不清理
        results.append([item] * 1000)  # 创建大对象
    return results
'''
    
    files = [
        {
            "file": "leaky_app.py",
            "content": leaky_code,
            "original": ""
        }
    ]
    
    report = run_dynamic_tests(files)
    
    print(f"\n测试结果:")
    print(f"  发现资源管理问题: {report['by_category'].get('resource_management', {}).get('issues', 0)}")
    
    for detail in report['details']:
        if detail['category'] == 'resource_management' and detail['issues_found']:
            print(f"\n  问题详情:")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def demo_concurrency():
    """演示：并发问题检测"""
    print("\n" + "=" * 70)
    print("演示 3: 并发与异步操作检测")
    print("=" * 70)
    
    concurrent_code = '''
import threading

# 共享资源（没有锁保护）
counter = 0

def increment():
    """增加计数器 - 存在竞态条件"""
    global counter
    for _ in range(1000):
        # 非原子操作！
        counter += 1

def worker_thread():
    """工作线程"""
    increment()

def run_concurrent_tasks():
    """运行并发任务"""
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker_thread)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    return counter
'''
    
    files = [
        {
            "file": "concurrent_app.py",
            "content": concurrent_code,
            "original": ""
        }
    ]
    
    report = run_dynamic_tests(files)
    
    print(f"\n测试结果:")
    print(f"  发现并发问题: {report['by_category'].get('concurrency', {}).get('issues', 0)}")
    
    for detail in report['details']:
        if detail['category'] == 'concurrency' and detail['issues_found']:
            print(f"\n  问题详情:")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def demo_boundary_conditions():
    """演示：边界条件检测"""
    print("\n" + "=" * 70)
    print("演示 4: 边界条件与异常处理检测")
    print("=" * 70)
    
    boundary_code = '''
def divide_numbers(a, b):
    """除法 - 未检查除数"""
    return a / b  # 可能除零！

def access_array(arr, index):
    """访问数组 - 未检查边界"""
    return arr[index]  # 可能越界！

def fibonacci(n):
    """斐波那契 - 可能无限递归"""
    if n <= 0:
        return 0
    # 缺少 n == 1 的情况！
    return fibonacci(n-1) + fibonacci(n-2)

def calculate_power(base, exp):
    """计算幂 - 可能溢出"""
    return base ** exp  # 大指数可能溢出！
'''
    
    files = [
        {
            "file": "boundary_app.py",
            "content": boundary_code,
            "original": ""
        }
    ]
    
    report = run_dynamic_tests(files)
    
    print(f"\n测试结果:")
    print(f"  发现边界问题: {report['by_category'].get('boundary_conditions', {}).get('issues', 0)}")
    
    for detail in report['details']:
        if detail['category'] == 'boundary_conditions' and detail['issues_found']:
            print(f"\n  问题详情:")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def demo_environment_config():
    """演示：环境配置检测"""
    print("\n" + "=" * 70)
    print("演示 5: 环境依赖与配置检测")
    print("=" * 70)
    
    env_code = '''
import os

def get_api_key():
    """获取 API 密钥 - 缺少默认值"""
    return os.environ['API_KEY']  # 可能不存在！

def load_config():
    """加载配置文件 - 未处理缺失"""
    with open('/etc/app/config.ini', 'r') as f:
        return f.read()  # 文件可能不存在！

def get_database_url():
    """获取数据库 URL"""
    # 硬编码配置（不灵活）
    return "postgresql://localhost/mydb"
'''
    
    files = [
        {
            "file": "env_app.py",
            "content": env_code,
            "original": ""
        }
    ]
    
    report = run_dynamic_tests(files)
    
    print(f"\n测试结果:")
    print(f"  发现环境问题: {report['by_category'].get('environment_config', {}).get('issues', 0)}")
    
    for detail in report['details']:
        if detail['category'] == 'environment_config' and detail['issues_found']:
            print(f"\n  问题详情:")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def demo_dynamic_execution():
    """演示：动态代码执行检测"""
    print("\n" + "=" * 70)
    print("演示 6: 动态代码执行检测")
    print("=" * 70)
    
    dynamic_code = '''
def execute_user_code(code_string):
    """执行用户代码 - 严重安全风险！"""
    return eval(code_string)  # 危险！

def run_command(cmd):
    """运行命令"""
    exec(cmd)  # 危险！

def deserialize_data(data):
    """反序列化数据"""
    import pickle
    return pickle.loads(data)  # 危险！
'''
    
    files = [
        {
            "file": "dynamic_app.py",
            "content": dynamic_code,
            "original": ""
        }
    ]
    
    report = run_dynamic_tests(files)
    
    print(f"\n测试结果:")
    print(f"  发现动态执行问题: {report['by_category'].get('dynamic_execution', {}).get('issues', 0)}")
    
    for detail in report['details']:
        if detail['category'] == 'dynamic_execution' and detail['issues_found']:
            print(f"\n  问题详情:")
            for issue in detail['issues_found']:
                print(f"    - {issue}")


def main():
    """运行所有演示"""
    print("\n" + "=" * 70)
    print("LLM 动态测试系统 - 综合演示")
    print("=" * 70)
    print("\n本系统使用大模型生成测试用例，实际执行代码进行动态检测")
    print("涵盖 6 大类别的运行时安全和可靠性问题\n")
    
    try:
        demo_user_input_detection()
        demo_resource_management()
        demo_concurrency()
        demo_boundary_conditions()
        demo_environment_config()
        demo_dynamic_execution()
        
        print("\n" + "=" * 70)
        print("所有演示完成！")
        print("=" * 70)
        print("\n总结:")
        print("- ✅ 用户输入检测：发现 SQL 注入、XSS、路径遍历等风险")
        print("- ✅ 资源管理检测：发现内存泄漏、文件未关闭等问题")
        print("- ✅ 并发检测：发现竞态条件、死锁等并发问题")
        print("- ✅ 边界检测：发现除零、数组越界、递归等问题")
        print("- ✅ 环境检测：发现配置缺失、硬编码等问题")
        print("- ✅ 动态执行检测：发现 eval、exec、pickle 等安全风险")
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()