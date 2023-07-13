Automation wrapper for passmark

Description:
         From website:  PassMark PerformanceTest™ for Linux allows you to objectively
         benchmark a Linux system using a variety of different speed tests and compare
         the results to others.

Location of underlying workload: https://www.passmark.com/products/pt_linux/index.php

Packages required: bc,numactl

To run:
```
[root@hawkeye ~]# git clone https://github.com/redhat-performance/passmark-wrapper
[root@hawkeye ~]# passmark-wrapper/passmark/passmark_run
```

The script will set the buffer sizes based on the hardware it is being executed on.

```
Options
--usage Usage:
  --cpu_add n: add n cpus each iteration until hit max cpus
  --powers_2: starting from 1 cpu, keep doubling the cpus until max cpus
General options
  --home_parent <value>: Our parent home directory.  If not set, defaults to current working directory.
  --host_config <value>: default is the current host name.
  --iterations <value>: Number of times to run the test, defaults to 1.
  --pbench: use pbench-user-benchmark and place information into pbench, defaults to do not use.
  --pbench_user <value>: user who started everything. Defaults to the current user.
  --pbench_copy: Copy the pbench data, not move it.
  --pbench_stats: What stats to gather. Defaults to all stats.
  --run_label: the label to associate with the pbench run. No default setting.
  --run_user: user that is actually running the test on the test system. Defaults to user running wrapper.
  --sys_type: Type of system working with, aws, azure, hostname.  Defaults to hostname.
  --sysname: name of the system running, used in determining config files.  Defaults to hostname.
  --tuned_setting: used in naming the tar file, default for RHEL is the current active tuned.  For non
    RHEL systems, default is none.
  --usage: this usage message.
```

Note: The script does not install pbench for you.  You need to do that manually.
