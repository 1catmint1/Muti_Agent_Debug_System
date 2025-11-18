import os
import sys
import subprocess

def run(cmd):
    result = subprocess.run(cmd, shell=True, check=True)
    if result.returncode != 0:
        print(f"❌ 命令执行失败: {cmd}")
        sys.exit(1)

print("🚀 开始打包智慧拼图游戏...")

# 检查 pyinstaller
try:
    import PyInstaller
except ImportError:
    print("📦 未安装 PyInstaller，正在安装...")
    run(f"{sys.executable} -m pip install pyinstaller")

# 清理
print("🧹 清理旧文件...")
subprocess.run("rmdir /s /q dist build *.spec >nul 2>&1", shell=True)

# 构建命令
build_cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--windowed',
    '--add-data', 'assets;assets',
    '--name', '智慧拼图',
    'main.py'
]

if os.path.exists('icon.ico'):
    build_cmd.extend(['--icon', 'icon.ico'])

print("📦 正在打包...")
print("运行命令:", ' '.join(build_cmd))
subprocess.call(build_cmd)