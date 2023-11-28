#!/bin/bash
sudo rm ~/nfs_wp/wp-config.php
sudo chown www-data:www-data ./wp-config.php
sudo mv ./wp-config.php ~/nfs_wp
