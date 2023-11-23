import functools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os.path import abspath, join, split


# ===== Definitions =========================================================================

jpn_q_definitions="""
    | `gdp`: 国内総生産（GDP）
    | `consumption`: 消費
    | `investment`: 投資
    | `government`: 政府支出
    | `exports`: 輸出
    | `imports`: 輸入
    | `capital`: 資本ストック
    | `employed`: 就業者数
    | `unemployed`: 失業者数
    | `unemployment_rate`: 失業率
    | `hours`: 労働者一人当たり月平均労働時間
    | `total_hours`: 月平均総労働時間（`employed`X`hours`）
    | `inflation`: インフレ率
    | `price`: 消費者物価指数
    | `deflator`: GDPデフレーター
    |
    | * 四半期データ
    |
    | ＜出典＞
    | GDPとその構成要素
    |    * 1994年Q1~2021年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 2015暦年（平成27年）連鎖価格
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |    * 1980年Q1~1993年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 平成27年基準支出側GDP系列簡易遡及（参考系列であり上のデータと接続可能）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | 実質資本ストック
    |   * 1994年Q1~2019年Q4
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
    |   * 景気動向指数（速報，改訂値，月次，原数値の前年同月比）から四半期平均として計算
    |
    | 消費者物価指数
    |   * 2020年基準
    |   * 「中分類指数（全国）＜時系列表＞【月次】」の四半期平均として計算
    |   * 簡便的に移動平均を使い季節調整を施している
    |
    | GDPデフレーター
    |   * 1994年Q1~2019年Q4
    |       * 2015年（平成27年）基準
    |       * 季節調整系列
    |   * 1980年Q1~1993年Q4
    |       * 2015年（平成27年）基準遡及系列
    |       * 季節調整系列"""

jpn_money_definitions="""
    | `cpi`: 消費者物価指数
    |   * 2015年の値を`100`
    |   * 季節調整済み
    | `money`: マネーストック（M1）
    |   * 2015年の値を`100`
    |   * 季節調整済み
    |
    | * 月次データ
    | * 1955年1月〜2021年12月
    | * 行ラベル：毎月の最終日
    |
    | ＜出典＞
    | OECD Main Economic Indicators"""

world_money_definitions="""
    | `iso`: ISO国コード
    | `country`: 国名
    | `year`: 年
    | `income_group`: 世界銀行が定義する所得グループ
    |   * High income
    |   * Upper Middle income
    |   * Lower Middle income
    |   * Low income
    | `money`: マネーストック（M1）
    | `deflator`: GDPディフレーター
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


ex_definitions="""
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

dates_definitions="""
    | `tani1`: １つの循環における第１の谷
    | `yama`:  １つの循環における山
    | `tani2`: １つの循環における第２の谷
    | `expansion`: 拡張期の期間（単位：月）
    |              `tani1`から`yama`までの期間 
    | `contraction`: 後退期の期間（単位：月）
    |                `yama`から`tani2`までの期間 
    |
    | ＜出典＞
    |   * 内閣府
    |   * https://www.esri.cao.go.jp/jp/stat/di/hiduke.html"""

bigmac_definitions="""
    | `year`: 年（2000年〜2023年）
    | `country`: 国名
    | `iso`: ISO国コード
    | `currency_code`: 通貨コード
    | `price_local`: Big Macの価格（自国通貨単位）
    | `exr`: 名目為替レート（自国通貨単位/米ドル）
    | `gdppc_local`: 名目一人当たりGDP（自国通貨単位）
    |
    | * 年次データ
    |
    | ＜出典＞
    | https://github.com/TheEconomist/big-mac-data (Copyright The Economist)"""

# ===== Helper functions =======================================================================

def _get_path(f):
    return split(abspath(f))[0]


def _mad_definitions():

    df = pd.read_csv(join(_get_path(__file__), "data/mad_definitions.csv")).iloc[[16,17,18],[0,1]]
    df.columns = ['vars','Definitions']
    df = df.set_index('vars')
    df.index.name = ''

    return df


# ===== Non-data-related functions ==========================================================================

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

    with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
        display(df)


def xvalues(l, h, n):
    """引数
        l：最小値（lowest value）
        h：最大値（highest value）
        n：作成する数値の数を指定する（正の整数型，number of values）
    戻り値
        n個の要素から構成されるリスト"""
    
    if ( n<=1 ) or ( not isinstance(n, int) ):
        raise Exception(f"引数 n には2以上の整数型を使う必要があります。n={n}となっています。")
    elif l>=h:
        raise Exception(f"引数 l と h の値では l>h もしくは l=h となります。l<h となるように値を設定し直してください。")
    else:
        return [l + x*(h-l)/(n-1) for x in range(n)]



