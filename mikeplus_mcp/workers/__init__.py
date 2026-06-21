"""Worker scripts — run as standalone subprocesses, never imported by the server.

Hard rule: each worker imports EITHER mikeplus OR mikeio*/matplotlib, never both
in the same file. run_worker/model_worker use mikeplus (need a MIKE+ license);
results_worker/plot_worker use mikeio1d/mikeio (no license needed).
"""
