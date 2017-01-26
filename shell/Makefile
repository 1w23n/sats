YYYYMMDD          = `date +%Y%m%d`
LOG_FILE          = ./logs/apl_rls_1w23n_$(YYYYMMDD).log
BACKUP_DIR        = ./$(YYYYMMDD)_BK
RESTORE_DIR       = ./tmp/$(YYYYMMDD)_refuge

# release target dir
1w23n_DIR         = /foo/1w23n
BATCH_DIR         = /baz/batch
BACKUP_1w23n      = $(BACKUP_DIR)$(1w23n_DIR)
BACKUP_BATCH      = $(BACKUP_DIR)$(BATCH_DIR)
RESTORE_1w23n     = $(RESTORE_DIR)$(1w23n_DIR)
RESTORE_BATCH     = $(RESTORE_DIR)$(BATCH_DIR)

USER_CHECK        = `id -u`
PS_1w23n          = `ps -ef | grep -iE '1w23n|java' | grep -v grep | grep -v other | grep -v $${$$} | wc -l`
APL_LIST          = ./conf/apl_rls_1w23n_lists.conf
REHEA_LS          = ./tmp/ls_rehearsal_diff.log
REHEA_HASH        = ./tmp/hash_rehearsal_diff.log

DELETE_CHECK      = `grep -v '^\#' $(APL_LIST) | grep delete | awk -F',' {'print $$4'}`
MATERIAL          = `grep -v '^\#' $(APL_LIST) | awk -F',' {'print $$3'}`
MATERIAL_DATE_OFF = $(MATERIAL) | awk {'print $$1, $$2, $$3, $$4, $$5, $$9'}
RELEASE           = `grep -v '^\#' $(APL_LIST) | awk -F',' {'print $$4'}`
RELEASE_DATE_OFF  = $(RELEASE) | awk {'print $$1, $$2, $$3, $$4, $$5, $$9'}
TEE_LOG           = tee -a $(LOG_FILE)

USER              = user01
GROUP             = users


