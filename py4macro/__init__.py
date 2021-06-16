# __init__.py

# https://github.com/Py4Macro/py4macro.git

from .py4macro import *

__all__ = ['data','trend','show']

__author__ = 'Tetsu Haruyama'
__version__ = '0.4.0'
__copyright__ = 'Copyright (c) 2021 Tetsu Haruyama'

__doc__ = """
    「Pythonで学ぶ中級マクロ経済学」のためのモジュール

        * HPフィルター関数
        * DataFrameを全て表示するshow関数
        * データ・セット
            * Penn World Tables 10.0
            * IMF World Economic Outlook 2021
            * Maddison Project Database 2020
            * 日本の四半期データ（GDPなど）
            * 日本の四半期データ（マネーストックなど）
            * 177ヵ国のマネーストックなど"""
