---
name: check-meituan-progress
description: Monitor Meituan merchant review collection progress, run analysis and export after completion, and archive files. Use when the user asks about 美团采集进度, wants to check collection status, needs auto-monitoring, or wants to move files after completion.
---

# Check Meituan Collection Progress

## Overview

Monitor the 美团外卖商家版评论采集 pipeline. Supports both quick manual checks and long-running auto-monitoring that waits for completion, triggers analysis/export, and archives files.

## Key Paths (adjust date suffix if needed)

| Path | Purpose |
|------|---------|
| `C:\Python314\python.exe` | Python interpreter |
| `E:\美团外卖商家版每天评论采集\monitor_and_restart_meituan.py` | Monitor/restart script |
| `E:\美团外卖商家版每天评论采集\meituan_readonly_exports_20260610\checkpoint.json` | Checkpoint file |
| `E:\美团外卖商家版每天评论采集\session_analysis.py` | Analysis script |
| `E:\美团外卖商家版每天评论采集\export_analysis_excel.py` | Excel export script |
| `E:\美团外卖商家版每天评论采集\analysis_output\` | Output directory |

## Mode 1: Quick Manual Check

Use this when the user just wants to know the current status.

### Step 1: Run the monitor script

```bash
C:\Python314\python.exe "E:\美团外卖商家版每天评论采集\monitor_and_restart_meituan.py"
```

Capture stdout. Possible keywords:
- `Target reached` — stores >= 200, analysis/export triggered automatically.
- `Collection appears stalled` — checkpoint age > 10 min, auto-restart attempted.
- `Collection is active` — checkpoint updated recently, running normally.

### Step 2: Read checkpoint.json

Read `checkpoint.json` and extract:
- `len(processed_store_ids)` — current store count
- `total_sessions` — session count
- `total_messages` — message count
- `updated_at` — last update timestamp
- `last_store_name` — most recent store (optional)

### Step 3: Determine status

| Condition | Status | Action |
|-----------|--------|--------|
| stores >= 200 | **Complete** | Monitor already ran analysis + export; notify user with path to Excel output. |
| checkpoint age > 10 min | **Stalled** | Monitor already attempted restart; notify user a restart was triggered. |
| checkpoint age <= 10 min | **Active** | Normal progress; notify user current counts. |

## Mode 2: Auto-Monitor (Background Wait)

Use this when the user wants to leave it running and be notified when done.

### What it does

1. Polls `checkpoint.json` every 30 minutes
2. When stores >= 200, automatically runs:
   - `session_analysis.py`
   - `export_analysis_excel.py`
3. Then moves all input/output files to `E:\宋\美团采集结果`
4. Logs everything to `auto_monitor.log`

### How to run

```bash
C:\Python314\python.exe "E:\美团外卖商家版每天评论采集\auto_monitor_completion.py"
```

Or copy the latest version from the skill scripts folder:
```bash
cp "C:\Users\Administrator\.qoderwork\skills\check-meituan-progress\scripts\auto_monitor.py" "E:\美团外卖商家版每天评论采集\auto_monitor_completion.py"
```

Then run in the background:
```bash
C:\Python314\python.exe "E:\美团外卖商家版每天评论采集\auto_monitor_completion.py"
```

### Check progress while running

Read the log file:
```bash
type "E:\美团外卖商家版每天评论采集\auto_monitor.log"
```

### Expected log output

```
[2026-06-12 17:46:13] 美团采集自动监控脚本启动
[2026-06-12 17:46:13] 当前进度: stores=152/200, sessions=2953, msgs=1206
[2026-06-12 17:46:13] 还需采集 48 家，30分钟后再次检查...
```

## Mode 3: Post-Completion File Archive

After collection completes and analysis/export finish, move all files.

### Files to move

| Source | Destination |
|--------|-------------|
| `meituan_readonly_exports_20260610` | `E:\宋\美团采集结果` |
| `analysis_output` | `E:\宋\美团采集结果` |
| `export_analysis_excel.py` | `E:\宋\美团采集结果` |
| `export_charts_excel.py` | `E:\宋\美团采集结果` |
| `session_analysis.py` | `E:\宋\美团采集结果` |
| `meituan_readonly_cdp_collect.py` | `E:\宋\美团采集结果` |
| `monitor_and_restart_meituan.py` | `E:\宋\美团采集结果` |
| `meituan_readonly_exports_20260610_run.log` | `E:\宋\美团采集结果` |
| `meituan_manual_restart_20260611.log` | `E:\宋\美团采集结果` |
| `auto_monitor.log` | `E:\宋\美团采集结果` |
| `采集说明_20260526.md` | `E:\宋\美团采集结果` |

## Summary Report Format

When reporting to the user, provide:

```
**当前进度：** X / 200 家（XX%）
- Sessions：X
- Messages：X
- 最后更新：YYYY-MM-DD HH:MM:SS
- 采集状态：活跃/挂起/已完成

**处理结论：**
1. 是否触发 "Target reached"
2. 是否触发 "Collection appears stalled"
3. 后续操作建议
```

## Notes

- The monitor script auto-triggers analysis and Excel export when the target is reached.
- The monitor script auto-restarts the collection process if stalled (>10 min without checkpoint update).
- If the export directory date suffix changes (e.g., `20260610` -> `20260611`), update paths accordingly before running.
- The auto-monitor script can be stopped with Ctrl+C and resumed by re-running it (it reads the latest checkpoint state).
