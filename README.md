# c0a20092-4th-ex
このソフトウェアの想定として、移行前の仮想マシンと移行先のKubernetesクラスタのマスターノード(Master)及びNFSサーバ(NFSserver)がある状況。
Masterのユーザーはmaster-userです。4つのファイルを3つのノードに以下の様に配置してください。
mig.sh, newconfig.py ⇒ 移行前の仮想マシン。
mysqltable.py ⇒ Kubernetesクラスタのマスターノード
mvfile.sh ⇒ NFSサーバ

## mig.sh
一番最初に実行するファイルです。

## newconfig.py
mig.sh中に自動で実行されます。自分から動かすことはありません

## mysqltable.py
mig.sh中に自動で実行されます。自分から動かすことはありません。

## mvfile.sh
mig.shが終了した後に動かしてください。
