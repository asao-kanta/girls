#!/bin/bash
chsh -s /bin/zsh
# スクリプトが置かれている場所をカレントディレクトリにする。
cd `dirname $0`
# venvの環境をactivateする
source girls/bin/activate

# pythonファイルの実行
python girl_coll.py