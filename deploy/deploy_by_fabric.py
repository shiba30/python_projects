import os
import tempfile

from fabric import Connection

# AWS EC2インスタンスのホスト名またはIPアドレス
# ec2_host = 'ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com'
ec2_host = 'ec2-43-207-68-227.ap-northeast-1.compute.amazonaws.com'

# EC2に接続するための秘密鍵ファイル
key_filename = '/Users/taipon512/.ssh/my_aws_key.pem'

# EC2に接続するためのユーザー名
ec2_user = 'ec2-user'

# デプロイ先のディレクトリ
deploy_dir = '/home/ec2-user/myapp'

# アプリケーションのソースコードがあるローカルのディレクトリ
local_dir = '/Users/taipon512/develop/resume'


# デプロイタスク
def deploy():
    # EC2インスタンスに接続
    conn = Connection(host=ec2_host, user=ec2_user, connect_kwargs={
                      'key_filename': key_filename})

    # デプロイ先のディレクトリを作成
    conn.run(f'mkdir -p {deploy_dir}')

    # ローカルのアプリケーションをEC2に転送
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 圧縮するファイル名
        tar_filename = os.path.join(tmp_dir, "resume.tar.gz")

        # ローカルでディレクトリを圧縮
        os.system(f'tar -czf {tar_filename} -C {local_dir} .')

        # 圧縮されたファイルをリモートに転送
        conn.put(tar_filename, f'{deploy_dir}/resume.tar.gz')

    # リモートで圧縮ファイルを解凍
    conn.run(f'tar -xzf {deploy_dir}/resume.tar.gz -C {deploy_dir}')

    # EC2で必要なパッケージをインストール
    # conn.sudo('sudo apt-get update')
    # git cloneまで
    # conn.sudo('sudo apt-get install git')
    # conn.sudo('git config --global credential.helper store')
    # conn.sudo('git clone https://github.com/ユーザ名/リポジトリ名.git')

    # python app
    conn.sudo('yum -y update')
    # conn.sudo('yum -y install python3 python3-pip')
    # conn.sudo(f'pip3 install -r {deploy_dir}/requirements.txt')

    # データベースをマイグレーション
    # conn.run(f'cd {deploy_dir} && python3 manage.py migrate')

    # アプリケーションを起動
    # conn.sudo('systemctl start myapp')


deploy()


# EC2
# sudo cp /home/ec2-user/myapp/startbootstrap-resume-gh-pages/index.html /var/www/html
# sudo cp -r /home/ec2-user/myapp/startbootstrap-resume-gh-pages/assets /var/www/html
# sudo cp -r /home/ec2-user/myapp/startbootstrap-resume-gh-pages/css /var/www/html
# sudo cp -r /home/ec2-user/myapp/startbootstrap-resume-gh-pages/js /var/www/html
# sudo systemctl start httpd
# sudo systemctl enable httpd
# セキュリティグループの設定: EC2インスタンスのセキュリティグループを設定して、インバウンドルールでHTTP（ポート80）を許可
# ブラウザアクセス　http://ec2-43-207-68-227.ap-northeast-1.compute.amazonaws.com/index.html
