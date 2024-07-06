v0.8.10, 2024-07-6
* `weo`の変数の説明をアルファベット順に変更
* `debts`の変数の説明を更新

v0.8.9, 2024-07-5
* `mad-regions`を`mad-region`に変更
* `mad`と`mad-region`のデータを更新
* `bigmac`を2024年1月1日のデータまでに更新
* `ex`を更新
* `weo`をWEO2024に更新
* `weo`の引数`description=-1`と`description=-2`は廃止
* `jpn-q`を2023年Q4のデータまでに更新
* 四半期データの`DatetimeIndex`は四半期の最初の日に変更
* `fukyo()`関数とデコレーターに引数`start`と`end`を追加
* 新たなデータセット`debts`を追加

v0.8.8, 2024-01-08
* `see`関数を追加

v0.8.7, 2023-11-23
* `bigmac`に2023年データを追加

v0.8.6, 2023-07-01
* `bigmac`の変数を一新

v0.8.5, 2023-05-25
* Penn World Table 10.01にアップデート
* Big Mac インデックスを追加

v0.8.4, 2023-01-17
* データの定義・出典を加筆・修正

v0.8.3, 2022-11-19
* `fukyo()`関数と`@py4macro.recessions()`デコレーターで表示される後退期間のグレーの塗りつぶしの枠を削除
* `__init__.py`のバージョン番号の修正

v0.8.2, 2022-11-16
* 後退期間にグレーの塗りつぶしを追加する`fukyo()`関数を追加
* `@py4macro.recessions()`デコレーターに引数を追加

v0.8.1, 2022-11-13
* 景気循環日付と拡張・後退期間のデータを追加
* 後退期間にグレーの塗りつぶしを追加するデコレーター`@py4macro.recessions`を追加
* `jpn-q`から`recession_start`と`recession_end`を削除

v0.8.0, 2022-11-12
* `jpn-q`のデータに景気循環日付（四半期）`recession_start`と`recession_end`を追加
* `xvalues()`関数を追加

v0.7.0, 2022-05-24
* `jpn-q`のデータに`price`と`deflator`を追加

v0.6.1, 2022-05-24
* `jpn-money`のデータを2021年12月まで拡張，データの説明を修正

v0.6.0, 2022-05-21
* `jpn-q`のデータを2021年第四半期まで拡張

v0.5.2, 2021-09-03
* `weo`の`year`を整数型に修正

v0.5.1, 2021-07-21
* `install_requires` の変更

v0.5.0, 2021-06-27
* 円/ドル為替レートなどを追加

v0.4.0, 2021-06-16
* 日本の四半期データ（マネーストックなど）と177ヵ国のマネーストックなどのデータを追加

v0.3.1, 2021-06-03
* 日本の四半期データ（GDPなど）を追加

v0.2.1, 2021-05-21
* Column names, added to the original PWT, are changed

v0.2.0, 2021-05-10
* DataFrameを全て表示する`show()`関数, 
* 変数の定義の`DataFrame`
* Penn World Table is combined with regions, income groups, etc

v0.1.4, 2021-05-09
* bug fixed (pwt-definitions.csv not found).

v0.1.3, 2021-05-09
* Github Action test.

v0.1.2, 2021-05-09
* Github Action test.

v0.1.1, 2021-05-09
* Initial release.