def fukyo(ax, color='k', alpha=0.1):
    """
    * 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加する関数
    * `@py4macro.recessions`デコレーターとの違い
        * `@py4macro.recessions`は全ての図に塗りつぶしを追加する
        * `fukyo()`関数は個々の軸に塗りつぶしを追加する

    引数：
        ax：`matplotlib`の軸
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
    fukyo(ax, color='red')

    ＜例３：複数の図の中で一つだけに追加＞
    fig, ax = plt.subplots(2,1)
    ax[0].plot(...)
    ax[1].plot(...)
    fukyo(ax[0], color='grey', alpha=0.2)
    """
    
    df = pd.read_csv(join(_get_path(__file__), "data/cycle_dates.csv.bz2"), index_col='index', parse_dates=True, compression="bz2", dtype={'expansion':'Int64','contraction':'Int64'})
    
    for i in df.index[8:]:
        start = df.loc[i,'yama']
        end = df.loc[i,'tani2']
        ax.axvspan(start, end, fill=True, linewidth=0, color=color, alpha=alpha)
    # return ax     



# ===== Decorator ==========================================================================

def recessions(color='k', alpha=0.1):
    """
    * 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加するデコレーター
    * `fukyo()`関数との違い
        * `@py4macro.recessions`は全ての図に塗りつぶしを追加する
        * `fukyo()`関数は個々の軸に塗りつぶしを追加する

    引数：
        color：色（デフォルトは黒）
        alpha：透明度（デフォルトは`0.1）

    戻り値
        funcが返す軸を返す

    ＜例１：一つの図をプロット（軸を返さない）＞
    @py4macro.recessions()
    def plot():
        <DataFrame もしくは Series>.plot()

    ＜例２：一つの図をプロット（軸を返す）＞
    @py4macro.recessions(color='r')
    def plot():
        ax = <DataFrame もしくは Series>.plot()
        return ax

    ＜例３：一つの図をプロット＞
    @py4macro.recessions(alpha=0.5)
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
    @py4macro.recessions(color='grey', alpha=0.1)
    def plot():
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(...)
        ax[1].plot(...)
        return ax       # この行は必須"""
    
    df = pd.read_csv(join(_get_path(__file__), "data/cycle_dates.csv.bz2"), index_col='index', parse_dates=True, compression="bz2", dtype={'expansion':'Int64','contraction':'Int64'})

    def _recessions(func):
    
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            ax = func(*args, **kwargs)
            
            # 図が一つの場合，軸はそのまま返される
            if not isinstance(ax, np.ndarray):
                for i in df.index[8:]:
                    start = df.loc[i,'yama']
                    end = df.loc[i,'tani2']
                    plt.axvspan(start, end, fill=True, linewidth=0, color=color, alpha=alpha)
                return ax     

            # 図が複数の場合，軸はarrayとして返される
            # DataFrame.plot()で縦に並べる場合，軸は１次元配列となる
            elif ax.ndim == 1:
                n = len(ax)
                for r in range(n):
                    for i in df.index[8:]:
                        start = df.loc[i,'yama']
                        end = df.loc[i,'tani2']
                        ax[r].axvspan(start, end, fill=True, linewidth=0, color=color, alpha=alpha)
                return ax     

            # 軸のarrayが2次元配列となる場合
            elif ax.ndim > 1:
                row = ax.shape[0]
                col = ax.shape[1]
                for r in range(row):
                    for c in range(col):
                        for i in df.index[8:]:
                            start = df.loc[i,'yama']
                            end = df.loc[i,'tani2']
                            ax[r,c].axvspan(start, end, fill=True, linewidth=0, color=color, alpha=alpha)
                return ax     

        return wrapper

    return _recessions


# ===== Data-related function ==========================================================================