check:

	@echo "if no arguments, default set [check]."
	@echo "  please input [all|check|backup|install|restore|clean]."
	@echo ""
	@-ls -lR $(MATERIAL) 1> ./logs/ls_material_timestamp_$(YYYYMMDD).log 2> /dev/null
	@-ls -lR $(MATERIAL_DATE_OFF) 1> ./logs/ls_material_diff_$(YYYYMMDD).log 2> /dev/null
	@-sha1sum $(MATERIAL) 1> ./logs/hash_material_diff_$(YYYYMMDD).log 2> /dev/null
	@-ls -lR $(RELEASE) 1> ./logs/ls_apl_timestamp_before_$(YYYYMMDD).log 2> /dev/null
	@-ls -lR $(RELEASE_DATE_OFF) 1> ./logs/ls_apl_diff_before_$(YYYYMMDD).log 2> /dev/null
	@-sha1sum $(RELEASE) 1> ./logs/hash_apl_diff_before_$(YYYYMMDD).log 2> /dev/null
	@-find $(1w23n_DIR) $(BATCH_DIR) -type f -exec 'sha1sum' {} \; 1> ./logs/hash_apl_all_before_$(YYYYMMDD).log 2> /dev/null
	@echo "create information log."
	@echo "  [./logs/ls_material_timestamp_$(YYYYMMDD).log]"
	@echo "  [./logs/ls_material_diff_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_material_diff_$(YYYYMMDD).log]"
	@echo "  [./logs/ls_apl_timestamp_before_$(YYYYMMDD).log]"
	@echo "  [./logs/ls_apl_diff_before_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_diff_before_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_all_before_$(YYYYMMDD).log]"
	@echo ""
	@. ./conf/common_env.conf ;\
	if [[ ! `hostname` =~ HOSTNAME[09][12] ]]; then \
	  WriteLog ERROR E501 "MSG: must execution in server HOSTNAME01 or HOSTNAME02." | ${TEE_LOG} ;\
	  exit 501 ;\
	elif [ ${USER_CHECK} -ne 0 ]; then \
	  WriteLog ERROR E502 "MSG: must execution in super user. (root)" | ${TEE_LOG} ;\
	  exit 502 ;\
	elif [ ${PS_1w23n} -ne 0 ]; then \
	  WriteLog ERROR E503 "MSG: 1w23n process is running. please stop." | ${TEE_LOG} ;\
	  echo "==== running process ====" ;\
	  echo `ps -ef | grep -iE '1w23n|java' | grep -v grep | grep -v other |  grep -v $${$$}` ;\
	  exit 503 ;\
	elif [ ! -f ${APL_LIST} ]; then \
	  WriteLog ERROR E504 "MSG: ${APL_LIST} not found." | ${TEE_LOG} ;\
	  exit 504 ;\
	elif [ -n ${DELETE_CHECK} ]; then \
	  echo "==== list delete files ====" ;\
	  ls -l ${DELETE_CHECK} ;\
	  echo "" ;\
	fi ;\
	if [ ! -f ${REHEA_LS} ]; then \
	  WriteLog WARNING W301 "MSG: '${REHEA_LS}' not found. can't check material. no problem?" | ${TEE_LOG} ;\
	else \
	  sed -e 's/\/.*\///g' ./logs/ls_material_diff_${YYYYMMDD}.log 1> ./tmp/tmp_ls_material_diff.log 2> /dev/null ;\
	  sed -e 's/\/.*\///g' ${REHEA_LS} 1> ./tmp/tmp_ls_rehearsal_diff.log 2> /dev/null ;\
	  echo "diff ./tmp/tmp_ls_material_diff.log ./tmp/tmp_ls_rehearsal_diff.log" ;\
	  diff ./tmp/tmp_ls_material_diff.log ./tmp/tmp_ls_rehearsal_diff.log 2> /dev/null ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog WARNING W302 "MSG: material and rehearsal result list differs. no problem?" | ${TEE_LOG} ;\
	  else \
	    WriteLog INFO I001 "MSG: material and rehearsal result list matches." | ${TEE_LOG} ;\
	  fi ;\
	  rm ./tmp/tmp_ls_material_diff.log ./tmp/tmp_ls_rehearsal_diff.log 2> /dev/null ;\
	fi ;\
	if [ ! -f ${REHEA_HASH} ]; then \
	  WriteLog WARNING W303 "MSG: '${REHEA_HASH}' not found. can't check material. no problem?" | ${TEE_LOG} ;\
	else \
	  awk {'print $$1'} ./logs/hash_material_diff_${YYYYMMDD}.log 1> ./tmp/tmp_hash_material_diff.log 2> /dev/null ;\
	  awk {'print $$1'} ${REHEA_HASH} 1> ./tmp/tmp_hash_rehearsal_diff.log 2> /dev/null ;\
	  echo "" ;\
	  echo "diff ./tmp/tmp_hash_material_diff.log ./tmp/tmp_hash_rehearsal_diff.log" ;\
	  diff ./tmp/tmp_hash_material_diff.log ./tmp/tmp_hash_rehearsal_diff.log 2> /dev/null ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog WARNING W304 "MSG: material and rehearsal result hash differs. no problem?" | ${TEE_LOG} ;\
	  else \
	    WriteLog INFO I002 "MSG: material and rehearsal result hash matches." | ${TEE_LOG} ;\
	  fi ;\
	  rm ./tmp/tmp_hash_material_diff.log ./tmp/tmp_hash_rehearsal_diff.log 2> /dev/null ;\
	fi
	@echo ""
	@echo "checking environment....end."
	@echo ""


all: check backup


