#!/bin/bash
# mysql full and increment
dumpdate=$(date +%Y%m%d)
User="backup"
Password="1qaz!QAZ"
Mysqldump=/bin/mysqldump
Mysql=/bin/mysql
size="+28"
namespace="mysqlns"
main_dir=/data/sqlbackup
Catalogue="${main_dir}/${dumpdate}"
Xdb_Leader_IP=$(/bin/kubectl get svc -n ${namespace} |grep xdbmysql57-leader|awk '{print $3}')
Xdb_Leader_Pod=$(kubectl get pod -n ${namespace} -l 'app=xdbmysql57,release=xdbmysql57,role=leader' |awk '/xdb/{print $1}')
test ! -d ${Catalogue} && mkdir -pv ${Catalogue}
test ! -d ${Catalogue}/logs && mkdir -pv ${Catalogue}/logs
test ! -d ${Catalogue}/all && mkdir -pv ${Catalogue}/all
test ! -d ${Catalogue}/increment && mkdir -pv ${Catalogue}/increment

# 清理历史保留记录
function delete_file() {

	find ${main_dir}  -maxdepth 1 ! -path ${main_dir} -type d -mtime ${size} |xargs -i rm -rf {}

}

function  full_database() {
	
        # 记录当前使用的binlog
	echo "${dumpdate} 开始全量数据库备份" >>  ${Catalogue}/logs/bcakup.log
        ${Mysqldump} -h${Xdb_Leader_IP} -u${User} -p${Password}  --quick --events --all-databases --flush-logs --delete-master-logs --single-transaction |gzip > ${Catalogue}/all/${dumpdate}.sql.gz
        echo "${dumpdate} 全量数据库备份完成" >>  ${Catalogue}/logs/bcakup.log
        if [ $? -eq 0 ];then
		# 记录当前使用的binlog
        	${Mysql} -h ${Xdb_Leader_IP} -u${User} -p${Password} -e "show master status;"|awk '/mysql-*/{print $1,$2}'  >> ${Catalogue}/Use_BinLog_File.txt
        	echo "开始全量数据库备份-记录当前binlog完成 ${dumpdate}" >>  ${Catalogue}/logs/bcakup.log
	fi

}

function increment() {


	# 获取上次全量备份后生成的binlog位置
	last_binlog_file=$(cat  ${Catalogue}/Use_BinLog_File.txt|awk '{print $1}')
	# 查询mysql数据目录位置
	databaseDir=$(${Mysql} -h ${Xdb_Leader_IP} -u${User} -p${Password} -e "show global variables like 'datadir'"|awk '/datadir/{print $2}')	
	# 获取当前mysql所有binlog文件
	binary_array=$(${Mysql} -h ${Xdb_Leader_IP} -u${User} -p${Password} -e "show binary logs;" |awk '/mysql/{print $1}')
	for i in ${binary_array[*]};do
		file_name=${Catalogue}/increment/${i}
		if [ ! -f ${file_name} ];then
			kubectl cp -n ${namespace} ${Xdb_Leader_Pod}:${databaseDir#/}${i} ${Catalogue}/increment/${i}
			if [ $? -eq 0 ];then

				echo "${dumpdate} 增量binlog备份完成: ${i}" >> ${Catalogue}/logs/bcakup.log
			else
				echo "${dumpdate} 增量binlog备份失败: ${i}" >> ${Catalogue}/logs/bcakup.log 
			fi
		fi
				
	done

}

function main() {

	case $1 in
		"full")
		full_database;;
		"increment")
		increment;;
		*)
		echo "输入有误full_database=全备，increment增量备份！"
		;;
	esac		

}
main $*
