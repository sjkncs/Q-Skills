"""
C Drive Scanner - Analyzes disk space usage and categorizes large items.
Outputs a structured report of space consumers, distinguishing movable
user data from system/software/environment files.
"""
import os
import ctypes
import json

def get_drive_info(drive):
    """Get total and free space for a drive."""
    free = ctypes.c_ulonglong(0)
    total = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, None, ctypes.pointer(total), ctypes.pointer(free))
    return {
        'total_gb': round(total.value / (1024**3), 2),
        'free_gb': round(free.value / (1024**3), 2),
        'used_gb': round((total.value - free.value) / (1024**3), 2)
    }

def get_dir_size(path):
    """Calculate total size and file count of a directory."""
    total = 0
    count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
                count += 1
            except (OSError, PermissionError):
                pass
    return total, count

# Directories that are software/system/env config - DO NOT move
SKIP_DIRS = {
    'AppData', 'Application Data', 'Local Settings', 'Cookies',
    'PrintHood', 'SendTo', 'Templates', 'NetHood', 'Recent',
    'Start Menu', '.qoder', '.qoderwork', '.cursor', '.vscode',
    '.claude', '.codex', '.trae', '.cache', '.rustup', '.docker',
    '.m2', '.bun', '.codeium', '.dingclaw', '.Neo4jDesktop', '.real',
    '.npm', '.cargo', '.gradle', '.nuget', '.conda', '.ipython',
    '.jupyter', '.local', '.config', '.ssh', '.gnupg',
}

# Root-level system dirs
SYSTEM_ROOT = {
    '$Recycle.Bin', 'System Volume Information', 'Recovery',
    'Windows', 'Program Files', 'Program Files (x86)',
    'ProgramData', 'PerfLogs', 'Users', 'Documents and Settings',
}

def scan_user_profile(user_home):
    """Scan user profile subdirectories."""
    results = {'movable': [], 'keep': []}
    
    if not os.path.exists(user_home):
        return results
    
    for item in os.listdir(user_home):
        full = os.path.join(user_home, item)
        if not os.path.isdir(full):
            continue
        
        size, count = get_dir_size(full)
        size_mb = round(size / (1024 * 1024), 1)
        
        if size_mb < 100:
            continue
        
        entry = {
            'name': item,
            'path': full,
            'size_mb': size_mb,
            'file_count': count,
        }
        
        if item in SKIP_DIRS:
            entry['category'] = 'software/env'
            results['keep'].append(entry)
        else:
            entry['category'] = 'user_data'
            results['movable'].append(entry)
    
    results['movable'].sort(key=lambda x: x['size_mb'], reverse=True)
    results['keep'].sort(key=lambda x: x['size_mb'], reverse=True)
    return results

def scan_large_files(base_path, min_size_mb=50, max_results=50):
    """Find large files excluding system directories."""
    large_files = []
    min_bytes = min_size_mb * 1024 * 1024
    
    skip_patterns = ['\\Windows\\', '\\Program Files', '\\ProgramData\\',
                     '\\AppData\\', '\\.qoder\\', '\\.qoderwork\\']
    
    for root, dirs, files in os.walk(base_path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                size = os.path.getsize(fp)
                if size >= min_bytes:
                    if not any(p in fp for p in skip_patterns):
                        large_files.append({
                            'path': fp,
                            'size_mb': round(size / (1024 * 1024), 1)
                        })
            except (OSError, PermissionError):
                pass
    
    large_files.sort(key=lambda x: x['size_mb'], reverse=True)
    return large_files[:max_results]

def scan_desktop(desktop_path):
    """Detailed scan of Desktop subfolders and files."""
    results = {'folders': [], 'files': []}
    
    if not os.path.exists(desktop_path):
        return results
    
    for item in os.listdir(desktop_path):
        full = os.path.join(desktop_path, item)
        if os.path.isdir(full):
            size, count = get_dir_size(full)
            size_mb = round(size / (1024 * 1024), 1)
            if size_mb > 50:
                results['folders'].append({
                    'name': item, 'path': full,
                    'size_mb': size_mb, 'file_count': count
                })
        elif os.path.isfile(full):
            try:
                size = os.path.getsize(full)
                size_mb = round(size / (1024 * 1024), 1)
                if size_mb > 50:
                    results['files'].append({
                        'name': item, 'path': full, 'size_mb': size_mb
                    })
            except (OSError, PermissionError):
                pass
    
    results['folders'].sort(key=lambda x: x['size_mb'], reverse=True)
    results['files'].sort(key=lambda x: x['size_mb'], reverse=True)
    return results

def run_scan(user_home=None, target_drive='E:\\'):
    """Run full scan and return structured report."""
    if user_home is None:
        user_home = os.path.expanduser('~')
    
    report = {
        'c_drive': get_drive_info('C:\\'),
        'user_profile': scan_user_profile(user_home),
        'desktop': scan_desktop(os.path.join(user_home, 'Desktop')),
        'downloads': scan_desktop(os.path.join(user_home, 'Downloads')),
        'documents': scan_desktop(os.path.join(user_home, 'Documents')),
        'large_files': scan_large_files(user_home),
    }
    
    # Check target drive
    if os.path.exists(target_drive):
        report['target_drive'] = get_drive_info(target_drive)
    else:
        report['target_drive'] = None
    
    return report

def print_report(report):
    """Print human-readable report."""
    c = report['c_drive']
    print(f"===== C DRIVE: {c['used_gb']} GB used / {c['free_gb']} GB free =====\n")
    
    print("--- MOVABLE (user data) ---")
    for item in report['user_profile']['movable']:
        print(f"  {item['name']:<40} {item['size_mb']:>10.1f} MB")
    
    print("\n--- KEEP (software/env config) ---")
    for item in report['user_profile']['keep']:
        print(f"  {item['name']:<40} {item['size_mb']:>10.1f} MB")
    
    if report['desktop']['folders']:
        print("\n--- DESKTOP FOLDERS (>50MB) ---")
        for item in report['desktop']['folders']:
            print(f"  {item['name']:<40} {item['size_mb']:>10.1f} MB")
    
    if report['large_files']:
        print("\n--- TOP LARGE FILES ---")
        for item in report['large_files'][:20]:
            print(f"  {item['size_mb']:>10.1f} MB   {item['path']}")
    
    td = report.get('target_drive')
    if td:
        print(f"\n--- TARGET DRIVE: {td['free_gb']} GB free ---")
    else:
        print("\n--- TARGET DRIVE: NOT FOUND ---")

if __name__ == '__main__':
    report = run_scan()
    print_report(report)
    
    # Also save JSON for programmatic use
    json_path = os.path.join(os.path.dirname(__file__), 'scan_result.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nJSON saved to: {json_path}")
