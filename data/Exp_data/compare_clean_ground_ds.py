# This script is to compare the prepared dataset with the ground dataset 
import re
import pandas as pd


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
        # tails = []
        for line_p in open(ds_f):
            pattern = re.compile(r'(COL|VAL)')
            line = line_p.rstrip()
            body = line[:-1]
            # tail = line[-1]
            # tails.append(int(tail))
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
        # df_3 = pd.DataFrame({'flag': tails})
        return df_1, df_2


def main():
    ground_ds = '../er_magellan/Structured/iTunes-Amazon'
    flags = ['train', 'test', 'valid']
    res_df = pd.DataFrame(columns=['dataset_name_clean', 'dataset_name_ground', 'column_name','mismatch','mismatch_freq'])
    for flag in flags:
        ground_ds_file = f'{ground_ds}/{flag}.txt'
        ground_output_df1 = f'Ground/df1_iTunes_{flag}.csv'
        ground_output_df2 = f'Ground/df2_Amazon_{flag}.csv'
        df1, df2 = create_input_ds(ground_ds_file)
        df1.to_csv(ground_output_df1, index=False)
        df2.to_csv(ground_output_df2, index=False)
        # clean_output_df1 = f'Clean/df1_iTunes_{flag}.csv'
        # clean_output_df2 = f'Clean/df2_Amazon_{flag}.csv'
        # res_df['dataset_name_clean']=  clean_output_df1
        # res_df['dataset_name_ground'] = ground_output_df1


if __name__ == "__main__":
    main()