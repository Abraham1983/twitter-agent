# Autonomous Monitoring and Self-Healing System

This system provides autonomous monitoring and self-healing capabilities for the Twitter Agent Pipeline, ensuring reliable operation and automatic recovery from common issues.

## Features

### 1. Pre-Posting Health Checks
- Runs comprehensive health checks 1 hour before scheduled posting times
- Verifies Twitter API connectivity
- Checks database connectivity
- Validates internet connectivity
- Ensures sufficient disk space
- Verifies scheduler service status

### 2. Post-Failure Recovery
- Automatically detects posting failures
- Identifies common failure types (rate limiting, authentication, etc.)
- Implements appropriate recovery strategies
- Notifies administrators of issues

### 3. Automated Fixing Routines
- Automatically attempts to fix common issues:
  - Twitter API connectivity problems
  - Database connection issues
  - Disk space problems
  - Scheduler service issues
- Implements rate limit backoff strategies
- Refreshes credentials when needed

### 4. Integration with Existing Scheduler
- Works alongside the existing scheduler system
- Provides additional monitoring and recovery capabilities
- Maintains compatibility with existing workflows

## System Architecture

```
Autonomous Monitoring System
├── Health Checks
│   ├── Twitter API Health Check
│   ├── Database Health Check
│   ├── Internet Connectivity Check
│   ├── Disk Space Check
│   └── Scheduler Status Check
├── Failure Detection
│   ├── Error Monitoring
│   ├── Log Analysis
│   └── Failure Classification
├── Recovery Mechanisms
│   ├── Automatic Fixes
│   ├── Rate Limit Backoff
│   ├── Credential Refresh
│   └── Service Restart
└── Notification System
    ├── Health Status Reports
    ├── Failure Alerts
    └── Recovery Notifications
```

## Scheduled Tasks

The autonomous monitoring system automatically runs these tasks:

- **8:00 AM & 2:00 PM**: Pre-posting health checks (1 hour before content posting)
- **Every 30 minutes**: Posting pipeline monitoring
- **As needed**: Failure detection and recovery

## Setup

1. **Make the setup script executable**:
   ```bash
   chmod +x setup_autonomous_monitor.sh
   ```

2. **Run the setup script** (requires sudo):
   ```bash
   sudo ./setup_autonomous_monitor.sh
   ```

## Service Management

### Start the service:
```bash
sudo systemctl start autonomiq-autonomous-monitor.service
```

### Stop the service:
```bash
sudo systemctl stop autonomiq-autonomous-monitor.service
```

### Check service status:
```bash
sudo systemctl status autonomiq-autonomous-monitor.service
```

### View service logs:
```bash
journalctl -u autonomiq-autonomous-monitor.service -f
```

## Manual Usage

To run the autonomous monitor manually:
```bash
python autonomous_monitor.py
```

## Configuration

The system uses the same configuration as the main Twitter Agent Pipeline:
- Twitter API credentials in `.env` file
- Database configuration in `utils/database.py`
- Logging configuration in `autonomous_monitor.py`

## Logging

The system maintains detailed logs in the `logs/` directory:
- `autonomous_monitor.log`: Main system logs
- `post_failures.log`: Detailed failure logs

## Extending the System

To add new health checks or recovery mechanisms:

1. Add new methods to the `AutonomousMonitor` class in `autonomous_monitor.py`
2. Update the `run_health_checks()` method to include new checks
3. Add new fixing routines to the `attempt_automatic_fixes()` method
4. Update the scheduling as needed in the `start_monitoring()` method