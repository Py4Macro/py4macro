import functools
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from math import ceil
from os.path import abspath, join, split


# ===== Definitions ===========================================================

jpn_yr_definitions = """
    | `gdp`:          国内総生産（GDP）
    | `consumption`:  消費
    | `investment`:   投資
    | `government`:   政府支出
    | `exports`:      輸出
    | `imports`:      輸入
    | `gdp_gap`:      GDPギャップ
    | `deflator`:     GDPデフレーター
    | `inflation`:    インフレ率
    | `unemployment_rate`: 失業率
    | `employed`:     就業者数
    | `population`:   人口
    | `gov_debt`:     政府負債
    | `gov_net_debt`: 政府純負債
    |
    | * 年次データ（暦年）
    |
    | ＜出典＞
    | GDPと各需要項目
    |    * 1994年~
    |        * 実額、暦年
    |        * 連鎖価格
    |        * 参照年：2015暦年（平成27年）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |    * 1980年~1993年
    |        * 実額、暦年
    |        * 2015年（平成27年）基準支出側GDP系列簡易遡及（参考系列であり上のデータと接続可能）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | GDPギャップ
    |   * 単位：％
    |   * GDPの潜在GDPからの乖離
    |   * IMF World Economic Outlook
    |
    | GDPデフレーター
    |   * IMF World Economic Outlook
    |
    | インフレ率
    |   * 単位：％
    |   * 年平均
    |   * IMF World Economic Outlook
    |
    | 失業率
    |   * 単位：％
    |   * IMF World Economic Outlook
    |
    | 就業者数，人口
    |   * 単位：万人
    |   * IMF World Economic Outlook
    |
    | 政府負債
    |   * 単位：10億円
    |   * IMF World Economic Outlook
    |
    | 政府純負債
    |   * 単位：10億円
    |   * IMF World Economic Outlook"""


jpn_q_definitions = """
    | `gdp`:         国内総生産（GDP）
    | `consumption`: 消費
    | `investment`:  投資
    | `government`:  政府支出
    | `exports`:     輸出
    | `imports`:     輸入
    | `capital`:     資本ストック
    | `employed`:    就業者数
    | `unemployed`:  失業者数
    | `unemployment_rate`: 失業率
    | `hours`:       労働者一人当たり月平均労働時間
    | `total_hours`: 月平均総労働時間（`employed`X`hours`）
    | `inflation`:   インフレ率
    | `price`:       消費者物価指数
    | `deflator`:    GDPデフレーター
    |
    | * 四半期データ
    |
    | ＜出典＞
    | GDPと各需要項目
    |    * 1994年Q1~2023年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 連鎖価格
    |        * 参照年：2015年（平成27年）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |    * 1980年Q1~1993年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 平成27年基準支出側GDP系列簡易遡及（参考系列であり上のデータと接続可能）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | 実質資本ストック
    |   * 1994年Q1~2023年Q4
    |        * 平成25年基準
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |   * 1980年Q1~1993年Q4
    |        * 平成25年基準遡及系列
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | 就業者数，失業者数，失業率
    |   * 総務省「労働力調査」
    |   * 単位：万人，％
    |
    | 労働者一人当たり月平均労働時間
    |   * 厚生労働省「毎月勤労統計調査」
    |   * 30 人以上(一般・パート)、月間実労働時間(総実労働時間)
    |   * 2020年の平均を100に基準化
    |
    | インフレ率
    |   * 景気動向指数（生鮮食品を除く総合，速報，改訂値，月次，原数値の前年同月比）から四半期平均として計算
    |
    | 消費者物価指数
    |   * 2020年基準
    |   * 「中分類指数（全国）＜時系列表＞【月次】」の四半期平均として計算
    |   * 簡便的な移動平均を使い季節調整を施している
    |
    | GDPデフレーター
    |   * 1994年Q1~2023年Q4
    |       * 2015年（平成27年）基準
    |       * 季節調整系列
    |   * 1980年Q1~1993年Q4
    |       * 2015年（平成27年）基準遡及系列
    |       * 季節調整系列"""

