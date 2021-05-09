# はじめに

[「Pythonで学ぶ中級マクロ経済学」](https://py4macro.github.io)で使うモジュール。

以下が含まれている。
* Hodrick-Prescottフィルターを使い時系列データのトレンドを返す関数
* ３つのデータ・セット
    * Penn World Tables 10.0
    * IMF World Economic Outlook 2021
    * Maddison Project Database 2020

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
* lamb: HPフィルターのlambda（デフォルトは四半期用のデータでは通常の値である1600としている）

**返り値**:

Hodrick-Prescottフィルターで計算したtrend（トレンド）の`Series`


**例**:

`py4macro.trend(df.loc[:,'gdp'])`

## ３つのデータ・セット

```
py4macro.data(dataset=None, description=False, estimates=False)
```

**引数**：

1. `dataset` (文字列):
    * `'pwt'`:   Penn World Table 10.0
    * `'weo'`:   IMF World Economic Outlook 2021
    * `'mad'`:   country data of Maddison Project Database 2020
    * `'mad-regions'`:   regional data of Maddison Project Database 2020

1. `description` (デフォルト：`False`):
    * `True`: 変数の定義を表示する。

1. `estimates` (デフォルト：`False`):
    * (`dataset='weo'`場合のみ有効になる)
    * `True`: `weo`には変数の予測値が含まれるが，予測値の開始年を示す。


**返り値**：

* `dataset='weo'` 以外の場合：
    * `description=False` の場合は `DataFrame`
    * `description=True` の場合は変数の定義の`DataFrame`

* `dataset='weo'` の場合：
    * `description=False`, `estimates=False` の場合は `DataFrame`
    * `description=True`, `estimates=False` の場合は変数の定義の`DataFrame`
    * `description=False`, `estimates=True` の場合は変数の推定値の開始年の`DataFrame`


**例１**：Penn World Tableの`DataFrame`を返す。

`py4macro.data('pwt')`


**例２**：Penn World Tableの変数の定義の`DataFrame`を返す。

`py4macro.data('pwt',description=True)`


**例３**：IMF World Economic Outlookの`DataFrame`を返す。

`py4macro.data('weo')`

**例４**：IMF World Economic Outlookの変数の定義の`DataFrame`を返す。

`py4macro.data('weo',description=True)`


**例５**：IMF World Economic Outlookの変数の推定値の開始年の`DataFrame`を返す。

`py4macro.data('weo',estimates=True)`


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