backup: check

	@. ./conf/common_env.conf ;\
	if [ ! -d ${BACKUP_DIR} ]; then \
	  WriteLog INFO I011 "CMD: \"mkdir -p ${BACKUP_1w23n} ${BACKUP_BATCH}\"" | ${TEE_LOG} ;\
	  mkdir -p ${BACKUP_1w23n} ${BACKUP_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E511 "MSG: mkdir failure. (${BACKUP_DIR})" | ${TEE_LOG} ;\
	    exit 511 ;\
	  fi ;\
	  WriteLog INFO I012 "CMD: \"cp -rp ${1w23n_DIR}/* ${BACKUP_1w23n}\"" | ${TEE_LOG} ;\
	  cp -rp ${1w23n_DIR}/* ${BACKUP_1w23n} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E512 "MSG: copy failure from '${1w23n_DIR}' to '${BACKUP_DIR}'." | ${TEE_LOG} ;\
	    exit 512 ;\
	  fi ;\
	  WriteLog INFO I013 "CMD: \"diff -r ${1w23n_DIR} ${BACKUP_1w23n}\"" | ${TEE_LOG} ;\
	  diff -r ${1w23n_DIR} ${BACKUP_1w23n} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E513 "MSG: differnce occurs. (${1w23n_DIR} ${BACKUP_DIR})" | ${TEE_LOG} ;\
	    exit 513 ;\
	  fi ;\
	  WriteLog INFO I014 "CMD: \"cp -rp ${BATCH_DIR}/* ${BACKUP_BATCH}\"" | ${TEE_LOG} ;\
	  cp -rp ${BATCH_DIR}/* ${BACKUP_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E514 "MSG: copy failure from '${BATCH_DIR}' to '${BACKUP_DIR}'." | ${TEE_LOG} ;\
	    exit 514 ;\
	  fi ;\
	  WriteLog INFO I015 "CMD: \"diff -r ${BATCH_DIR} ${BACKUP_BATCH}\"" | ${TEE_LOG} ;\
	  diff -r ${BATCH_DIR} ${BACKUP_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E515 "MSG: differnce occurs. (${BATCH_DIR} ${BACKUP_DIR})" | ${TEE_LOG} ;\
	    exit 515 ;\
	  fi \
	else \
	  WriteLog WARNING W311 "MSG: already exists. (${BACKUP_DIR})" | ${TEE_LOG} ;\
	  exit 311 ;\
	fi
	@echo ""
	@echo "backup successful. ($(BACKUP_DIR))"


install: check

	@. ./conf/common_env.conf ;\
	if [ ! -d ${BACKUP_DIR} ]; then \
	  WriteLog ERROR E520 "MSG: no exists. please backup exec." | ${TEE_LOG} ;\
	  exit 520 ;\
	fi ;\
	exec < ${APL_LIST} ;\
	while read LINE ;\
	do \
	  if [[ ! $${LINE} =~ ^'#' && ! $${LINE} =~ ^$$  ]]; then \
	    FLAG=`echo $${LINE} | awk -F',' {'print $$1'}` ;\
	    case $${FLAG} in \
	      create) \
	        PERM=`echo $${LINE} | awk -F',' {'print $$2'}` ;\
	        RELEASE_APL=`echo $${LINE} | awk -F',' {'print $$3, $$4'} | sed -e 's/,/\ /g'` ;\
	        WriteLog INFO I021 "CMD: \"install -v -m $${PERM} -o ${USER} -g ${GROUP} $${RELEASE_APL}\"" | ${TEE_LOG} 1> /dev/null ;\
	        install -v -m $${PERM} -o ${USER} -g ${GROUP} $${RELEASE_APL} 1> /dev/null ;\
	        if [ $${?} -ne 0 ]; then \
	          WriteLog ERROR E521 "MSG: install failure. ($${RELEASE_APL})" | ${TEE_LOG} ;\
	          continue ;\
	        fi ;\
	        WriteLog INFO I022 "CMD: \"diff $${RELEASE_APL}\"" | ${TEE_LOG} 1> /dev/null ;\
	        diff $${RELEASE_APL} ;\
	        if [ $${?} -ne 0 ]; then \
	          WriteLog ERROR E522 "MSG: difference occurs. ($${RELEASE_APL})" | ${TEE_LOG} ;\
	          continue ;\
	        else \
	          HASH_BEFORE=`sha1sum $$(echo $${LINE} | awk -F',' {'print $$3'}) | awk -F' ' {'print $$1'}` ;\
	          HASH_AFTER=`sha1sum $$(echo $${LINE} | awk -F',' {'print $$4'}) | awk -F' ' {'print $$1'}` ;\
	          if [ "$${HASH_BEFORE}" == "$${HASH_AFTER}" ]; then \
	            WriteLog INFO I023 "MSG: hash matches. ($${RELEASE_APL})" | ${TEE_LOG} 1> /dev/null ;\
	          else \
	            WriteLog ERROR E523 "MSG: hash differs. ($${RELEASE_APL})" | ${TEE_LOG} ;\
	            continue ;\
	          fi \
	        fi \
	        ;; \
	      delete) \
	        RELEASE_APL=`echo $${LINE} | awk -F',' {'print $$4'}` ;\
	        if [ -f $${RELEASE_APL} ]; then \
	          WriteLog INFO I026 "CMD: \"rm $${RELEASE_APL}\"" | ${TEE_LOG} 1> /dev/null ;\
	          rm $${RELEASE_APL} ;\
	          if [ ! -f $${RELEASE_APL} ]; then \
	            WriteLog INFO I027 "MSG: remove success. ($${RELEASE_APL})" | ${TEE_LOG} 1> /dev/null ;\
	            continue ;\
	          else \
	            WriteLog ERROR E527 "MSG: remove failure. ($${RELEASE_APL})" | ${TEE_LOG} ;\
	            continue ;\
	          fi \
	        else \
	          WriteLog WARNING W326 "MSG: already not exist. ($${RELEASE_APL})" | ${TEE_LOG} ;\
	          continue ;\
	        fi \
	        ;; \
	      *) \
	        echo "skiping....first field input mistake. input create or delete." ;\
	        continue ;\
	        ;; \
	    esac \
	  fi \
	done
	@echo ""
	@echo "install successful."
	@echo ""
	@-ls -lR $(RELEASE) 1> ./logs/ls_apl_timestamp_after_$(YYYYMMDD).log 2> /dev/null
	@-ls -lR $(RELEASE_DATE_OFF) 1> ./logs/ls_apl_diff_after_$(YYYYMMDD).log 2> /dev/null
	@-sha1sum $(RELEASE) 1> ./logs/hash_apl_diff_after_$(YYYYMMDD).log 2> /dev/null
	@-find $(1w23n_DIR) $(BATCH_DIR) -type f -exec 'sha1sum' {} \; 1> ./logs/hash_apl_all_after_$(YYYYMMDD).log 2> /dev/null
	@echo "create information log."
	@echo "  [./logs/ls_apl_timestamp_after_$(YYYYMMDD).log]"
	@echo "  [./logs/ls_apl_diff_after_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_diff_after_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_all_after_$(YYYYMMDD).log]"
	@echo ""
	@echo "final confirmation..."
	@. ./conf/common_env.conf ;\
	diff ${REHEA_LS} ./logs/ls_apl_diff_after_${YYYYMMDD}.log 2> /dev/null ;\
	if [ $${?} -ne 0 ]; then \
	  WriteLog ERROR E528 "MSG: list information differs." | ${TEE_LOG} ;\
	else \
	  WriteLog INFO I028 "MSG: list information matches." | ${TEE_LOG} ;\
	fi ;\
	diff ${REHEA_HASH} ./logs/hash_apl_diff_after_${YYYYMMDD}.log 2> /dev/null ;\
	if [ $${?} -ne 0 ]; then \
	  WriteLog ERROR E529 "MSG: hash differs." | ${TEE_LOG} ;\
	else \
	  WriteLog INFO I029 "MSG: all hash matches. release compleated!" | ${TEE_LOG} ;\
	fi


restore:

	@. ./conf/common_env.conf ;\
	if [ ! -d ${BACKUP_DIR} ]; then \
	  WriteLog ERROR E530 "MSG: can't restore, because not exists. (${BACKUP_DIR})" | ${TEE_LOG} ;\
	  exit 530 ;\
	elif [ -z ${1w23n_DIR} -o -z ${BATCH_DIR} ]; then \
	  WriteLog ERROR E531 "MSG: dangerous action!! '\$${1w23n_DIR}' or '\$${BATCH_DIR}' is empty." | ${TEE_LOG} ;\
	  exit 531 ;\
	elif [ ! -d ${RESTORE_DIR} ]; then \
	  WriteLog INFO I032 "CMD: \"mkdir -p ${RESTORE_1w23n} ${RESTORE_BATCH}\"" | ${TEE_LOG} ;\
	  mkdir -p ${RESTORE_1w23n} ${RESTORE_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E532 "MSG: mkdir failure. (${RESTORE_DIR})" | ${TEE_LOG} ;\
	    exit 532 ;\
	  fi ;\
	  WriteLog INFO I033 "CMD: \"mv ${1w23n_DIR}/* ${RESTORE_1w23n}\"" | ${TEE_LOG} ;\
	  mv ${1w23n_DIR}/* ${RESTORE_1w23n} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E533 "MSG: move failure from '${1w23n_DIR}/*' to '${RESTORE_DIR}'." | ${TEE_LOG} ;\
	    exit 533 ;\
	  fi ;\
	  WriteLog INFO I034 "CMD: \"cp -rp ${BACKUP_1w23n}/* ${1w23n_DIR}\"" | ${TEE_LOG} ;\
	  cp -rp ${BACKUP_1w23n}/* ${1w23n_DIR} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E534 "MSG: copy failure from '${BACKUP_DIR}' to '${1w23n_DIR}'." | ${TEE_LOG} ;\
	    exit 534 ;\
	  fi ;\
	  WriteLog INFO I035 "CMD: \"diff -r ${1w23n_DIR} ${BACKUP_1w23n}\"" | ${TEE_LOG} ;\
	  diff -r ${1w23n_DIR} ${BACKUP_1w23n} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E535 "MSG: differnce occurs. (${1w23n_DIR} ${BACKUP_DIR})" | ${TEE_LOG} ;\
	    exit 535 ;\
	  fi ;\
	  WriteLog INFO I036 "CMD: \"mv ${BATCH_DIR}/* ${RESTORE_BATCH}\"" | ${TEE_LOG} ;\
	  mv ${BATCH_DIR}/* ${RESTORE_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E536 "MSG: move failure from '${BATCH_DIR}/*' to '${RESTORE_DIR}'." | ${TEE_LOG} ;\
	    exit 536 ;\
	  fi ;\
	  WriteLog INFO I037 "CMD: \"cp -rp ${BACKUP_BATCH}/* ${BATCH_DIR}\"" | ${TEE_LOG} ;\
	  cp -rp ${BACKUP_BATCH}/* ${BATCH_DIR} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E537 "MSG: copy failure from '${BACKUP_DIR}' to '${BATCH_DIR}'." | ${TEE_LOG} ;\
	    exit 537 ;\
	  fi ;\
	  WriteLog INFO I038 "CMD: \"diff -r ${BATCH_DIR} ${BACKUP_BATCH}\"" | ${TEE_LOG} ;\
	  diff -r ${BATCH_DIR} ${BACKUP_BATCH} ;\
	  if [ $${?} -ne 0 ]; then \
	    WriteLog ERROR E538 "MSG: differnce occurs. (${BATCH_DIR} ${BACKUP_DIR})" | ${TEE_LOG} ;\
	    exit 538 ;\
	  fi \
	else \
	  WriteLog WARNING W332 "MSG: already exists. (${RESTORE_DIR})" | ${TEE_LOG} ;\
	  exit 332 ;\
	fi
	@echo ""
	@echo "restore successful."
	@-ls -lR $(RELEASE) 1> ./logs/ls_apl_timestamp_restore_$(YYYYMMDD).log 2> /dev/null
	@-ls -lR $(RELEASE_DATE_OFF) 1> ./logs/ls_apl_diff_restore_$(YYYYMMDD).log 2> /dev/null
	@-sha1sum $(RELEASE) 1> ./logs/hash_apl_diff_restore_$(YYYYMMDD).log 2> /dev/null
	@-find $(1w23n_DIR) $(BATCH_DIR) -type f -exec 'sha1sum' {} \; 1> ./logs/hash_apl_all_restore_$(YYYYMMDD).log 2> /dev/null
	@echo ""
	@echo "create information log."
	@echo "  [./logs/ls_apl_timestamp_restore_$(YYYYMMDD).log]"
	@echo "  [./logs/ls_apl_diff_restore_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_diff_restore_$(YYYYMMDD).log]"
	@echo "  [./logs/hash_apl_all_restore_$(YYYYMMDD).log]"


clean:

	@echo "[clean] not defined."
