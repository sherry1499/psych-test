"""
运行自动化测试的脚本
用法：python run_tests.py
"""

import subprocess
import sys
import os

def main():
    # 切换到项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 50)
    print("心理测试项目 - 自动化测试")
    print("=" * 50)
    
    # 检查依赖
    print("\n[1/2] 检查并安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
    
    # 运行测试
    print("\n[2/2] 运行 Selenium 测试...")
    print("-" * 50)
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_psych.py", 
        "-v",                    # 详细输出
        "--tb=short",            # 简短的错误追踪
        "-x",                    # 遇到第一个失败就停止（可去掉）
    ])
    
    print("-" * 50)
    if result.returncode == 0:
        print("\n✓ 所有测试通过！")
    else:
        print(f"\n✗ 有测试失败，返回码: {result.returncode}")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
