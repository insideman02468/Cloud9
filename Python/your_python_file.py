# coding: utf-8

from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import os,sys
import pandas as pd
from do_pivot import main

backend : Agg

# global path name(store file path)
path_name = "."

def close_window():
    root.destroy()

def load_file(_entry):
    global path_name
    try:
        filename = tkFileDialog.askopenfilename(initialdir=path_name)
        if filename is not None:
            path_name = os.path.dirname(filename) #現在のpathをdefaultに設定
            _entry.set(filename)
    except ValueError, e:
        pass

def pivot(*args):
    try:
        result_dic = main(input_filename.get(), funcs.get().encode('utf-8'), \
                          row_columns.get().encode('utf-8'), col_columns.get().encode('utf-8'))
        for (row_label,col_label, s_func), pivoted_data in result_dic.items():
            pivoted_data.to_csv(output_filename.get()+row_label+u'-'+col_label+u'-'+u'_pivot('+s_func+u').csv', encodeing='shift-jis')
        tkMessageBox.showinfo(u'showinfo', u'正常終了')
    except Exception, e:
        import traceback
        print traceback.format_exc()
        tkMessageBox.showerror(u'showerror',u'エラーが発生しました')

def set_save_file_name(_entry):
    global path_name
    try:
        filename = tkFileDialog.asksaveasfilename(initialfile='pivot_result_', defaultextension='' ,initialdir=path_name)
        if filename is not None:
            path_name = os.path.dirname(filename)
            _entry.set(filename)
    except ValueError:
        pass

if __name__=='__main__':
    root = Tk()
    root.title(u"pivot data")

    # frameの定義
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # 変数の定義
    input_filename = StringVar()
    output_filename = StringVar()
    row_columns = StringVar()
    col_columns = StringVar()
    funcs = StringVar()

    # 初期値の設定
    row_columns.set('demogra,class')
    col_columns.set('満足項目1、満足項目2、満足項目3、満足項目4')
    funcs.set('カウント、平均')

    ttk.Label(mainframe, text=u"アンケート結果ファイル").grid(column=1, row=1, sticky=W)
    input_filename_entry = ttk.Entry(mainframe, width=20, textvariable=input_filename)
    input_filename_entry.grid(column=2, row=1, sticky=(W, E))
    ttk.Button(mainframe, text=u'ファイル検索', command= lambda: load_file(input_filename)).grid(column=3, row=1,sticky=E)

    ttk.Label(mainframe, text=u"出力ベースファイル名").grid(column=1, row=2, sticky=W)
    output_filename_entry = ttk.Entry(mainframe, width=20, textvariable=output_filename)
    output_filename_entry.grid(column=2, row=2, sticky=(W, E))
    ttk.Button(mainframe, text=u'ファイル検索', command= lambda: set_save_file_name(output_filename)).grid(column=3, row=2, sticky=E)

    ttk.Label(mainframe, text=u"セグメント列（複数可）").grid(column=1, row=3, sticky=W)
    row_columns_entry = ttk.Entry(mainframe, width=20, textvariable=row_columns)
    row_columns_entry.grid(column=2, row=3, sticky=(W, E))

    ttk.Label(mainframe, text=u"集計対象列（複数可）").grid(column=1, row=4, sticky=W)
    col_columns_entry = ttk.Entry(mainframe, width=20, textvariable=col_columns)
    col_columns_entry.grid(column=2, row=4, sticky=(W, E))

    ttk.Label(mainframe, text=u"集計方法（複数可）").grid(column=1, row=5, sticky=W)
    funcs_entry = ttk.Entry(mainframe, width=20, textvariable=funcs)
    funcs_entry.grid(column=2, row=5, sticky=(W, E))

    # calculate button
    ttk.Button(mainframe, text=u'Calculate', command=pivot).grid(column=2,row=6, sticky=E)

    # close button
    ttk.Button(mainframe, text=u'Exit', command=close_window).grid(column=3,row=6)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=6)

    input_filename_entry.focus()
    root.bind('<Return>', pivot)

    root.mainloop()
    
    # coding: utf-8

