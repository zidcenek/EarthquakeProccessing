import pandas as pd
from os import listdir, remove, replace
from os.path import isfile, join
import filecmp
from Earthquake import Earthquake

COLUMNS = ['date', 'id', 'time', 'lat', 'lon', 'h', 'WGS', 'Ml', 'station', 'P/S', 'zeros', 'datetime', 'duration']


def fetch_files(path: str, ending: str) -> [str]:
    '''
    Fetches all files in the given path  ending with '.bul'
    :param path:
    :return: list of file names
    '''
    if path[-1] != '/':
        path += '/'
    files = []
    try:
        files = [f for f in listdir(path) if isfile(join(path, f))]
    except:
        print("Trouble opening a directory")
        return files
    return [path + f for f in files if f[-len(ending):] == ending]


def open_files(files: [str]):
    '''
    Tries to open all the given files and creates pandas dataframes
    :param files:
    :return:
    '''
    dataframes = []
    counter = 0
    for f in files:
        try:
            df = pd.read_csv(f, delimiter=';', header=None, names=COLUMNS, index_col=False)
            dataframes.append(df)
            df['file'] = counter
            counter += 1
        except:
            print('Chyba při čtení souboru', f)

    return dataframes


def drop_unnecessary_columns(df, cols: [str]):
    '''
    Drops the fiven columns from the dataframe
    :param df:
    :param cols:
    :return:
    '''
    try:
        return df.drop(cols, axis=1)
    except:
        print('Could not delete some these columns:', cols, 'Returning unchanged dataframe')
        return df


def merge_coordinates(df):
    '''
    Merges 'lat' and 'lon' columns into 'coordinates' column and then drops the original ones
    :param df:
    :return:
    '''
    df['coordinates'] = df['lat'].str.strip() + " " + df['lon'].str.strip()
    return df.drop(['lat', 'lon'], axis=1)


def make_groups(df):
    '''
    Divides the data into groups based on the 'id' column and then into subgroups based on the 'coordinates' column
    :param df:
    :return:
    '''
    groups = dict.fromkeys(df.id.unique())
    #     eq_number = 0
    for key in groups.keys():
        #         eq_number += 1
        tmp = df[df.id == key]
        subgroups = dict.fromkeys([key for key, _ in tmp.groupby(['coordinates'])])
        order_number = 0
        for row in tmp.iterrows():
            if subgroups[row[1]['coordinates']] == None:
                subgroups[row[1]['coordinates']] = Earthquake(row[1]['coordinates'], str(key)[4:], order_number)
                order_number += 1
            subgroups[row[1]['coordinates']].add_record(row[1])
        groups[key] = subgroups
    return groups


def divide_data(df):
    groups = make_groups(df)
    for group in groups.values():
        for earthquake in group.values():
            earthquake.convert_to_pandas_df()
            earthquake.process_records()
            earthquake.create_output_files('../output')


def compare_files(path):
    '''
    Compares the dupplicate files, if they are the same then removes one and renames the other
    :param path:
    :return:
    '''
    if path[-1] != '/':
            path += '/'
    files = fetch_files(path, '_0.csv')
    for file in files:
        if isfile(file[0:-6] + "_1.csv"):
            print(file)
            if filecmp.cmp(file[0:-6] + "_0.csv", file[0:-6] + "_1.csv"):
                print("Files are the same => removing ")
                remove(file[0:-6] + "_1.csv")
                if isfile(file[0:-6] + "_0.csv"):
                    replace(file[0:-6] + "_0.csv", file[0:-6] + ".csv")
            else:
                print('Files are different => keeping both versions')
        else:
            if isfile(file):
                replace(file, file[0:-6] + ".csv")


def initialize():
    df = pd.concat(open_files(fetch_files('../data', '.bul')))
    df = df.reset_index(drop=True)
    df = merge_coordinates(df)
    cols = ['h', 'WGS', 'Ml', 'date', 'time', 'zeros', 'duration', 'file']
    df = drop_unnecessary_columns(df, cols)
    df['station'] = df['station'].str.strip()
    df['datetime'] = pd.to_datetime(df['datetime'], format=" %Y-%m-%d %H:%M:%S.%f")
    divide_data(df)


initialize()

compare_files('../output')  # delete this if you want to keep both output versions
