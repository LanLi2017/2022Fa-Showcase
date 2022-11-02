import pandas as pd 


def get_labels(fname):
    print(fname)
    labels = []
    with open(fname, 'rt')as file:
        # data = csv.reader(file)
        for row in file:
            line = row.rstrip()
            label = line[-1]
            labels.append(label)
    return labels


def serialized(df:pd.DataFrame):
    cols = list(df.columns)
    new_df = pd.DataFrame(columns=cols)
    for index, row in df.iterrows():
        for col in cols:
            old_value = row[col]
            new_value = f"COL {col} VAL {old_value}"
            new_df.at[index, col] = new_value
            # .....new_df 
    return new_df


def main():
    flags = ['train', 'test', 'valid']
    # flags = ['train']
    for flag in flags:
        input_fn=f'../ditto/er_magellan/Dirty/iTunes-Amazon/{flag}.txt'
        labels = get_labels(input_fn)
        df3 = pd.DataFrame(labels, columns=['label'])

        df1_csv = f'OpenRefine_Output/df1_iTunes_{flag}_clean_final.csv'
        df2_csv = f'OpenRefine_Output/df2_Amazon_{flag}_clean_final.csv'
        print(df1_csv)
        out_fn = f'ditto_input/{flag}.txt'
        df1 = pd.read_csv(df1_csv, index_col=False)
        df2 = pd.read_csv(df2_csv, index_col=False)
        df1_serialized = serialized(df1)
        df2_serialized = serialized(df2)
        assert df1_serialized.shape[0] == df2_serialized.shape[0]
        assert len(labels) == df1_serialized.shape[0]
        
        with open(out_fn, 'w') as fout:
            for i in range(len(df1_serialized)):
                entry0 = ''
                entry1 = ''
                fir_row = df1_serialized.iloc[i]
                entry0 += ' '.join(fir_row)
                sec_row = df2_serialized.iloc[i]
                entry1 += ' '.join(sec_row)
                entry2 = int(df3.loc[i, 'label'])
                # out_row_list.append(list(fir_row)+list(sec_row)+[entry2])
                fout.write(entry0 + '\t' + entry1 + '\t' + str(entry2) + '\n')
                # print(f"{entry0} + '\t' + {entry1} + '\t' + {entry2}")


if __name__ == '__main__':
    main()