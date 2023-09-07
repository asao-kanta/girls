#!/bin/bash
chsh -s /bin/zsh
# スクリプトが置かれている場所をカレントディレクトリにする。
cd `dirname $0`

# 念のためvirtualenvのインストールとpipのアップグレードを行う。
pip install virtualenv
python -m pip install --upgrade pip

# venvの環境を構築する。
python3 -m venv girls
source girls/bin/activate

python -m pip install --upgrade pip
# 各パッケージをインストール
pip install pandas
pip install requests
pip install beautifulsoup4