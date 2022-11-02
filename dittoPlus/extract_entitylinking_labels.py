import re
import pandas as pd
from pathlib import Path

def sep_ds(ds):
    """
    Separate the combined and serialized dataset to the original datasets
    use this as the input for Sherlock
    """
    dict_prep = {}
    for inner_value in ds:
        # [(' title ', ' query optimization by predicate move-around '), (' authors ', ' inderpal singh mumick , alon y. levy , yehoshua sagiv '), (' venue ', ' vldb '), (' year ', ' 1994 \t')]
        for k, v in inner_value:
            col_name = k.strip()
            col_value = v.strip()
            dict_prep.setdefault(col_name, []).append(col_value)
    return pd.DataFrame(dict_prep)


def create_input_ds(ds_f):
        # col_names_1 = []
        # col_names_2 = []
        ds_1 = []
        ds_2 = []
        # ds_3 = []
        tails = []
        for line_p in open(ds_f):
            pattern = re.compile(r'(COL|VAL)')
            line = line_p.rstrip()
            body = line[:-1]
            tail = line[-1]
            tails.append(int(tail))
            items = pattern.split(body)[1:]
            assert len(items) % 4 == 0
            pairs = []
            for i in range(len(items) // 4):
                pairs.append((items[i * 4 + 1], items[i * 4 + 3]))
            pair_1 = pairs[:len(pairs) // 2]
            pair_2 = pairs[len(pairs) // 2:]
            # col_names_1 = [v[0].strip() for v in pair_1]
            # col_names_2 = [v[0].strip() for v in pair_2]
            ds_1.append(pair_1)
            ds_2.append(pair_2)
        df_1 = sep_ds(ds_1)
        df_2 = sep_ds(ds_2)
        df_3 = pd.DataFrame({'flag': tails})
        return df_1, df_2, df_3


def split_ds(flag='train', input_fn='../data/ditto/er_magellan/Dirty/iTunes-Amazon/train.txt', overwrite=False):
    df1_raw_filename_csv = f'../data/Exp_data/Dirty/df1_iTunes_{flag}.csv' 
    df2_raw_filename_csv = f'../data/Exp_data/Dirty/df2_Amazon_{flag}.csv'
    if overwrite:
        df1, df2, df3 = create_input_ds(input_fn) # the first dataset, the second dataset, and the flag
        # df1: the first dataset; df2: the second dataset; df3: the pairing result
        df1.to_csv(df1_raw_filename_csv, index=False)
        df2.to_csv(df2_raw_filename_csv, index=False)
    else:
        pass
    return df1_raw_filename_csv, df2_raw_filename_csv

                
def extract_labels(fname):
    e1_label_list = []
    e2_label_list = []
    with open(fname, 'rt')as file:
        # data = csv.reader(file)
        for row in file:
            line = row.rstrip()
            body = line[:-1]
            label = line[-1]
            e1 = body.split('\t')[0]
            e2 = body.split('\t')[1]
            # label = body.split('\t')[2]
            e1_attr_label = re.findall(r'COL\sSong_Name\sVAL\s<head>(.*?)<\/head><tail>(.*?)<\/tail>', e1)
            e2_attr_label = re.findall(r'COL\sSong_Name\sVAL\s<head>(.*?)<\/head><tail>(.*?)<\/tail>', e2)
            e1_label_list.append(e1_attr_label)
            e2_label_list.append(e2_attr_label)
    return e1_label_list, e2_label_list


def split_ds_wf(flag):
    # flag='test'
    # flag = 'valid'
    input_fn=f'../data/ditto/er_magellan/Dirty/iTunes-Amazon/{flag}.txt'
    res1, res2 = split_ds(flag, input_fn, overwrite=False)
    return res1, res2


def main(flag='train'):
    # //projects/bbno/lanl2/2022Fa-Showcase/data/entity_linking_data/train.txt.entityLinking.prompt=0.dk
    # flag = 'train'
    dirty_data_1,  dirty_data_2 = split_ds_wf(flag)
    print(dirty_data_1)

    filename = f'../data/entity_linking_data/{flag}.txt.entityLinking.prompt=0.dk'
    e1_list, e2_list = extract_labels(filename)
    # /projects/bbno/lanl2/2022Fa-Showcase/data/Exp_data/Dirty/df1_Dirty_iTunes-Amazon.csv
    # dirty_data_1 = '../data/Exp_data/Dirty/df1_Dirty_iTunes-Amazon.csv'
    dirty_df1 = pd.read_csv(dirty_data_1, index_col=False)
    # /projects/bbno/lanl2/2022Fa-Showcase/data/Exp_data/Dirty/df2_Dirty_iTunes-Amazon.csv
    # dirty_data_2 = '../data/Exp_data/Dirty/df2_Dirty_iTunes-Amazon.csv'
    dirty_df2 = pd.read_csv(dirty_data_2, index_col=False)
    assert len(e1_list) == dirty_df1.shape[0]
    assert len(e2_list) == dirty_df2.shape[0]
    dirty_df1['Song_Name_Clean'] = dirty_df1['Song_Name']
    dirty_df2['Song_Name_Clean'] = dirty_df2['Song_Name']
    for i,row in enumerate(e1_list):
        if row:
            assert len(row[0]) == 2
            dirty_df1['Song_Name_Clean'].iloc[i] = row[0][0]
        else:
            dirty_df1['Song_Name_Clean'].iloc[i] = ''
    
    for j,row_j in enumerate(e2_list):
        if row_j:
            assert len(row_j[0]) == 2
            dirty_df2['Song_Name_Clean'].iloc[j] = row_j[0][0]
        else:
            dirty_df2['Song_Name_Clean'].iloc[j] = ''
    
    clean_d1 = f'../data/Exp_data/Clean/df1_iTunes_{flag}_clean.csv' 
    clean_d2 = f'../data/Exp_data/Clean/df2_Amazon_{flag}_clean.csv' 
    d1_path = Path(clean_d1)
    d2_path = Path(clean_d2)
    # if not d1_path.exists():
    dirty_df1.to_csv(clean_d1, index=False)
    # if not d2_path.exists():
    dirty_df2.to_csv(clean_d2, index=False)


if __name__ == '__main__':
    for flag in ['train', 'test', 'valid']:
        main(flag)
    # flag = 'train'
    # flag = 'test'
    # flag = 'valid'
    # split_ds_wf()