jpn_money_definitions = """
    | `cpi`: 消費者物価指数
    |   * 2015年の値を`100`
    |   * 季節調整済み
    | `money`: マネーストック（M1）
    |   * 2015年の値を`100`
    |   * 季節調整済み
    |
    | * 月次データ
    | * 1955年1月〜2020年12月
    |
    | ＜出典＞
    | OECD Main Economic Indicators"""

world_money_definitions = """
    | `iso`:          ISO国コード
    | `country`:      国名
    | `year`:         年
    | `income_group`: 世界銀行が定義する所得グループ
    |   * High income
    |   * Upper Middle income
    |   * Lower Middle income
    |   * Low income
    | `money`:        マネーストック（M1）
    | `deflator`:     GDPディフレーター
    |
    | * 年次データ
    |
    | ＜注意点＞
    | * `money`と`deflator`が10年間以上連続で欠損値がない経済（177ヵ国）のみが含まれている。
    | * 国によって含まれるデータの`year`が異なる。
    | * 所得グループに関する情報
    |   https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
    |
    | ＜出典＞
    | World Bank Development Indicators"""

ex_definitions = """
    | `real_ex_geus_%change`: 独マルク/米ドル実質為替レート変動率（％）
    |                           * 月次，季節調整ない
    | `real_ex_jpus_%change`: 円/米ドル実質為替レート変動率（％）
    |                           * 月次，季節調整ない
    | `real_ex_jpus`:         円/米ドル実質為替レート
    |                           * 月次，季節調整ない
    | `ex_jpus`:              円/米ドル名目為替レート
    |                           * 月次，季節調整ない
    | `relative_p_jpus`:      日本の一般物価水準に対しての米国の一般物価水準の比率
    |                           * 日本のCPI分の米国のCPI
    |                           * 2015年CPI=100
    |                           * 月次，季節調整ない
    |
    | * 月次データ
    | * 期間：1960年1月〜
    |
    | ＜出典＞
    | OECD Main Economic Indicators"""

dates_definitions = """
    | `tani1`:       １つの循環における第１の谷
    | `yama`:        １つの循環における山
    | `tani2`:       １つの循環における第２の谷
    | `expansion`:   拡張期の期間（単位：月）
    |                `tani1`から`yama`までの期間
    | `contraction`: 後退期の期間（単位：月）
    |                `yama`から`tani2`までの期間
    |
    | ＜出典＞
    | 内閣府
    | https://www.esri.cao.go.jp/jp/stat/di/hiduke.html"""

bigmac_definitions = """
    | `year`:          年（2000年〜）
    | `country`:       国名
    | `iso`:           ISO国コード
    | `currency_code`: 通貨コード
    | `price_local`:   Big Macの価格（自国通貨単位）
    | `exr`:           名目為替レート（自国通貨単位/米ドル）
    | `gdppc_local`:   名目一人当たりGDP（自国通貨単位）
    |
    | * 年次データ
    |
    | ＜出典＞
    | https://github.com/TheEconomist/big-mac-data (Copyright The Economist)"""

mad_definitions = """
    | `GDP pc`:        Real GDP per capita in 2011$
    | `Population`:    Population, mid-year (thousands)
    | `Regional data`: Regional GDP per capita and population estimates
    |
    | * `GDP pc`が欠損値の行は全て削除している。
    |
    | ＜出典＞
    | Maddison Project Database 2023
    |
    | https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023
    |
    | Bolt, Jutta, and Jan Luiten van Zanden (2024) "Maddison-style estimates of
    | the evolution of the world economy: A new 2023 update." Journal of Economic
    | Surveys, pp.1-41."""

debts_definitions = """
    | `countrycode`:      ISO3国名コード
    | `country`:          国名
    | `year`:             年
    | `revenue`:          Government revenue, percent of GDP
    | `expenditure`:      Government expenditure, percent of GDP
    | `interest_exp`:     Government interest expense, percent of GDP
    | `prim_expenditure`: Government primary expenditure, percent of GDP
    | `prim_balance`:     Government primary balance, percent of GDP
    | `debt`:             Government gross debt, percent of GDP
    | `rltir`:            Real long-term interest rate, percent
    | `rgc`:              Real GDP growth rate, percent
    | `GG_budg`:          sector coverage indicator for rev, exp, ie (0 for central gov't, 1 for general gov't)
    | `GG_debt`:          sector coverage indicator for debt (0 for central gov't, 1 for general gov't)
    |
    | ＜出典＞
    | Public Finances in Modern History
    | https://www.imf.org/external/datamapper/datasets/FPP"""

