#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美团采集自动监控脚本
功能：定期检查采集进度，完成后自动运行分析脚本、导出Excel，并将文件归档。
"""
import json, time, subprocess, shutil, os, sys
from datetime import datetime

# ============================ 配置区（按需修改） ============================
SOURCE_DIR = r'E:\美团外卖商家版每天评论采集'
CHECKPOINT = os.path.join(SOURCE_DIR, r'meituan_readonly_exports_20260610\checkpoint.json')
TARGET = 200
PYTHON = r'C:\Python314\python.exe'
DEST_DIR = r'E:\宋\美团采集结果'  # 完成后剪切到的目标目录
LOG_FILE = os.path.join(SOURCE_DIR, 'auto_monitor.log')
# ===========================================================================

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def get_progress():
    with open(CHECKPOINT, 'r', encoding='utf-8') as f:
        d = json.load(f)
    stores = len(d.get('processed_store_ids', []))
    sessions = d.get('total_sessions', 0)
    msgs = d.get('total_messages', 0)
    return stores, sessions, msgs

def run_analysis_and_export():
    log("正在运行分析脚本 session_analysis.py...")
    r1 = subprocess.run(
        [PYTHON, os.path.join(SOURCE_DIR, 'session_analysis.py')],
        cwd=SOURCE_DIR, timeout=120, capture_output=True, text=True
    )
    log(f"session_analysis.py 返回码: {r1.returncode}")
    if r1.stdout:
        log(r1.stdout[:500])
    
    log("正在运行导出脚本 export_analysis_excel.py...")
    r2 = subprocess.run(
        [PYTHON, os.path.join(SOURCE_DIR, 'export_analysis_excel.py')],
        cwd=SOURCE_DIR, timeout=120, capture_output=True, text=True
    )
    log(f"export_analysis_excel.py 返回码: {r2.returncode}")
    if r2.stdout:
        log(r2.stdout[:500])

def move_files_to_song():
    log(f"正在将文件剪切到 {DEST_DIR}...")
    os.makedirs(DEST_DIR, exist_ok=True)
    
    items_to_move = [
        'meituan_readonly_exports_20260610',
        'analysis_output',
        'export_analysis_excel.py',
        'export_charts_excel.py',
        'session_analysis.py',
        'meituan_readonly_cdp_collect.py',
        'monitor_and_restart_meituan.py',
        'meituan_readonly_exports_20260610_run.log',
        'meituan_manual_restart_20260611.log',
        'auto_monitor.log',
        '采集说明_20260526.md',
    ]
    
    moved = []
    for item in items_to_move:
        src = os.path.join(SOURCE_DIR, item)
        dst = os.path.join(DEST_DIR, item)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                moved.append(item)
                log(f"  已移动: {item}")
            except Exception as e:
                log(f"  移动失败 {item}: {e}")
        else:
            log(f"  跳过（不存在）: {item}")
    
    log(f"共移动 {len(moved)} 项到 {DEST_DIR}")
    return moved

def main():
    log("=" * 60)
    log("美团采集自动监控脚本启动")
    log(f"目标: {TARGET} 家店铺 | 检查间隔: 30 分钟")
    log("=" * 60)
    
    while True:
        try:
            stores, sessions, msgs = get_progress()
            log(f"当前进度: stores={stores}/{TARGET}, sessions={sessions}, msgs={msgs}")
            
            if stores >= TARGET:
                log("✅ 采集目标已达成！正在执行后续操作...")
                run_analysis_and_export()
                move_files_to_song()
                log("🎉 所有任务已完成")
                log("=" * 60)
                break
            else:
                remaining = TARGET - stores
                log(f"还需采集 {remaining} 家，30分钟后再次检查...")
                time.sleep(1800)
                
        except Exception as e:
            log(f"❌ 监控过程中出现错误: {e}")
            log("10分钟后重试...")
            time.sleep(600)

if __name__ == '__main__':
    main()
