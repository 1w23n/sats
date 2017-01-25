#!/bin/bash

# ---------------------------------------------------------------------
# Variable definition
# ---------------------------------------------------------------------

SHELL_NAME=`basename $0`
SCRIPT_DIR=`cd $(dirname $0); pwd`
COMMON=${SCRIPT_DIR}/conf/tools.common
LOOP_CNT=0

# ---------------------------------------------------------------------
# Checking various
# ---------------------------------------------------------------------

if [ -f ${COMMON} ]; then
    . ${COMMON}
else
    echo "[ERROR] 共通関数ファイルが見つかりません。"
    exit 1
fi


# ---------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------

# header insert for new file
if [ ! -f ${LOG_FILE} ]; then
    echo "tool_yyyymmdd,tool_timestamp,hostname,severity,id,timestamp,am/pm,\
        iface,rxpck/s,txpck/s,rxkB/s,txkB/s,rxcmp/s,txcmp/s,rxmcst/s,%ifutil" > ${LOG_FILE}
fi

while [ ${LOOP_CNT} -lt 2 ]; do

    # getting network bandwidth stats 
    RESULT=`sar -n DEV 1 1 | grep eth0 | grep -v Average | tr -s " " ","`

    # output log
    WriteLog INFO I001 "${RESULT}" | tee -a ${LOG_FILE}

    (( LOOP_CNT++ ))

done
