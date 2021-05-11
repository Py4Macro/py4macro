from os.path import abspath, join, split
import pandas as pd


# =============================================================================================

def trend(s, lamb=1600):
    """trend関数の説明

        引数:
            s: Seriesもしくは１列のDataFrameとし，行のラベルはDatetimeIndexとすること。
            lamb: 四半期用のデータでは通常の値（デフォルト：1600）

        返り値:
            Hodrick-Prescott filterで計算したtrend（トレンド）のSeries

        例: trend(df.loc[:,'gdp'])"""

    from statsmodels.tsa.filters.hp_filter import hpfilter

    return hpfilter(s.dropna(), lamb=lamb)[1]



def show(df):
    """show関数の説明

        引数：DetaFrame
        戻り値：行・列ともに全て表示する。"""

    with pd.option_context('display.max_colwidth', None, 'display.max_rows', None):
        display(df)


# =============================================================================================

def _get_path(f):
    return split(abspath(f))[0]


def _mad_definitions():

    df = pd.read_csv(join(_get_path(__file__), "data/mad_definitions.csv")).iloc[[16,17,18],[0,1]]
    df.columns = ['vars','Definitions']
    df = df.set_index('vars')
    df.index.name = ''

    return df



def data(dataset=None, description=0):
    """data関数の説明
        引数：
            dataset: (文字列)
                'pwt':   Penn World Table 10.0
                'weo':   IMF World Economic Outlook 2021
                'mad':   country data of Maddison Project Database 2020
                'mad-regions':   regional data of Maddison Project Database 2020

            description (デフォルト：0, 整数型):
                0: データのDataFrameを返す
                1: 変数の定義を全て表示する
                2: 変数の定義のDataFrameを返す
               -1: 何年以降から予測値なのかを全て示す(dataset='weo'場合にのみ有効)
               -2: 何年以降から予測値なのかを示すDataFrameを返す(dataset='weo'場合にのみ有効)

        返り値：
            DataFrame もしくは DataFrameの表示

        例１：py4macro.data('weo')
                -> IMF World Economic OutlookのDataFrameを返す。

        例２：py4macro.data('weo', description=1)
                -> IMF World Economic Outlookの変数定義の全てを表示する。

        例３：py4macro.data('weo', description=2)
                -> IMF World Economic Outlookの変数定義のDataFrameを返す。

        例４：py4macro.data('weo', description=-1)
                -> IMF World Economic Outlookの変数の推定値の開始年を全て表示する。

        例５：py4macro.data('weo', description=-2)
                -> IMF World Economic Outlookの変数の推定値の開始年のDataFrameを返す。"""


    if dataset not in ['pwt','weo','mad','mad-regions']:
        try:
            raise ValueError("""次の内１つを選んでください。
    'pwt': Penn World Table 10.0
    'weo': IMF World Economic Outlook 2021
    'mad': country data of Maddison Project Database 2020
    'mad-regions': regional data of Maddison Project Database 2020""")
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

    else:
        pass