# ===== Helper functions ======================================================


def _get_path(f):
    return split(abspath(f))[0]


def _find_full_file_path(path, dataset_to_open):
    """
    parameters:
        path: the folder of`py4macro.py`
        dataset_to_open: dataset to open

    return:
        a full file path of `dataset_to_open` including its file name"""

    for current_folder, sub_folders, _files in os.walk(path):
        if dataset_to_open in _files:
            return os.path.join(current_folder, dataset_to_open)


# ===== Non-data-related functions ============================================


def trend(s, lamb=1600):
    """|
       | 引数:
       |     s: Seriesもしくは１列のDataFrameとし，行のラベルはDatetimeIndexとすること。
       |     lamb: 四半期用のデータでは通常の値（デフォルト：1600）
       |
       | 返り値:
       |     Hodrick-Prescott filterで計算したtrend（トレンド）のSeries
       |
       | 例: py4macro.trend(df.loc[:,'gdp'])"""

    from statsmodels.tsa.filters.hp_filter import hpfilter

    return hpfilter(s.dropna(), lamb=lamb)[1]


def show(df):
    """|
       | 引数：DetaFrame
       |
       | 戻り値：行・列ともに全て表示する。
       |
       | 例：py4macro.show(＜DataFrame＞)"""

    with pd.option_context('display.max_colwidth',
                           None,
                           'display.max_rows',
                           None):
        display(df)


def xvalues(l, h, n):
    """引数
        l：最小値（lowest value）
        h：最大値（highest value）
        n：作成する数値の数を指定する（正の整数型，number of values）
    戻り値
        n個の要素から構成されるリスト"""

    if (n <= 1) or (not isinstance(n, int)):
        raise Exception(f"引数 n には2以上の整数型を使う必要があります。n={n}となっています。")
    elif l >= h:
        raise Exception(
            "引数 l と h の値では l>h もしくは l=h となります。l<h となるように値を設定し直してください。"
        )
    else:
        return [l + x*(h-l)/(n-1) for x in range(n)]


def fukyo(ax, start=1980, end=2999, color='k', alpha=0.1):
    """
    * 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加する関数
    * `@py4macro.recessions`デコレーターとの違い
        * `@py4macro.recessions`は全ての図に塗りつぶしを追加する
        * `fukyo()`関数は個々の軸に塗りつぶしを追加する

    引数：
        ax：`matplotlib`の軸
        start：`fukyo()`関数を適用し始める年（デフォルトは`1980`）
        end：`fukyo()`関数を適用し終わる年（デフォルトは`2999`）
        color：色（デフォルトは黒）
        alpha：透明度（デフォルトは`0.1）

    戻り値：
        なし（表示のみ）

    ＜例１：一つの図＞
    fig, ax = plt.subplots()
    ax.plot(...)
    fukyo(ax)

    ＜例２：一つの図＞
    ax = <DataFrame もしくは Series>.plot()
    fukyo(ax, start=1960)

    ＜例３：複数の図の中で一つだけに追加＞
    fig, ax = plt.subplots(2,1)
    ax[0].plot(...)
    ax[1].plot(...)
    fukyo(ax[0], start=1970, end=2000, color='grey', alpha=0.2)

    ＜景気基準日付＞ https://www.esri.cao.go.jp/jp/stat/di/hiduke.html"""

    full_file_path = _find_full_file_path(_get_path(__file__), 'cycle_dates.csv.bz2')
    df = pd.read_csv(full_file_path,
                     index_col='index',
                     parse_dates=['tani1','yama','tani2'],
                     compression="bz2",
                     dtype={'expansion': 'Int64', 'contraction': 'Int64'})

    if start < 1951:
        print('\n景気基準日付は1951年6月から始まります。\n')
        
    yr_lst = df['yama'].astype(str).str[:4].astype(int)
    cond = ( yr_lst >= start ) & ( yr_lst <= end )
    df = df.loc[cond,:].reset_index(drop=True)
    
    for i in df.index:
        yama = df.loc[i, 'yama']
        tani = df.loc[i, 'tani2']
        ax.axvspan(yama, tani, fill=True, linewidth=0,
                   color=color, alpha=alpha)
    # return ax


