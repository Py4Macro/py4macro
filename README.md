[![PyPI version fury.io](https://badge.fury.io/py/py4macro.svg)](https://pypi.python.org/pypi/py4macro/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/py4macro)
[![CodeQL](https://github.com/Py4Macro/py4macro/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Py4Macro/py4macro/actions?query=workflow%codeql-analysis)


# はじめに

[Pythonで学ぶマクロ経済学 (中級＋レベル)](https://py4macro.github.io)で使うモジュール。

以下が含まれている。
* Hodrick-Prescottフィルターを使い時系列データのトレンドを返す`trend()`関数
* DataFrameを全て表示する`show()`関数
* `n`個の浮動小数点数から構成されるリストを返す`xvalues()`関数
* オブジェクトの属性（`_`もしくは`__`が付いた属性以外）を表示する`see()`関数
* 後退期間にグレーの塗りつぶしを追加する`fukyo()`関数
* 後退期間にグレーの塗りつぶしを追加する`recessions()`デコレーター
* データ・セット
    * Big Macインデックス
    * IMF World Economic Outlook 2024
    * Maddison Project Database 2023
    * Penn World Tables 10.01
    * 日本の四半期データ（GDPなど）
    * 日本の年次データ（GDPなど）
    * 日本の四半期データ（マネーストックなど）
    * 177ヵ国のマネーストックなど
    * 円/ドル為替レートなど
    * 景気循環日付と拡張・後退期間
    * 政府負債に関する長期時系列データ

# 使い方
```
import py4macro
```

## Hodrick-Prescottフィルターによるトレンド抽出
```
py4macro.trend(s,lamb=1600)
```
**引数**:

* `s`：`Series`もしくは１列の`DataFrame`とし，行のラベルは`DatetimeIndex`にすること。
* `lamb`: HPフィルターのlambda（デフォルトは四半期用のデータでは通常の値である1600としている）

**戻り値**:

Hodrick-Prescottフィルターで計算したtrend（トレンド）の`Series`


**例**:

`py4macro.trend(df.loc[:,'gdp'])`


## `DataFrame`の行・列を全て表示する
```
py4macro.show(df)
```
**引数**：
* `df`：`DataFrame`

**戻り値**：

`DataFrame`の表示のみ


## `n`個の数値から構成されるリストを作成する
```
py4macro.xvalues(l, h, n)
```
**引数**：
* `l`：最小値
* `h`：最大値
* `n`：要素数

**戻り値**：
* `n`個の浮動小数点数のリスト

**例**:

`py4macro.xvalues(-1, 1, 5)`

```
>>> [-1.0, -0.5, 0.0, 0.5, 1.0]
```

## オブジェクトの属性（`_`もしくは`__`が付いた属性以外）を表示する

`py4macro.see(obj, col=4, width=70)`

引数：
* `obj`: 属性を調べるオブジェクト
* `col`: 表示の列の数（デフォルトは4）
* `width`: 表示の幅（デフォルトは70）
    　　(列の幅は width/col 以上である最小整数となる)

戻り値：
* `None` (表示のみ)


例：整数型である100の属性を調べる。

`py4macro.see(100)`

```
>>> .as_integer_ratio   .bit_count       .bit_length      .conjugate
>>> .denominator        .from_bytes      .imag            .numerator
>>> .real               .to_bytes
```


## 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加する関数
* `fukyo()`関数は後退期間の塗りつぶしを追加する

```
py4macro.fukyo(ax, start=1980, end=2999, color='k', alpha='0.1')
```
**引数**：
* `ax`：`matplotlib`の軸
* `start`：`fukyo()`関数を適用し始める年（デフォルトは`1980`）
* `end`：`fukyo()`関数を適用し終わる年（デフォルトは`2999`）
* `color`：色（デフォルトは黒）
* `alpha`：透明度（デフォルトは`0.1`）

**戻り値**：
* なし（表示のみ）

<img height="350" src="figures/fukyo.jpg">


＜例１：一つの図＞
```
fig, ax = plt.subplots()
ax.plot(...)
fukyo(ax)
```

＜例２：一つの図＞
```
ax = <DataFrame もしくは Series>.plot()
fukyo(ax, start=1960, color='red')
```

＜例３：複数の図の中で一つだけに追加＞
```
fig, ax = plt.subplots(2,1)
ax[0].plot(...)
ax[1].plot(...)
fukyo(ax[0], start=1970, end=2005, color='grey', alpha=0.2)
```


## 横軸に`DatetimeIndex`を使うプロットに対して後退期間にグレーの塗りつぶしを追加するデコレーター
* `@py4macro.recessions()`は全ての軸に後退期間の塗りつぶしを追加する

```
@py4macro.recessions(start=1980, end=2900, color='k', alpha=0.1)
＜関数＞
```

**引数**：
* `start`：`fukyo()`関数を適用し始める年（デフォルトは`1980`）
* `end`：`fukyo()`関数を適用し終わる年（デフォルトは`2999`）
* `color`：色（デフォルトは黒）
* `alpha`：透明度（デフォルトは`0.1）


＜例１：一つの図をプロット（軸を返さない）＞
```
@py4macro.recessions()
def plot():
    <DataFrame もしくは Series>.plot()
```

＜例２：一つの図をプロット（軸を返す）＞
```
@py4macro.recessions(start=1960, color='red')
def plot():
    ax = <DataFrame もしくは Series>.plot()
    return ax
```

＜例３：一つの図をプロット＞
```
@py4macro.recessions(end=2000, alpha=0.9)
def plot():
    fig, ax = plt.subplots()
    ax.plot(...)
    return ax       # 省略すると軸を返さない
```

＜例４：複数の図をプロット＞
```
@py4macro.recessions(start=1975, color='green', alpha=0.2)
def plot():
    ax = <DataFrame>.plot(subplots=True, layout=(2,2))
    return ax       # この行は必須
```

＜例５：複数の図をプロット＞
```
@py4macro.recessions(start=1975, end=2010, color='grey', alpha=0.3)
def plot():
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(...)
    ax[1].plot(...)
    return ax       # この行は必須
```


## データ・セット

```
py4macro.data(dataset=None, description=0)
```

**引数**：

* `dataset`: (文字列)
    * `'bigmac'`: Big Macインデックス
    * `'debts'`: 政府負債に関する長期時系列データ
    * `'ex'`: 円/ドル為替レートなど
    * `'jpn-money'`: 日本の月次データ（CPIとマネーストック）
    * `'jpn-q'`: 日本の四半期データ（GDPなど）
    * `'mad'`:   country data of Maddison Project Database 2023
    * `'mad-region'`:   regional data of Maddison Project Database 2023
    * `'pwt'`:   Penn World Table 10.01
    * `'weo'`:   IMF World Economic Outlook 2024
    * `'world-money'`: 177ヵ国のマネーストックなど


* `description` (デフォルト：`0`, 整数型):
    * `0`: データのDataFrameを返す
        * 全てのデータセット
    * `1`: 変数の定義を全て表示する
        * 全てのデータセット
    * `2`: 変数の定義のDataFrameを返す
        * `'pwt'`，`'weo'`のみ

**返り値**：
    `DataFrame`もしくは`DataFrame`の表示


例１：IMF World Economic OutlookのDataFrameを返す

`py4macro.data('weo')`

例２：IMF World Economic Outlookの変数定義の全てを表示する

`py4macro.data('weo',description=1)`

例３：IMF World Economic Outlookの変数定義のDataFrameを返す

`py4macro.data('weo',description=2)`


# インストール方法
```
pip install py4macro
```
or
```
pip install git+https://github.com/Py4Macro/py4macro.git
```
or
```
git clone https://github.com/Py4Macro/py4macro.git
cd py4macro
pip install .
```
