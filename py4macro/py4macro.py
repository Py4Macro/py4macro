from os.path import abspath, join, split
import pandas as pd


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
    |
    | ＜出典＞
    | GDPとその構成要素
    |    * 1994年Q1~2019年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 2011暦年（平成23年）連鎖価格
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |    * 1980年Q1~1993年Q4
    |        * 実額・四半期・実質季節調整系列（年換算）
    |        * 平成23年基準支出側GDP系列簡易遡及（参考系列であり上のデータと接続可能）
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | 実質資本ストック
    |   * 1994年Q1~2019年Q4
    |        * 平成23年基準
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |   * 1980年Q1~1993年Q4
    |        * 平成23年基準遡及系列
    |        * 単位：10億円
    |        * 国民経済計算（GDP統計）
    |
    | 就業者数，失業者数，失業率
    |   * 総務省「労働力調査」
    |   * 単位：万人
    |
    | 労働者一人当たり月平均労働時間
    |   * 厚生労働省「毎月勤労統計調査」
    |   * 30 人以上(一般・パート)、月間実労働時間(総実労働時間)
    |   * 2015年の平均を100に基準化
    |
    | インフレ率
    |   * 景気動向指数（速報、改訂値）（月次）から計算"""

jpn_money_definitions="""
    | `cpi`: 消費者物価指数
    | `money`: マネーストック（M1）
    |
    | * 行ラベル：四半期の最終日
    |
    | ＜出典＞
    | International Monetary Fund"""

world_money_definitions="""
    | `iso`: ISO国名コード
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
    | ＜注意点＞
    | * `money`と`deflator`が10年間以上連続で欠損値がない経済（177ヵ国）のみが含まれている。
    | * 国によって含まれるデータの`year`が異なる。
    | * 所得グループに関する情報
    |   https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
    |
    | ＜出典＞
    | World Bank Development Indicators"""

# ===== Helper functions =======================================================================

def _get_path(f):
    return split(abspath(f))[0]


def _mad_definitions():

    df = pd.read_csv(join(_get_path(__file__), "data/mad_definitions.csv")).iloc[[16,17,18],[0,1]]
    df.columns = ['vars','Definitions']
    df = df.set_index('vars')
    df.index.name = ''

    return df


# ===== Main functions ==========================================================================

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



def data(dataset=None, description=0):
    """|
       | 引数：
       |     dataset: (文字列)
       |         'pwt':   Penn World Table 10.0
       |         'weo':   IMF World Economic Outlook 2021
       |         'mad':   country data of Maddison Project Database 2020
       |         'mad-regions':   regional data of Maddison Project Database 2020
       |         'jpn-q': 日本の四半期データ（GDPなど）
       |         'jpn-money': 日本の四半期データ（マネーストックなど）
       |         'world-money': 177ヵ国のマネーストックなど
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
       | * region：南極以外の6大陸
       |         Africa
       |         Asia
       |         Australia
       |         Europe
       |         North America
       |         South America"""


    if dataset not in ['pwt','weo','mad','mad-regions','jpn-q','jpn-money','world-money']:
        try:
            raise ValueError("""次の内１つを選んでください。
    'pwt': Penn World Table 10.0
    'weo': IMF World Economic Outlook 2021
    'mad': country data of Maddison Project Database 2020
    'mad-regions': regional data of Maddison Project Database 2020
    'jpn-q': 日本の四半期データ（GDPなど）
    'jpn-money': 日本の四半期データ（マネーストックなど）
    'world-money': 177ヵ国のマネーストックなど""")
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

    # Otherwise ------------------------------------------------------------------------
    else:
        pass