# ===== Decorator =============================================================


def recessions(start=1980, end=2999, color='k', alpha=0.1):
    """
    * 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加するデコレーター
    * `fukyo()`関数との違い
        * `@py4macro.recessions`は全ての図に塗りつぶしを追加する
        * `fukyo()`関数は個々の軸に塗りつぶしを追加する

    引数：
        start：`fukyo()`関数を適用し始める年（デフォルトは`1980`）
        end：`fukyo()`関数を適用し終わる年（デフォルトは`2999`）
        color：色（デフォルトは黒）
        alpha：透明度（デフォルトは`0.1）

    戻り値
        funcが返す軸を返す

    ＜例１：一つの図をプロット（軸を返さない）＞
    @py4macro.recessions()
    def plot():
        <DataFrame もしくは Series>.plot()

    ＜例２：一つの図をプロット（軸を返す）＞
    @py4macro.recessions(star=1960, color='r')
    def plot():
        ax = <DataFrame もしくは Series>.plot()
        return ax

    ＜例３：一つの図をプロット＞
    @py4macro.recessions(end=2005, alpha=0.5)
    def plot():
        fig, ax = plt.subplots()
        ax.plot(...)
        return ax       # 省略すると軸を返さない

    ＜例４：複数の図をプロット＞
    @py4macro.recessions(color='green', alpha=0.2)
    def plot():
        ax = <DataFrame>.plot(subplots=True, layout=(2,2))
        return ax       # この行は必須

    ＜例５：複数の図をプロット＞
    @py4macro.recessions(start=1970, end=2015, color='grey', alpha=0.1)
    def plot():
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(...)
        ax[1].plot(...)
        return ax       # この行は必須"""

    full_file_path = _find_full_file_path(_get_path(__file__), 'cycle_dates.csv.bz2')
    df = pd.read_csv(full_file_path,
                     index_col='index',
                     parse_dates=['tani1','yama','tani2'],
                     compression="bz2",
                     dtype={'expansion': 'Int64', 'contraction': 'Int64'})

    def _recessions(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            nonlocal df, start, end, color, alpha

            if start < 1951:
                print('\n景気基準日付は1951年6月から始まります。\n')

            ax = func(*args, **kwargs)

            # 図が一つの場合，軸はそのまま返される
            if not isinstance(ax, np.ndarray):

                yr_lst = df['yama'].astype(str).str[:4].astype(int)
                cond = ( yr_lst >= start ) & ( yr_lst <= end )
                df = df.loc[cond,:].reset_index(drop=True)

                for i in df.index:
                    yama = df.loc[i, 'yama']
                    tani = df.loc[i, 'tani2']
                    plt.axvspan(yama, tani, fill=True, linewidth=0,
                               color=color, alpha=alpha)

                return ax

            # 図が複数の場合，軸はarrayとして返される
            # DataFrame.plot()で縦に並べる場合，軸は１次元配列となる
            elif ax.ndim == 1:
                n = len(ax)
                for r in range(n):

                    yr_lst = df['yama'].astype(str).str[:4].astype(int)
                    cond = ( yr_lst >= start ) & ( yr_lst <= end )
                    df = df.loc[cond,:].reset_index(drop=True)
                    
                    for i in df.index:
                        yama = df.loc[i, 'yama']
                        tani = df.loc[i, 'tani2']
                        ax[r].axvspan(yama, tani, fill=True, linewidth=0,
                                   color=color, alpha=alpha)

                return ax

            # 軸のarrayが2次元配列となる場合
            elif ax.ndim > 1:
                row = ax.shape[0]
                col = ax.shape[1]
                for r in range(row):
                    for c in range(col):

                        yr_lst = df['yama'].astype(str).str[:4].astype(int)
                        cond = ( yr_lst >= start ) & ( yr_lst <= end )
                        df = df.loc[cond,:].reset_index(drop=True)
                        
                        for i in df.index:
                            yama = df.loc[i, 'yama']
                            tani = df.loc[i, 'tani2']
                            ax[r,c].axvspan(yama, tani, fill=True, linewidth=0,
                                       color=color, alpha=alpha)
                return ax

        return wrapper

    return _recessions


# ===== see function (show attributes) =======================================


def _create_template(obj, col, width):
    """
    表示用のテンプレートを作成する関数

    引数：
        obj: 属性を調べるオブジェクト
        col: 表示する際の列の数
        width: 表示の幅
        　　　　　(列の幅は width/col 以上である最小整数となる)
    戻り値：
        テンプレートを含む辞書
            値：任意の行の列
            値：テンプレートのリスト


    例：3つの列があり，表示全体の幅は20

　　    _create_template(obj_x, col=3, width=20)

       ＜実行結果＞
        {1: ['{0:7}'], 2: ['{0:7}', '{0:7}'], 3: ['{0:7}', '{0:7}', '{0:7}']}

        キー：表示される行に列が1つしかない場合，2つしかない場合，３つある場合を表す。
        値：.format()関数に使い，文字列を代入するためのテンプレート
            値にある0は .format()関数を使う際の位置引数の値
            値にある7は各列の幅を表す
        (注意) width=20は実行結果の7の計算に使われている。
    """

    # set width of each column
    col_width = ceil(width/col)

    # template for each column
    temp = ["{" + str(0) + ":" + str(col_width) + "}"]

    # create templates for rows
    # with one column, two columns, three columns,...
    template_dic = {}

    for i in range(1, col+1):

        template_dic[i] = temp * i

    return template_dic


def see(obj, col=4, width=70):
    """
    オブジェクトの属性（`_`もしくは`__`が付いた属性以外）を表示する

    引数：
        obj: 属性を調べるオブジェクト
        col: 表示する際の列の数（デフォルトは4）
        width: 表示の幅（デフォルトは70）
        　　　　　(列の幅は width/col 以上である最小整数となる)
    戻り値：
        None (表示のみ)


    例：整数型である100の属性を調べる。

       see(100)

       ＜実行結果＞
       .as_integer_ratio   .bit_count          .bit_length         .conjugate
       .denominator        .from_bytes         .imag               .numerator
       .real               .to_bytes
    """

    lst = [i for i in dir(obj) if i[0] != "_"]

    # create a list of lists
    new_lst = []
    for i in range(ceil(len(lst)/col)):
        new_lst.append(lst[i*col:i*col+col])

    # create templates for inserting texts
    template = _create_template(obj, col=col, width=width)

    # print each line of attributes
    for inner_lst in new_lst:

        num = len(inner_lst)

        # create a new inner list with inserted text
        inner_lst_new = []
        for idx, j in enumerate(template[num]):
            inner_lst_new.append(j.format("."+inner_lst[idx]))

        # create concatenated strings for a line to print
        line_str = ""
        for e in inner_lst_new:
            line_str += e+"  "

        print(line_str.strip())


# ===== Data-related function =================================================


def data(dataset=None, description=0):
    """|
       | 引数：
       |     dataset: (文字列)
       |         'bigmac': Big Macインデックス
       |         'debts'：政府負債に関する長期時系列データ
       |         'dates': 景気循環日付と拡張・後退期間
       |         'ex': 円/ドル為替レートなど
       |         'jpn-money': 日本の四半期データ（マネーストックなど）
       |         'jpn-q': 日本の四半期データ（GDPなど）
       |         'jpn-yr': 日本の年次データ（GDPなど）
       |         'mad': country data of Maddison Project Database 2020
       |         'mad-region': regional data of Maddison Project Database 2020
       |         'pwt': Penn World Table 10.01
       |         'weo': IMF World Economic Outlook 2024
       |         'world-money': 177ヵ国のマネーストックなど
       |
       |     description (デフォルト：0, 整数型):
       |         0: データのDataFrameを返す
       |            * 全てのデータセット
       |         1: 変数の定義を全て表示する
       |            * 全てのデータセット
       |         2: 変数の定義のDataFrameを返す
       |            * `'pwt'`，`'weo'`のみ
       |
       | 返り値：
       |     DataFrame もしくは DataFrameの表示
       |
       | 例１：py4macro.data('weo')
       |         -> IMF World Economic OutlookのDataFrameを返す。
       |
       | 例２：py4macro.data('weo', description=1)
       |         -> IMF World Economic Outlookの変数定義の全てを表示する。
       |
       | 例３：py4macro.data('weo', description=2)
       |         -> IMF World Economic Outlookの変数定義のDataFrameを返す。
       |
       |
       | ----- Penn World Tableについて -------------------------------------------
       |
       | PWTには以下の列が追加されている。
       |
       | * oecd：1990年代に始まった中央ヨーロッパへの拡大前にOECDメンバー国であれば1，そうでなければ0
       |
       | * income_group：世界銀行が所得水準に従って分けた４つのグループ
       |         High income
       |         Upper middle income
       |         Lower middle income
       |         Low income
       |
       | * region：世界銀行が国・地域に従って分けた７つのグループ化
       |         East Asia & Pacific
       |         Europe & Central Asia
       |         Latin America & Caribbean
       |         Middle East & North Africa
       |         North America
       |         South Asia
       |         Sub-Saharan Africa
       |
       | * continent：南極以外の6大陸
       |         Africa
       |         Asia
       |         Australia
       |         Europe
       |         North America
       |         South America"""

    if dataset not in ['pwt', 'weo', 'mad', 'mad-region', 'jpn-q', 'jpn-yr',
                       'jpn-money', 'world-money', 'ex', 'dates', 'bigmac', 'debts']:
        try:
            raise ValueError("""次の内１つを選んでください。
    'bigmac': Big Macインデックス
    'debts'：Historical Debts Data (Public Finances in Modern History)
    'dates': 景気循環日付など
    'ex': 円/ドル為替レートなど
    'jpn-money': 日本の四半期データ（マネーストックなど）
    'jpn-q': 日本の四半期データ（GDPなど）
    'jpn-yr': 日本の年次データ（GDPなど）
    'mad': country data of Maddison Project Database 2023
    'mad-region': regional data of Maddison Project Database 2023
    'pwt': Penn World Table 10.01
    'weo': IMF World Economic Outlook 2024
    'world-money': 177ヵ国のマネーストックなど""")
        except ValueError as e:
            print(e)



    # Penn World Table --------------------------------------------------------
    if (dataset == 'pwt') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'pwt_data.csv.bz2')
        return pd.read_csv(full_file_path, compression="bz2")

    elif (dataset == 'pwt') & (description == 1):
        full_file_path = _find_full_file_path(_get_path(__file__), 'pwt_definitions.csv')
        df = pd.read_csv(full_file_path
                        ).iloc[:, [0, 1]].dropna(subset=['Variable name']
                                                  ).set_index('Variable name')
        df.index.name = ''

        with pd.option_context('display.max_colwidth', None,
                               'display.max_rows', None):
            display(df)

    elif (dataset == 'pwt') & (description == 2):
        full_file_path = _find_full_file_path(_get_path(__file__), 'pwt_definitions.csv')
        df = pd.read_csv(full_file_path
                        ).iloc[:, [0, 1]].dropna(subset=['Variable name']
                                                  ).set_index('Variable name')
        df.index.name = ''

        return df

    elif (dataset == 'pwt') & (description not in [0, 1, 2]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示
    2: 変数の定義のDataFrame""")
        except ValueError as e:
            print(e)

    # IMF World Economic Outlook ----------------------------------------------
    elif (dataset == 'weo') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'weo.csv.bz2')
        return pd.read_csv(full_file_path, compression="bz2")

    elif (dataset == 'weo') & (description == 1):
        full_file_path = _find_full_file_path(_get_path(__file__), 'weo_description.csv.bz2')
        df = pd.read_csv(full_file_path,
                         compression="bz2").set_index("WEO Subject Code").sort_index()

        with pd.option_context('display.max_colwidth', None,
                               'display.max_rows', None):
            display(df)
    
    elif (dataset == 'weo') & (description == 2):
        full_file_path = _find_full_file_path(_get_path(__file__), 'weo_description.csv.bz2')
        df = pd.read_csv(full_file_path,
                         compression="bz2").set_index("WEO Subject Code").sort_index()
        return df

    elif (dataset == 'weo') & (description not in [0, 1, 2]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示
    2: 変数の定義のDataFrame""")
        except ValueError as e:
            print(e)

    # Maddison Project (Countries) --------------------------------------------
    elif (dataset == 'mad') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'mad_country.csv.bz2')
        return pd.read_csv(full_file_path,
                           compression="bz2", thousands=','
                           ).sort_values(['countrycode', 'year'])

    elif (dataset == 'mad') & (description == 1):
        print(mad_definitions)

    elif (dataset == 'mad') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示""")
        except ValueError as e:
            print(e)

    # Maddison Project (regionsional data) ----------------------------------------------
    elif (dataset == 'mad-region') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'mad_region.csv.bz2')
        return pd.read_csv(full_file_path,
                           compression="bz2", thousands=','
                           ).sort_values(['region', 'year'])

    elif (dataset == 'mad-region') & (description == 1):
        print(mad_definitions)

    elif (dataset == 'mad-region') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 日本の四半期データ（GDPなど）-------------------------------------------------------
    elif (dataset == 'jpn-q') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'jpn_quarterly.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='index',
                         parse_dates=True,
                         compression="bz2")
        df.index.name = ''
        return df

    elif (dataset == 'jpn-q') & (description == 1):
        print(jpn_q_definitions)

    elif (dataset == 'jpn-q') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 日本の年次データ（GDPなど）-------------------------------------------------------
    elif (dataset == 'jpn-yr') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'jpn_annual.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='index',
                         parse_dates=True,
                         compression="bz2")
        df.index.name = ''
        return df

    elif (dataset == 'jpn-yr') & (description == 1):
        print(jpn_yr_definitions)

    elif (dataset == 'jpn-yr') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 日本の四半期データ（マネーストックなど）-----------------------------------------
    elif (dataset == 'jpn-money') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'jpn_money.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='date', parse_dates=True, compression="bz2")
        df.index.name = ''
        return df

    elif (dataset == 'jpn-money') & (description == 1):
        print(jpn_money_definitions)

    elif (dataset == 'jpn-money') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 177ヵ国のマネーストックなど -----------------------------------------------------
    elif (dataset == 'world-money') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'world_money.csv.bz2')
        df = pd.read_csv(full_file_path,
                         compression="bz2")
        return df

    elif (dataset == 'world-money') & (description == 1):
        print(world_money_definitions)

    elif (dataset == 'world-money') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 円/ドル為替レートなど -----------------------------------------------------
    elif (dataset == 'ex') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'real_ex_rate.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='index',
                         parse_dates=True,
                         compression="bz2")
        df.index.name = ''
        return df

    elif (dataset == 'ex') & (description == 1):
        print(ex_definitions)

    elif (dataset == 'ex') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 景気循環日付など -----------------------------------------------------
    elif (dataset == 'dates') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'cycle_dates.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='index',
                         parse_dates=['tani1','yama','tani2'],
                         compression="bz2",
                         dtype={'expansion': 'Int64', 'contraction': 'Int64'})
        df.index.name = ''
        return df

    elif (dataset == 'dates') & (description == 1):
        print(dates_definitions)

    elif (dataset == 'dates') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # Big Mac Index -----------------------------------------------------
    elif (dataset == 'bigmac') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'bigmac.csv.bz2')
        df = pd.read_csv(full_file_path,
                         index_col='index',
                         compression="bz2",
                         dtype={'expansion': 'Int64', 'contraction': 'Int64'})
        df.index.name = ''
        return df

    elif (dataset == 'bigmac') & (description == 1):
        print(bigmac_definitions)

    elif (dataset == 'bigmac') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # Historical Delts --------------------------------------------------------
    elif (dataset == 'debts') & (description == 0):
        full_file_path = _find_full_file_path(_get_path(__file__), 'debts.csv.bz2')
        return pd.read_csv(full_file_path, compression="bz2")

    elif (dataset == 'debts') & (description == 1):
        print(debts_definitions)

    elif (dataset == 'debts') & (description not in [0, 1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示""")
        except ValueError as e:
            print(e)

    # Otherwise ---------------------------------------------------------------
    else:
        pass
