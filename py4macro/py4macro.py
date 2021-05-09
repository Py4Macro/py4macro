"""Module for 「Pythonで学ぶ中級マクロ経済学」
    * HPフィルター関数
    * データ・セット
        * Penn World Tables 10.0
        * IMF World Economic Outlook 2021
        * Maddison Project Database 2020
"""
from os.path import abspath, join, split
import pandas as pd


# =============================================================================================

def trend(s, lamb=1600):
    """
    Parameter（引数）:
        s: Seriesもしくは１列のDataFrameとし，行のラベルはDatetimeIndexとすること。
        lamb: 四半期用のデータでは通常の値（デフォルト：1600）
    
    return（返り値）:
        Hodrick-Prescott filterで計算したtrend（トレンド）のSeries


    例: trend_cycle(df.loc[:,'gdp'])
    """
    from statsmodels.tsa.filters.hp_filter import hpfilter
    
    return hpfilter(s.dropna(), lamb=lamb)[1]


# =============================================================================================

def _get_path(f):
    return split(abspath(f))[0]


mad_definitions="""\
gdppc:   Real GDP per capita in 2011$
pop:     Population, mid-year (thousands)"""


def data(dataset=None, description=False, estimates=False):
    """
    引数：
        dataset:
            'pwt':   Penn World Table 10.0
            'weo':   IMF World Economic Outlook 2021
            'mad':   country data of Maddison Project Database 2020
            'mad-regions':   regional data of Maddison Project Database 2020

        description (デフォルト：False):
            True: 変数の定義を表示する。

        estimates (デフォルト：False):
            (dataset='weo'場合のみ有効になる)
            True:   'weo'には変数の予測値が含まれるが，何年以降から予測値なのかを示す

    返り値：
        dataset='weo' 以外の場合：
            description=False の場合は DataFrame
            description=True の場合は変数の定義のDataFrame

        dataset='weo' の場合：
            description=False, estimates=False の場合は DataFrame
            description=True, estimates=False の場合は変数の定義のDataFrame
            description=False, estimates=True の場合は変数の推定値の開始年のDataFrame

    例１：py4macro.data('pwt')はPenn World TableのDataFrameを返す。
    例２：py4macro.data('pwt',description=True)はPenn World Tableの変数定義のDataFrameを返す。
    例３：py4macro.data('weo',description=True)はIMF World Economic Outlookの変数定義のDataFrameを返す。
    例４：py4macro.data('weo',estimates=True)はIMF World Economic Outlookの変数の推定値の開始年のDataFrameを返す。
    """

    if dataset == None:
        raise ValueError("""次の内１つを選んでください。
            'pwt': Penn World Table 10.0
            'weo': IMF World Economic Outlook 2021
            'mad': country data of Maddison Project Database 2020
            'mad-regions': regional data of Maddison Project Database 2020""")

    # Penn World Table ----------------------------------------------------------------------
    elif (dataset=='pwt') & (description==False):
        return pd.read_csv(join(_get_path(__file__), "data/pwt_data.csv.bz2"), compression="bz2")

    elif (dataset=='pwt') & (description==True):
        df = pd.read_csv('pwt_definitions.csv').iloc[:,[0,1]].dropna(subset=['Variable name']).set_index('Variable name')
        df.index.name = ''
        with pd.option_context('display.max_colwidth', None) and pd.option_context('display.max_rows', None):
            display(df)

    # IMF World Economic Outlook ------------------------------------------------------------
    elif (dataset=='weo') & (description==False) & (estimates==False):
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

    elif (dataset=='weo') & (description==True) & (estimates==False):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"), compression="bz2")
        jp = df.query('Country=="Japan"').iloc[:,[2,4,5,6,7]].set_index('WEO Subject Code')
        jp.index.name = ''
        with pd.option_context('display.max_colwidth', None) and pd.option_context('display.max_rows', None):
            display(jp)

    elif (dataset=='weo') & (description==False) & (estimates==True):
        df = pd.read_csv(join(_get_path(__file__), "data/WEOApr2021all.csv.bz2"),
                         compression="bz2", thousands=',', na_values='--')
        df = df.iloc[:,[1,2,3,-1]].dropna()
        # with pd.option_context('display.max_colwidth', None) and pd.option_context('display.max_rows', None):
            # display(df)
        return df

    elif (dataset=='weo') & (description==True) & (estimates==True):
        raise ValueError("""次の引数のどちらかをFalseにしてください。
            * description
            * estimates""")

    # Maddison Project (Countries) -----------------------------------------------------------
    elif (dataset=='mad') & (description==False):
        return pd.read_csv(join(_get_path(__file__), "data/mad_country.csv.bz2"),
                           compression="bz2", thousands=',').sort_values(['countrycode','year'])

    elif (dataset=='mad') & (description==True):
        print(mad_definitions)

    # Maddison Project (Regions) -------------------------------------------------------------
    elif (dataset=='mad-regions') & (description==False):
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

    elif (dataset=='mad-regions') & (description==True):
        print(mad_definitions)

    else:
        pass
