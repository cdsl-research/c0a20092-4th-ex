# wp-config.php ファイルのパスを指定
wp_config_path = '/home/cdsl/nfs_wp/wp-config.php'

# wp-config.php ファイルから情報を抽出
import re

with open(wp_config_path, 'r') as wp_config_file:
    config_contents = wp_config_file.read()

db_name_match = re.search(r"define\(\s*'DB_NAME',\s*'([^']+)'\s*\);", config_contents)
db_user_match = re.search(r"define\(\s*'DB_USER',\s*'([^']+)'\s*\);", config_contents)
db_password_match = re.search(r"define\(\s*'DB_PASSWORD',\s*'([^']+)'\s*\);", config_contents)
db_host_match = re.search(r"define\(\s*'DB_HOST',\s*'([^']+)'\s*\);", config_contents)
db_charset_match = re.search(r"define\(\s*'DB_CHARSET',\s*'([^']+)'\s*\);", config_contents)

key_salt_matches = re.findall(r"define\(\s*'([^']+)',\s*'([^']+)'\s*\);", config_contents)

# ファイルに情報を書き込む
with open('./config_info.txt', 'w') as output_file:
    if db_name_match and db_user_match and db_password_match and db_host_match and db_charset_match:
        db_name = db_name_match.group(1)
        db_user = db_user_match.group(1)
        db_password = db_password_match.group(1)
        db_host = db_host_match.group(1)
        db_charset = db_charset_match.group(1)

        output_file.write(db_name + '\n')
        output_file.write(db_user + '\n')
        output_file.write(db_password + '\n')
        output_file.write(db_host + '\n')
        output_file.write(db_charset + '\n')
    else:
        output_file.write("DB設定が見つかりませんでした。\n")

    if key_salt_matches:
        key_salt_values = {key: value for key, value in key_salt_matches}

        output_file.write(key_salt_values['AUTH_KEY'] + '\n')
        output_file.write(key_salt_values['SECURE_AUTH_KEY'] + '\n')
        output_file.write(key_salt_values['LOGGED_IN_KEY'] + '\n')
        output_file.write(key_salt_values['NONCE_KEY'] + '\n')
        output_file.write(key_salt_values['AUTH_SALT'] + '\n')
        output_file.write(key_salt_values['SECURE_AUTH_SALT'] + '\n')
        output_file.write(key_salt_values['LOGGED_IN_SALT'] + '\n')
        output_file.write(key_salt_values['NONCE_SALT'] + '\n')
    else:
        output_file.write("AUTH_KEYからNONCE_SALTまでの設定が見つかりませんでした。\n")

print("情報は config_info.txt に書き込まれました。")

import os

# 'config_info.txt'ファイルから情報を読み込む
with open('./config_info.txt', 'r') as config_info_file:
    lines = config_info_file.readlines()

