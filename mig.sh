#!/bin/bash
# データ同期用に移行元仮想マシンにディレクトリを作成
mkdir ~/wpfiles && mkdir ~/sqlfiles

# WordPressのデータ同期の為に移行元仮想マシンとNFSサーバを同期
sudo mount -t nfs NFS-server:~/nfs_wp ~/wpfiles
# MySQLデータ同期の為に移行元仮想マシンとマスターを同期
sudo mount -t nfs Master:~/dir_sql ~/sqlfiles

# WordPressのデータ圧縮＋MySQLデータをエクスポート
cd /var/www/html
sudo tar pcf ~/nodir.tar --exclude='./wp-admin' --exclude='./wp-content' --exclude='./wp-includes' ./* &
sudo tar pcf ~/content.tar -C /var/www/html wp-content &
sudo tar pcf ~/admin.tar -C /var/www/html wp-admin &
sudo tar pcf ~/includes.tar -C /var/www/html wp-includes &
wait
cd
mysqldump -u YourUser -pYourPassword YourDatabase > wordpress.sql

# データをそれぞれ同期したディレクトリに展開
sudo tar xfp ~/nodir.tar -C ~/wpfiles &
sudo tar xfp ~/content.tar -C ~/wpfiles &
sudo tar xfp ~/admin.tar -C ~/wpfiles &
sudo tar xfp ~/includes.tar -C ~/wpfiles &
wait
sudo mv ~/newconfig.py ~/wpfiles
sudo chown www-data:www-data ~/wpfiles/newconfig.py
mv wordpress.sql ~/sqlfiles
ssh master-user@Master 'mv ~/dir_sql/wordpress.sql ~/'

# 同期解除
sudo umount -l ~/wpfiles
sudo umount -l ~/sqlfiles

# 展開したMySQLデータをインポート
export Mypas="MySQLPassword"
sql=$(ssh master-user@Master 'kubectl get pod' | grep mysql | awk '{print $1}')
ssh master-user@Master "kubectl cp ~/wordpress.sql $sql:/tmp/wordpress.sql"
ssh master-user@Master "kubectl exec -i $sql -- /bin/bash -c 'export MYSQL_PWD=\"MySQLPassword\"; mysql -u YourUser -h YourHost YourDatabase < /tmp/wordpress.sql'"

# 各ファイルを実行
ssh master-user@NFSserver 'python3 ~/nfs_wp/newconfig.py' & ssh master-user@Master 'python3 mysqltable.py' &
wait
