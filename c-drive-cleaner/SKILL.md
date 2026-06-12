---
name: c-drive-cleaner
description: Analyze and clean Windows C drive space. Scan for large files and folders, categorize them (movable user data vs system/software/env config), present a cleanup plan, and move selected items to another drive using robocopy. Use when user mentions cleaning C drive, low disk space, disk cleanup, moving large files to another drive, or freeing up space on system drive.
---

# C Drive Cleaner

A systematic workflow for analyzing Windows C drive space usage and safely moving large user files to another drive, while preserving all software, registry, and environment configuration files.

## Workflow Overview

```
Scan -> Categorize -> Present -> Confirm -> Move -> Verify
```

## Step 1: Scan C Drive

Run `scripts/scan_drive.py` to collect space usage data:

```bash
python scripts/scan_drive.py
```

The script produces:
- User profile subfolder sizes (>100MB)
- C drive root folder sizes
- Top 50 large files (>50MB, excluding system dirs)
- Desktop/Downloads/Documents detailed breakdown
- System reference sizes (AppData, Temp, ProgramData, pagefile, hiberfil)
- Target drive availability check

**Important**: All PowerShell/Python scripts must be written to files first (not inline) to avoid `$_` variable and Chinese encoding issues in bash.

## Step 2: Categorize Results

Classify every large item into one of two categories:

### Movable (user data, project files, media)
- Desktop project folders
- Downloads (installers, archives, data files)
- Documents (non-software: reports, data, crash dumps)
- WeChat/messaging file caches (`xwechat_files`)
- User-created content folders

### Do NOT Move (software/registry/env config)
- `AppData\*` (all software data, caches, configs)
- `ProgramData` (system-wide software data)
- `Program Files`, `Program Files (x86)` (installed programs)
- `Windows\*` (OS files)
- `pagefile.sys`, `hiberfil.sys`, `swapfile.sys` (system files)
- `$Recycle.Bin` (suggest emptying instead)
- Dot-tool directories: `.rustup`, `.docker`, `.m2`, `.bun`, `.npm`, `.cache`, `.cargo` (package managers/runtimes)
- IDE/tool directories: `.cursor`, `.vscode`, `.qoder`, `.qoderwork`, `.claude`, `.codex`, `.trae` (development tools)
- Software-specific: `.Neo4jDesktop`, `.real`, `.codeium`, `.dingclaw` etc.
- `Python*`, `node_modules`, `venv` at root level (runtime environments)

When in doubt, ask the user. Present the categorized list using a table format:

```markdown
| Location | Size | Category |
|----------|------|----------|
| Desktop\project | 8.9 GB | Movable |
| AppData\Local\Cursor | 2.0 GB | Software - Keep |
```

## Step 3: Present & Confirm

Use `AskUserQuestion` to let the user select which movable items to transfer. Options:
- All movable items
- Only specific categories (Desktop, Downloads, etc.)
- Item-by-item selection (multiSelect)

Always confirm:
- Source paths
- Destination path (e.g., `E:\target_folder`)
- Estimated total size

## Step 4: Move Files

Use `scripts/move_folders.py` or robocopy directly:

```bash
python scripts/move_folders.py
```

**Why robocopy, not shutil.move**:
- `shutil.move` uses `os.rename` which fails across drives (OSError 17)
- Falls back to copy+delete, but delete can fail on locked files (PermissionError 5)
- `robocopy /E /MOVE` handles cross-drive moves, retries on locked files, and is the Windows-native reliable approach

Robocopy command pattern:
```
robocopy "source" "dest" /E /MOVE /R:3 /W:5 /NP /NFL /NDL /NC /NS
```

Flags: `/E` = include subdirs, `/MOVE` = delete source after copy, `/R:3` = 3 retries, `/W:5` = 5s wait, `/NP /NFL /NDL /NC /NS` = minimal output.

Exit codes: 0=no files, 1=files copied, 2=extra files in dest, 3=both, 8+=errors.

**Encoding tip**: Always use Python scripts (not inline PowerShell) when paths contain Chinese characters. Use Unicode escapes for Chinese folder names:
```python
target = '\u5b8b\u7684\u6587\u4ef6\u593a'  # 宋的文件夹
```

## Step 5: Verify

After each move, verify:
1. Destination exists and file count/size matches source
2. Source has been removed from C drive
3. Check new C drive free space: `ctypes.windll.kernel32.GetDiskFreeSpaceExW`

Report final summary table and C drive before/after comparison.

## Quick Space Wins (suggest to user)

If more space is needed after moving user files, suggest:
- Empty Recycle Bin (`$Recycle.Bin`)
- Clean `%TEMP%` and `C:\Windows\Temp`
- Run Disk Cleanup (`cleanmgr`)
- Disable hibernation if not needed: `powercfg /h off` (frees hiberfil.sys)
- Reduce pagefile size if RAM is sufficient