import pandas as pd
import os
import numpy as np

def get_data(ifname):
    if '.csv' in ifname:
        return pd.read_csv(ifname, delimiter=r',', encoding='shift-jis')
    elif '.tsv' in ifname:
        return pd.read_csv(ifname, delimiter=r'\t', encoding='shift-jis')

def calculate_pivot(df_data, row_label, col_label, agg_func):
    try:
        df_data[col_label].astype(np.float64)
        return df_data[[row_label, col_label]].groupby(row_label).aggregate(agg_func)
    except Exception, e:
        print e
        return df_data[[row_label, col_label]].pivot_table(rows=row_label, cols=col_label, aggfunc=agg_func, fill_value=0)

def select_pivot_func(str_funcs):
    avg = (u'average',u'avg',u'mean',u'平均',u'平均値')
    cnt = (u'count',u'カウント',u'カウント数',u'カウント値',u'回数')
    total_sum = (u'sum',u'total',u'合計',u'計',u'合計値')
    med = (u'median',u'中央値',u'中央')
    sv = (u'分散',u'var',u'variance')
    sd = (u'標準偏差',u'deviation',u'sd')

    func_list = []
    except_len_list = []
    for t_func in replace_comma(str_funcs):
        t_func = t_func.strip()
        if t_func in cnt:
            func_list.append((t_func,[len]))
        elif t_func in avg:
            except_len_list = add_func(except_len_list, t_func, np.mean)
        elif t_func in total_sum:
            except_len_list = add_func(except_len_list, t_func, np.sum)
        elif t_func in med:
            except_len_list = add_func(except_len_list, t_func, np.median)
        elif t_func in sv:
            except_len_list = add_func(except_len_list, t_func, np.var)
        elif t_func in sd:
            except_len_list = add_func(except_len_list, t_func, np.std)
    return func_list+except_len_list

def add_func(except_len_list, t_func, func):
    if len(except_len_list)!=0:
        except_len_list[0] = \
            (except_len_list[0][0]+','+t_func, except_len_list[0][1]+[func])
    else:
        except_len_list.append((t_func,[func]))
    return except_len_list

def replace_comma(str_data):
    str_res = [ s.decode('utf-8') for s in str_data.replace('、', ',').strip().split(',')]
    return map(lambda s:s.strip(), str_res)

def do_pivot(df_data ,row_labels, col_labels, str_funcs):
    pivot_dic = {}
    for s_func, func in select_pivot_func(str_funcs):
        for row_label in replace_comma(row_labels):
            for col_label in replace_comma(col_labels):
                try:
                    pivot_dic[(row_label,col_label,s_func)] = \
                        calculate_pivot(df_data, row_label, col_label, func)
                except Exception, e:
                    #print "miss:", s_func, col_label
                    print e
    #for (row_label,col_label, s_func), pivot_q in pivot_dic.items():
    #    print type(row_label), row_label
    #    pivot_q.to_csv( row_label+u'-'+col_label+u'-'+u'_pivot('+s_func+u').csv')
    return pivot_dic

def main(ifname, str_funcs, str_row_labels, str_col_labels):
    df_raw_data = get_data(ifname)

    return  do_pivot(df_raw_data, str_row_labels, str_col_labels, str_funcs)

if __name__ == '__main__':
    basepath = os.getcwd()
    ifpath = basepath + '/'
    ofpath = basepath + '/'
    ifname = ifpath + '/test.tsv'

    ### raw dataの取得
    df_raw_data = get_data(ifname)
    df_raw_data['test'] = np.random.randint(5,size=len(df_raw_data.ix[:,0]))

    # ピポッド項目
    str_funcs = 'カウント、平均,分散'
    col_labels = "Q4_s, Q5_s,Q6_s,Q7_s,Q8_s,Q9_s,test"
    row_labels = "class,demogra"

    do_pivot(df_raw_data, row_labels, col_labels, str_funcs)