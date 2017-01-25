#!/bin/bash

# ---------------------------------------------------------------------
# Variable definition
# ---------------------------------------------------------------------

SHELL_NAME=`basename $0`
SCRIPT_DIR=`cd $(dirname $0); pwd`
COMMON=${SCRIPT_DIR}/conf/tools.common

# target host
IP_LIST=`cat ${SCRIPT_DIR}/conf/iplist | grep -v ^#`


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

# ping to each server
for host in ${IP_LIST}; do

    # survival confirmation of the target host (timeout 3sec)
    ping -w 3 -c 1 ${host} > /dev/null 2>&1
    if [ ${?} -eq 0 ]; then

        # get average value for response time of ping 10 times (decimal point truncation)
        RESULT=`ping -c 10 -q ${host} | grep rtt`
        AVERAGE=`echo ${RESULT} | awk '{print $4}' | awk -F/ '{print $2}' | sed s/\.[0-9,]*$//g`

        # warning message if response time is more than 2sec
        if [ ${AVERAGE} -gt 2000 ]; then
            WriteLog WARNING W001 "${host} response time 2000 ms over ${AVERAGE} ms.[${RESULT}]" | \
                tee -a ${LOG_FILE}
        else
            WriteLog INFO I001 "${host} response time ${AVERAGE} ms.[${RESULT}]" | \
                tee -a ${LOG_FILE}
        fi
    else
        WriteLog ERROR E001 "${host} not reachable for icmp." | \
            tee -a ${LOG_FILE}
    fi
done