def data(dataset=None, description=0):
    """|
       | 引数：
       |     dataset: (文字列)
       |         'pwt':   Penn World Table 10.01
       |         'weo':   IMF World Economic Outlook 2021
       |         'mad':   country data of Maddison Project Database 2020
       |         'mad-regions':   regional data of Maddison Project Database 2020
       |         'jpn-q': 日本の四半期データ（GDPなど）
       |         'jpn-money': 日本の四半期データ（マネーストックなど）
       |         'world-money': 177ヵ国のマネーストックなど
       |         'ex': 円/ドル為替レートなど
       |         'dates': 景気循環日付と拡張・後退期間
       |         'bigmac': Big Macインデックス
       |
       |     description (デフォルト：0, 整数型):
       |         0: データのDataFrameを返す
       |            * 全てのデータセット
       |         1: 変数の定義を全て表示する
       |            * 全てのデータセット
       |         2: 変数の定義のDataFrameを返す
       |            * `'pwt'`，`'weo'``'mad'`のみ
       |        -1: 何年以降から予測値なのかを全て示す
       |            * `'weo'`のみ
       |        -2: 何年以降から予測値なのかを示すDataFrameを返す
       |            * `'weo'`のみ
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
       | 例４：py4macro.data('weo', description=-1)
       |         -> IMF World Economic Outlookの変数の推定値の開始年を全て表示する。
       |
       | 例５：py4macro.data('weo', description=-2)
       |         -> IMF World Economic Outlookの変数の推定値の開始年のDataFrameを返す。
       |
       |
       | ----- Penn World Tableについて ---------------------------------------------
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


    if dataset not in ['pwt','weo','mad','mad-regions','jpn-q','jpn-money','world-money','ex','dates','bigmac']:
        try:
            raise ValueError("""次の内１つを選んでください。
    'pwt': Penn World Table 10.01
    'weo': IMF World Economic Outlook 2021
    'mad': country data of Maddison Project Database 2020
    'mad-regions': regional data of Maddison Project Database 2020
    'jpn-q': 日本の四半期データ（GDPなど）
    'jpn-money': 日本の四半期データ（マネーストックなど）
    'world-money': 177ヵ国のマネーストックなど
    'ex': 円/ドル為替レートなど
    'dates': 景気循環日付など
    'bigmac': Big Macインデックス""")
        except ValueError as e:
            print(e)

    # Penn World Table ----------------------------------------------------------------------
    elif (dataset=='pwt') & (description==0):
        return pd.read_csv(join(_get_path(__file__), "data/pwt_data.csv.bz2"), compression="bz2")


    elif (dataset=='pwt') & (description==1):
        df = pd.read_csv(join(_get_path(__file__), "data/pwt_definitions.csv")
                ).iloc[:,[0,1]].dropna(subset=['Variable name']).set_index('Variable name')
        df.index.name = ''

        with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
            display(df)


    elif (dataset=='pwt') & (description==2):
        df = pd.read_csv(join(_get_path(__file__), "data/pwt_definitions.csv")
                ).iloc[:,[0,1]].dropna(subset=['Variable name']).set_index('Variable name')
        df.index.name = ''

        return df


    elif (dataset=='pwt') & (description not in [0,1,2]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示
    2: 変数の定義のDataFrame""")
        except ValueError as e:
            print(e)


    # IMF World Economic Outlook ------------------------------------------------------------
    elif (dataset=='weo') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"),
                         compression="bz2", thousands=',', na_values='--')
        df = df.dropna(subset=['ISO']).pivot(index=['ISO','Country'],
                                             columns='WEO Subject Code',
                                             values=[str(x) for x in range(1980,2027)]
                                            ).stack(level=0
                                                   ).reset_index().rename(columns={'level_2':'year',
                                                                                           'Country':'country',
                                                                                           'ISO':'countrycode'}
                                                                         ).sort_values(['countrycode','year'])
        df.columns.name = ''
        df['year'] = df['year'].astype(int)

        return df


    elif (dataset=='weo') & (description==1):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"), compression="bz2")
        jp = df.query('Country=="Japan"').iloc[:,[2,4,5,6,7]].set_index('WEO Subject Code').sort_index()
        jp.index.name = ''
        jp = jp.rename(columns = {i:i.upper() for i in df.columns})

        with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
            display(jp)


    elif (dataset=='weo') & (description==2):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"), compression="bz2")
        jp = df.query('Country=="Japan"').iloc[:,[2,4,5,6,7]].set_index('WEO Subject Code').sort_index()
        jp.index.name = ''
        jp = jp.rename(columns = {i:i.upper() for i in df.columns})

        return jp


    elif (dataset=='weo') & (description==-1):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"),
                         compression="bz2", thousands=',', na_values='--')
        df = df.iloc[:,[1,2,3,-1]].dropna()

        with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
            display(df)


    elif (dataset=='weo') & (description==-2):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"),
                         compression="bz2", thousands=',', na_values='--')
        df = df.iloc[:,[1,2,3,-1]].dropna()

        return df


    elif (dataset=='weo') & (description not in [-2,-1,0,1,2]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示
    2: 変数の定義のDataFrame
   -1: 変数の推定値の開始年の表示
   -2: 変数の推定値の開始年のDataFrame""")
        except ValueError as e:
            print(e)

    # Maddison Project (Countries) -----------------------------------------------------------
    elif (dataset=='mad') & (description==0):
        return pd.read_csv(join(_get_path(__file__), "data/mad_country.csv.bz2"),
                           compression="bz2", thousands=',').sort_values(['countrycode','year'])


    elif (dataset=='mad') & (description==1):
        return _mad_definitions()


    elif (dataset=='mad') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame (デフォルト)
    1: 変数の定義を全て表示""")
        except ValueError as e:
            print(e)

    # Maddison Project (Regions) -------------------------------------------------------------
    elif (dataset=='mad-regions') & (description==0):

        # GDPpc DataFrame
        df_gdppc = pd.read_csv(join(_get_path(__file__), "data/mad_regions.csv"),
                               thousands=',', skiprows=[0,2], usecols=list(range(9))+[18])
        df_gdppc = pd.melt(df_gdppc, id_vars=['Region'], value_vars=df_gdppc.columns[1:])
        df_gdppc = df_gdppc.rename(columns={'Region':'year','variable':'regions', 'value':'gdppc'})

        # # Population DataFrame
        df_pop = pd.read_csv(join(_get_path(__file__), "data/mad_regions.csv"),
                             thousands=',', skiprows=[0,2], usecols=[0]+list(range(9,18)))
        df_pop.columns = df_pop.columns.str.replace('.1','', regex=False)
        df_pop = pd.melt(df_pop, id_vars=['Region'], value_vars=df_pop.columns[1:])
        df_pop = df_pop.rename(columns={'Region':'year', 'variable':'regions', 'value':'pop'})

        # merge
        df = pd.merge(df_gdppc, df_pop, left_on=['regions','year'], right_on=['regions','year'])

        return df.iloc[:,[1,0,2,3]].sort_values(['regions','year'])


    elif (dataset=='mad-regions') & (description==1):
        return _mad_definitions()


    elif (dataset=='mad-regions') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 日本の四半期データ（GDPなど）-------------------------------------------------------
    elif (dataset=='jpn-q') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/jpn_quarterly.csv.bz2"), index_col='index', parse_dates=True, compression="bz2")
        df.index.name = ''
        return df

    elif (dataset=='jpn-q') & (description==1):
        print(jpn_q_definitions)

    elif (dataset=='jpn-q') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 日本の四半期データ（マネーストックなど）-----------------------------------------
    elif (dataset=='jpn-money') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/jpn_money.csv.bz2"), index_col='date', parse_dates=True, compression="bz2")
        df.index.name = ''
        return df

    elif (dataset=='jpn-money') & (description==1):
        print(jpn_money_definitions)

    elif (dataset=='jpn-money') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 177ヵ国のマネーストックなど -----------------------------------------------------
    elif (dataset=='world-money') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/world_money.csv.bz2"), compression="bz2")
        return df

    elif (dataset=='world-money') & (description==1):
        print(world_money_definitions)

    elif (dataset=='world-money') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 円/ドル為替レートなど -----------------------------------------------------
    elif (dataset=='ex') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/real_ex_rate.csv.bz2"), index_col='index', parse_dates=True, compression="bz2")
        df.index.name = ''
        return df

    elif (dataset=='ex') & (description==1):
        print(ex_definitions)

    elif (dataset=='ex') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # 景気循環日付など -----------------------------------------------------
    elif (dataset=='dates') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/cycle_dates.csv.bz2"), index_col='index', parse_dates=True, compression="bz2", dtype={'expansion':'Int64','contraction':'Int64'})
        df.index.name = ''
        return df

    elif (dataset=='dates') & (description==1):
        print(dates_definitions)

    elif (dataset=='dates') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # Big Mac Index -----------------------------------------------------
    elif (dataset=='bigmac') & (description==0):
        df = pd.read_csv(join(_get_path(__file__), "data/bigmac.csv.bz2"), index_col='index', compression="bz2", dtype={'expansion':'Int64','contraction':'Int64'})
        df.index.name = ''
        return df

    elif (dataset=='bigmac') & (description==1):
        print(bigmac_definitions)

    elif (dataset=='bigmac') & (description not in [0,1]):
        try:
            raise ValueError("""descriptionに次の内１つを選んでください。
    0: データのDataFrame
    1: 変数の定義を表示""")
        except ValueError as e:
            print(e)

    # Otherwise ------------------------------------------------------------------------
    else:
        pass
