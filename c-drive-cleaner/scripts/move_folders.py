"""
C Drive Mover - Moves selected folders from C drive to target drive using robocopy.
Handles Chinese paths via Unicode, verifies move integrity, reports results.

Usage:
    python move_folders.py --config move_config.json
    python move_folders.py --interactive  (reads scan_result.json and prompts)
"""
import os
import sys
import json
import subprocess
import ctypes
import argparse

def get_drive_free(drive):
    """Get free space in bytes for a drive."""
    free = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, None, None, ctypes.pointer(free))
    return free.value

def get_dir_size(path):
    """Calculate total size of a directory."""
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

def move_folder(src, dest):
    """
    Move a folder using robocopy /E /MOVE.
    Returns (success, details_dict).
    """
    result = {
        'source': src,
        'destination': dest,
        'source_exists_before': os.path.exists(src),
    }
    
    if not os.path.exists(src):
        result['success'] = False
        result['error'] = 'Source not found'
        return result
    
    # Pre-move size
    src_size, src_count = get_dir_size(src)
    result['source_size_mb'] = round(src_size / (1024 * 1024), 1)
    result['source_file_count'] = src_count
    
    # Ensure destination parent exists
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    # Run robocopy
    cmd = ['robocopy', src, dest, '/E', '/MOVE', '/R:3', '/W:5',
           '/NP', '/NFL', '/NDL', '/NC', '/NS']
    
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    result['robocopy_exit_code'] = proc.returncode
    
    # Verify destination
    if os.path.exists(dest):
        dest_size, dest_count = get_dir_size(dest)
        result['dest_size_mb'] = round(dest_size / (1024 * 1024), 1)
        result['dest_file_count'] = dest_count
        result['size_verified'] = abs(src_size - dest_size) < 1024  # within 1KB tolerance
    else:
        result['dest_size_mb'] = 0
        result['dest_file_count'] = 0
        result['size_verified'] = False
    
    # Check source cleanup
    if os.path.exists(src):
        remaining, rem_count = get_dir_size(src)
        result['source_remaining_mb'] = round(remaining / (1024 * 1024), 1)
        result['source_remaining_files'] = rem_count
        
        if remaining == 0:
            # Try to remove empty directory tree
            for root, dirs, files in os.walk(src, topdown=False):
                for d in dirs:
                    try:
                        os.rmdir(os.path.join(root, d))
                    except OSError:
                        pass
            try:
                os.rmdir(src)
                result['source_removed'] = True
            except OSError:
                result['source_removed'] = False
        else:
            result['source_removed'] = False
    else:
        result['source_removed'] = True
        result['source_remaining_mb'] = 0
        result['source_remaining_files'] = 0
    
    result['success'] = (
        proc.returncode in (0, 1, 2, 3) and
        result.get('size_verified', False) and
        result.get('source_removed', False)
    )
    
    return result

def move_batch(items, target_base):
    """
    Move a batch of folders.
    items: list of {'src': path, 'name': display_name}
    target_base: destination base directory
    """
    os.makedirs(target_base, exist_ok=True)
    
    c_before = get_drive_free('C:\\')
    results = []
    
    for item in items:
        src = item['src']
        folder_name = os.path.basename(src)
        dest = os.path.join(target_base, folder_name)
        
        # Avoid name collision
        if os.path.exists(dest):
            i = 1
            while os.path.exists(dest + f'_{i}'):
                i += 1
            dest = dest + f'_{i}'
        
        print(f"Moving: {item.get('name', folder_name)}")
        print(f"  {src} -> {dest}")
        
        result = move_folder(src, dest)
        result['display_name'] = item.get('name', folder_name)
        results.append(result)
        
        status = 'OK' if result['success'] else 'PARTIAL' if result.get('size_verified') else 'FAILED'
        print(f"  [{status}] {result.get('source_size_mb', 0):.1f} MB")
        print()
    
    c_after = get_drive_free('C:\\')
    freed_mb = (c_after - c_before) / (1024 * 1024)
    
    summary = {
        'items': results,
        'total_moved_mb': sum(r.get('source_size_mb', 0) for r in results if r.get('size_verified')),
        'c_drive_freed_mb': round(freed_mb, 1),
        'c_drive_free_now_gb': round(c_after / (1024**3), 2),
        'all_success': all(r['success'] for r in results),
    }
    
    return summary

def interactive_mode(scan_json_path, target_base):
    """Read scan results and interactively select items to move."""
    with open(scan_json_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    movable = report['user_profile']['movable']
    if not movable:
        print("No movable items found.")
        return
    
    print("Movable items:")
    for i, item in enumerate(movable):
        print(f"  [{i}] {item['name']:<40} {item['size_mb']:>10.1f} MB")
    
    print(f"\n  [A] Move all")
    print(f"  [Q] Quit")
    
    choice = input("\nSelect (comma-separated indices, A, or Q): ").strip()
    
    if choice.upper() == 'Q':
        return
    elif choice.upper() == 'A':
        selected = movable
    else:
        indices = [int(x.strip()) for x in choice.split(',')]
        selected = [movable[i] for i in indices if 0 <= i < len(movable)]
    
    items = [{'src': item['path'], 'name': item['name']} for item in selected]
    summary = move_batch(items, target_base)
    
    print("=" * 50)
    print(f"Total moved: {summary['total_moved_mb']:.1f} MB")
    print(f"C drive freed: {summary['c_drive_freed_mb']:.1f} MB")
    print(f"C drive free now: {summary['c_drive_free_now_gb']:.2f} GB")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move folders from C drive')
    parser.add_argument('--config', help='JSON config file with items to move')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode using scan_result.json')
    parser.add_argument('--scan-json', default='scan_result.json', help='Path to scan result JSON')
    parser.add_argument('--target', default=None, help='Target base directory')
    args = parser.parse_args()
    
    if args.interactive:
        target = args.target or input("Target directory (e.g., E:\\backup): ").strip()
        interactive_mode(args.scan_json, target)
    elif args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        summary = move_batch(config['items'], config['target_base'])
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
