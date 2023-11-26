import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate 
import japanize_matplotlib
plt.rcParams['font.size'] = 15 # グラフの基本フォントサイズの設定

import datetime
now = datetime.datetime.now()
now = now.strftime("%y%m%d")

# テキストファイルをpandasデータフレーム形式で読み込む
# 区切り文字はsepで指定できる。例えば、タブ区切りの場合はsep='\t'と記述する
DF = pd.read_csv('231126_test.csv', sep=',', encoding="utf-8")


# 抽出データの列名
x_name = 'x'
y_name = 'y'
z_name = 'z'

# 等高線の数
# my_levels = 40 # 等高線の数
my_levels = [100,150,200,250] # 等高線の数
my_bins = 100 # 等高線の色数

# カラーマップ
my_cmap = 'jet' # 'bwr' 'bwr_r' 'cool' 'cool_r'

# ラベル
my_title = '関数 $f(x, y) = 6x - x^2 + 4y - y^2$'
my_xlabel = x_name + '軸'
my_ylabel = y_name + '軸'
my_zlabel = 'z = f(x, y)'


def plot_func(flag_contour_fill, z_min = None, z_max = None):
    # x, y, zデータを1次元のnumpyアレイ型へ変換
    x = DF[x_name].values
    y = DF[y_name].values
    z = DF[z_name].values

    # データ数と最小値、最大値を抽出
    N = len(DF)
    if z_min is None:
        x_min, y_min, z_min = x.min(), y.min(), z.min()
    else:
        x_min, y_min = x.min(), y.min()
    if z_max is None:
        x_max, y_max, z_max = x.max(), y.max(), z.max()
    else:
        x_max, y_max = x.max(), y.max()
    
    # データ点数を減らし等間隔の格子点用のデータを抜粋して作成する
    n = int(N / 4)
    xi, yi = np.linspace(x.min(), x.max(), n), np.linspace(y.min(), y.max(), n) 
    xi, yi = np.meshgrid(xi, yi) 
    # データ抜けがある場合にデータを線形補完
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear') 

    # 画像のインスタンスを生成
    fig = plt.figure(figsize=(8, 6))
    
    
    
    # 等高線
    if flag_contour_fill: # 等高線を塗りつぶす場合
        ax1 = fig.add_subplot(111)
        contour1 = ax1.contour(zi, vmin=z_min, vmax=z_max, 
                              origin='lower', levels=my_levels, colors=['black'],
                              extent=[x_min, x_max, y_min, y_max])
        # 等高線の色の階級を作成する
        my_bins_buf = np.arange(z_min, z_max, (z_max-z_min)/my_bins)
        my_z_range = np.append(my_bins_buf, z_max)
        
        cb = plt.contourf(xi, yi, zi, my_z_range, cmap=my_cmap) #カラーマップ
        
        # p = plt.colorbar(orientation="vertical") # カラーバーの表示
        cbar = fig.colorbar(cb, ticks=list(i for i in range(150,250,10)), shrink=0.5, orientation="vertical")
        # p.set_label(my_zlabel) # カラーバーのラベル
        
    else:
        # 背景色の設定 https://xkcd.com/color/rgb/
        ax1 = fig.add_subplot(111, facecolor="#ffffe4") # 背景色：オフホワイト
        contour1 = ax1.contour(zi, vmin=z_min, vmax=z_max, 
                              origin='lower', levels=my_levels, cmap=my_cmap,
                              extent=[x_min, x_max, y_min, y_max])

    # 等高線の線上に数値ラベルを表示
    contour1.clabel(fmt='%1.1f', fontsize=14)
    ax1.axis("off")

    # ラベル
    my_fontsize = 16
    # ax1.set_title(my_title, fontsize=my_fontsize)
    # ax1.set_xlabel(my_xlabel, fontsize=my_fontsize)
    # ax1.set_ylabel(my_ylabel, fontsize=my_fontsize)

    # 軸の範囲
    # buf_x = (x_max - x_min) * 0.001
    # buf_y = (y_max - y_min) * 0.001
    # ax1.set_xlim(x_min - buf_x, x_max + buf_x)
    # ax1.set_ylim(y_min - buf_y, y_max + buf_y)
    
    # 格子グリッド
    # plt.grid()

    # X軸のラベルを指定
    #x_range_list = list(np.arange(12, 20, 1))
    #plt.xticks(x_range_list, x_range_list)

    # X,Y軸の1目盛りの表示の縦横比を揃える
    plt.gca().set_aspect('equal', adjustable='box') 
    
    # グラフの見た目を整える
    plt.tick_params(labelsize=my_fontsize)
    plt.tight_layout() 

    # ファイルを保存
    fig.savefig(now + '_'  + "_contour_" + str(flag_contour_fill) + ".png")
    plt.show()
    plt.close()
    
    # ### 作成した等高線データをcsvに保存する
    # # numpy配列を展開
    # X, Y, Z = xi.flatten(), yi.flatten(), zi.flatten()
    # # pandasデータフレームへ変換してcsvファイルへ出力
    # df_buf = pd.DataFrame({x_name:X, y_name:Y, z_name:Z})
    # df_buf.to_csv(now + '_' + my_title + '.csv', encoding='cp932', index=False)

# 関数の実行
plot_func(True) # コンターを塗りつぶす場合はTrue
# plot_func(False) # コンターを塗りつぶさない場合はFalse