# テンプレートファイルの内容
template = """<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 *
 *
 * @package WordPress
 */

// a helper function to lookup "env_FILE", "env", then fallback
if (!function_exists('getenv_docker')) {{
        function getenv_docker($env, $default) {{
                if ($fileEnv = getenv($env . '_FILE')) {{
                        return rtrim(file_get_contents($fileEnv), "\r\n");
                }}
                else if (($val = getenv($env)) !== false) {{
                        return $val;
                }}
                else {{
                        return $default;
                }}
        }}
}}

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', getenv_docker('WORDPRESS_DB_NAME', '{{DB_NAME}}' ));

/** Database username */
define( 'DB_USER', getenv_docker('WORDPRESS_DB_USER', '{{DB_USER}}' ));

/** Database password */
define( 'DB_PASSWORD', getenv_docker('WORDPRESS_DB_PASSWORD', '{{DB_PASSWORD}}' ));

/** Database hostname */
define( 'DB_HOST', getenv_docker('WORDPRESS_DB_HOST', '{{DB_HOST}}' ));

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', getenv_docker('WORDPRESS_DB_CHARSET', '{{DB_CHARSET}}' ));

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', getenv_docker('WORDPRESS_DB_COLLATE', '') );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 *
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         getenv_docker('WORDPRESS_AUTH_KEY', '{{AUTH_KEY}}' ));
define( 'SECURE_AUTH_KEY',  getenv_docker('WORDPRESS_SECURE_AUTH_KEY', '{{SECURE_AUTH_KEY}}' ));
define( 'LOGGED_IN_KEY',    getenv_docker('WORDPRESS_LOGGED_IN_KEY', '{{LOGGED_IN_KEY}}' ));
define( 'NONCE_KEY',        getenv_docker('WORDPRESS_NONCE_KEY', '{{NONCE_KEY}}' ));
define( 'AUTH_SALT',        getenv_docker('WORDPRESS_AUTH_SALT', '{{AUTH_SALT}}' ));
define( 'SECURE_AUTH_SALT', getenv_docker('WORDPRESS_SECURE_AUTH_SALT', '{{SECURE_AUTH_SALT}}' ));
define( 'LOGGED_IN_SALT',   getenv_docker('WORDPRESS_LOGGED_IN_SALT', '{{LOGGED_IN_SALT}}' ));
define( 'NONCE_SALT',       getenv_docker('WORDPRESS_NONCE_SALT', '{{NONCE_SALT}}' ));

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = getenv_docker('WORDPRESS_TABLE_PREFIX', 'wp_');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 *
 */
define( 'WP_DEBUG', !!getenv_docker('WORDPRESS_DEBUG', '') );

/* Add any custom values between this line and the "stop editing" line. */

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {{
        define( 'ABSPATH', __DIR__ . '/' );
}}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
"""

# hostの情報だけ取得
import subprocess
shell_command = "ssh cdsl@c0a20092-master 'kubectl get svc | grep mysql'"
result = subprocess.run(shell_command, shell=True, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = result.stdout
matches = re.findall(r'mysql-\S+', output)
first_match = matches[0]

# config_info.txt から読み込んだ情報をテンプレートに挿入
if len(lines) >= 13:
    template = template.format(
        DB_NAME=lines[0].strip(),
        DB_USER=lines[1].strip(),
        DB_PASSWORD=lines[2].strip(),
        DB_HOST=lines[3].strip(),
        DB_CHARSET=lines[4].strip(),
        AUTH_KEY=lines[5].strip(),
        SECURE_AUTH_KEY=lines[6].strip(),
        LOGGED_IN_KEY=lines[7].strip(),
        NONCE_KEY=lines[8].strip(),
        AUTH_SALT=lines[9].strip(),
        SECURE_AUTH_SALT=lines[10].strip(),
        LOGGED_IN_SALT=lines[11].strip(),
        NONCE_SALT=lines[12].strip()
    )
else:
    print("config_info.txt ファイルに十分な情報が含まれていません。")

template = template.replace('{DB_NAME}', lines[0].strip())
template = template.replace('{DB_USER}', lines[1].strip())
template = template.replace('{DB_PASSWORD}', lines[2].strip())
template = template.replace('{DB_HOST}', first_match)
template = template.replace('{DB_CHARSET}', lines[4].strip())
template = template.replace('{AUTH_KEY}', lines[5].strip())
template = template.replace('{SECURE_AUTH_KEY}', lines[6].strip())
template = template.replace('{LOGGED_IN_KEY}', lines[7].strip())
template = template.replace('{NONCE_KEY}', lines[8].strip())
template = template.replace('{AUTH_SALT}', lines[9].strip())
template = template.replace('{SECURE_AUTH_SALT}', lines[10].strip())
template = template.replace('{LOGGED_IN_SALT}', lines[11].strip())
template = template.replace('{NONCE_SALT}', lines[12].strip())

# 新しいテンプレートファイルを保存
new_wp_config_path = './wp-config.php'
with open(new_wp_config_path, 'w') as output_file:
    output_file.write(template)

# config_info.txt ファイルを削除
if os.path.exists('./config_info.txt'):
    os.remove('./config_info.txt')

print("新しい wp-config.php ファイルが作成されました。")
