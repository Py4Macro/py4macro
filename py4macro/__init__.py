# __init__.py

# https://github.com/Py4Macro/py4macro.git

from .py4macro import *

__all__ = ['data','trend','show','xvalues','recessions','fukyo', 'see']

__author__ = 'Tetsu Haruyama'
__version__ = '0.8.11a'
__copyright__ = 'Copyright (c) 2024 Tetsu Haruyama'

__doc__ = """
    「Pythonで学ぶマクロ経済学 (中級＋レベル)」のためのモジュール

        * HPフィルターを使いトレンドを抽出する`trend()`関数
        * `DataFrame`を全て表示する`show()`関数
        * `n`個の浮動小数点数から構成されるリストを返す`xvalues()`関数
        * オブジェクトの属性（`_`もしくは`__`が付いた属性以外）を表示する`see()`関数
        * 後退期間にグレーの塗りつぶしを追加する`fukyo()`関数
        * 後退期間にグレーの塗りつぶしを追加する`recessions()`デコレーター
        * データ・セット
            * Penn World Tables 10.1
            * IMF World Economic Outlook 2024
            * Maddison Project Database 2023
            * 日本の四半期データ（GDPなど）
            * 日本の月次データ（マネーストックなど）
            * 177ヵ国のマネーストックなど
            * 円/ドル為替レート
            * 景気循環日付と拡張・後退期間
            * Big Mac インデックス
            * 政府負債に関する長期時系列データ
