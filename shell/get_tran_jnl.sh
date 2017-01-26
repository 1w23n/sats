#!/bin/sh

YYYYMMDD=${1}

SHELL_NAME=`basename $0 .sh`
SCRIPT_DIR=`cd $(dirname $0); pwd`
LOG_FILE=${SCRIPT_DIR}/logs/${SHELL_NAME}_${YYYYMMDD}.log

FLG_CNT=0
USER_CHECK=`id | grep user01 | cut -c 1-1`

if [[ ! `hostname` =~ HOSTNAME[12] ]]; then
  echo "[ERROR]must execution in server HOSTNAME01 or HOSTNAME02."
  exit 501
elif [ -z ${USER_CHECK} ]; then
  echo "[ERROR]must execution in user user01."
  exit 502
elif [ ${#} -eq 0 -o ${#} -gt 3 ]; then
  echo "[ERROR]incorrect arguments."
  echo "ex."
  echo "  sh ${SHELL_NAME}.sh <YYYYMMDD> [--limit=<int>] [--file]"
  exit 503
fi

for i in ${@}
do
  if [[ "${i}" =~ --limit=[0-9]+$ ]]; then
    LIMIT_ROWNUM=`echo ${i} | awk -F'=' {'print $2'}`
    FLG_CNT=$(( FLG_CNT+1 ))
  elif [ "${i}" == "--file" ]; then
    FLG_CNT=$(( FLG_CNT+2 ))
  fi
done

case ${FLG_CNT} in

  0) # stdout result full
    sqlplus -s "USER01/foobaz" << EOF
      set linesize 30000
      set long 1500
      set longchunksize 1500
      set pagesize 0
      set trimspool on
      set colsep ','
      column jnl_hdr format a500
      column jnl_bdy format a1500

      select
        *
       from
        T_JNL_${YYYYMMDD}
       order by
        JNL_SEQ asc;

      exit
EOF
      ;;


  1) # stdout result limit
    sqlplus -s "USER01/foobaz" << EOF
      set linesize 30000
      set long 1500
      set longchunksize 1500
      set pagesize 0
      set trimspool on
      set colsep ','
      column jnl_hdr format a500
      column jnl_bdy format a1500

      select
        *
       from
        T_JNL_${YYYYMMDD}
       where
        rownum <= ${LIMIT_ROWNUM}
       order by
        JNL_SEQ asc;

      exit
EOF
      ;;

  2) # stdout result full with output file
    sqlplus -s "USER01/foobaz" << EOF
      set linesize 30000
      set long 1500
      set longchunksize 1500
      set pagesize 0
      set trimspool on
      set colsep ','
      column jnl_hdr format a500
      column jnl_bdy format a1500

      spool ${LOG_FILE} app

      select
        *
       from
        T_JNL_${YYYYMMDD}
       order by
        JNL_SEQ asc;

      spool off
      exit
EOF
      ;;

  3) # stdout result limit with output file
    sqlplus -s "USER01/foobaz" << EOF
      set linesize 30000
      set long 1500
      set longchunksize 1500
      set pagesize 0
      set trimspool on
      set colsep ','
      column jnl_hdr format a500
      column jnl_bdy format a1500

      spool ${LOG_FILE} app

      select
        *
       from
        T_JNL_${YYYYMMDD}
       where
        rownum <= ${LIMIT_ROWNUM}
       order by
        JNL_SEQ asc;

      spool off
      exit
EOF
      ;;

  *)
    echo "[ERROR]arguments error."
    ;;

esac

if [ ${?} -ne 0 ]; then
  echo "[ERROR]sqlplus exec error."
  exit 511
fi

exit 0
