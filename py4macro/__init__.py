# __init__.py

# https://github.com/Py4Macro/py4macro.git

from .py4macro import *

__all__ = ['data','trend','show']

__author__ = 'Tetsu Haruyama'
__version__ = '0.6.0'
__copyright__ = 'Copyright (c) 2022 Tetsu Haruyama'

__doc__ = """
    「Pythonで学ぶマクロ経済学 (中級＋レベル)」のためのモジュール

        * HPフィルター関数
        * DataFrameを全て表示するshow関数
        * データ・セット
            * Penn World Tables 10.0
            * IMF World Economic Outlook 2021
            * Maddison Project Database 2020
            * 日本の四半期データ（GDPなど）
            * 日本の四半期データ（マネーストックなど）
            * 177ヵ国のマネーストックなど
            * 円/ドル為替レート"""
