英文核心词	5岁都能懂的意思	对应的底层命令	为什么记这个？
Data-at-rest	躺在硬盘里睡觉的数据	ls -l / chmod	审计员要看文件权限。
Data-in-transit	在网线上跑的数据	socket / ssh	保护传输过程不被截获。
Integrity	完整性（没被改过）	sha256sum	证明数据没被黑客动过。
Encryption	加密（变成乱码）	gpg / openssl	PIPL 要求必须做的保护。
De-identification	脱敏（把名字遮住）	regex (正则表达式)	金融审计的核心加分项。
Operational privileges	谁能动这个数据（权限）	sudo / whoami	降低“内鬼”泄密风险。