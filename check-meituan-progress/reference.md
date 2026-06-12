# Check Meituan Progress — Reference

## Auto-Monitor Script Configuration

The script `scripts/auto_monitor.py` is designed to run indefinitely in the background. It polls the checkpoint file and automatically handles completion.

### Configurable variables (edit in script)

| Variable | Default | Description |
|----------|---------|-------------|
| `SOURCE_DIR` | `E:\美团外卖商家版每天评论采集` | Root directory of the collection project |
| `CHECKPOINT` | `{SOURCE_DIR}\meituan_readonly_exports_20260610\checkpoint.json` | Path to checkpoint.json |
| `TARGET` | `200` | Target number of stores to collect |
| `PYTHON` | `C:\Python314\python.exe` | Python interpreter path |
| `DEST_DIR` | `E:\宋\美团采集结果` | Where to move files after completion |
| `LOG_FILE` | `{SOURCE_DIR}\auto_monitor.log` | Log file path |

### Items moved on completion

The script moves these items from `SOURCE_DIR` to `DEST_DIR`:

1. `meituan_readonly_exports_20260610` — collected raw data
2. `analysis_output` — analysis results
3. `export_analysis_excel.py` — Excel export script
4. `export_charts_excel.py` — chart export script
5. `session_analysis.py` — analysis script
6. `meituan_readonly_cdp_collect.py` — collection script
7. `monitor_and_restart_meituan.py` — monitor/restart script
8. `meituan_readonly_exports_20260610_run.log` — collection log
9. `meituan_manual_restart_20260611.log` — manual restart log
10. `auto_monitor.log` — this monitor's log
11. `采集说明_20260526.md` — project documentation

### Running on Windows

**Foreground (for testing):**
```cmd
C:\Python314\python.exe E:\美团外卖商家版每天评论采集\auto_monitor_completion.py
```

**Background (using pythonw to hide console):**
```cmd
C:\Python314\pythonw.exe E:\美团外卖商家版每天评论采集\auto_monitor_completion.py
```

**As a scheduled task:**
Use Windows Task Scheduler to run the script on system startup.

### Stopping the monitor

- If running in foreground: press `Ctrl+C`
- If running in background: find and terminate the python.exe process

### Resuming after interruption

Simply re-run the script. It will read the latest checkpoint state and continue monitoring from the current progress.

### Log rotation

The log file (`auto_monitor.log`) appends indefinitely. For long-running deployments, consider periodically archiving or truncating it.
