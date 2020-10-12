import pandas as pd
import numpy as np


class Earthquake:
    def __init__(self, coordinates, earthquake_id, order_number):
        self.__coordinates = coordinates
        self.__earthquake_id = earthquake_id
        self.__order_number = order_number
        self.__records = []
        self.__output = pd.DataFrame(columns=['STA', 'P', 'S', 'S-P'])
        self.__buffer = []

    @property
    def coordinates(self) -> str:
        return self.__coordinates

    @property
    def earthquake_id(self) -> int:
        return self.__earthquake_id

    @property
    def order_number(self) -> int:
        return self.__order_number

    def add_record(self, record: list):
        '''
        Adds a record to the "self.__records" list
        :param record:
        :return:
        '''
        self.__records.append(record.drop(['coordinates']))

    def convert_to_pandas_df(self):
        '''
        Converts a normal list to pandas dataframe
        :return:
        '''
        self.__records = pd.DataFrame(self.__records)

    def process_records(self):
        '''
        Processes the records and transforms them into an output-like format list
        :return:
        '''
        self.__records.datetime = self.__records.datetime - self.__records.datetime.min()
        self.__records['zero_time'] = self.__records.datetime.astype(np.int64) // 10 ** 6
        self.__records = self.__records.sort_values('zero_time')

        for row in self.__records.iterrows():
            self.process_line(row[1])

        size = len(self.__buffer)
        for i in range(size):
            print('S value before a P value at', self.__earthquake_id)
            self.process_line(self.__buffer[i])

    def process_line(self, line: list):
        '''
        Tranfrorms a single line to an output-like format and saves it to the "self.__output" lists
        :param line:
        :return:
        '''
        if line['P/S'].strip() == 'P':
            output_line = {}
            output_line['STA'] = line.station
            output_line['P'] = line.zero_time
            output_line['S'] = 99999
            output_line['S-P'] = 99999
            self.__output = self.__output.append(output_line, ignore_index=True)

        elif line['P/S'].strip() == 'S':
            station = line.station
            if len(self.__output[self.__output.STA == station].index.values) == 0:
                self.__buffer.append(line)
                return
            index = self.__output[self.__output.STA == station].index.values[0]
            self.__output.loc[index]['S'] = line.zero_time
            self.__output.loc[index]['S-P'] = line.zero_time - self.__output.loc[index]['P']

    def create_output_files(self, path):
        '''
        Creates output files from the 'self.__output' dataframe
        :param path:
        :return:
        '''
        if path[-1] != '/':
            path += '/'
        complete_path = path + str(self.earthquake_id) + '_' + str(self.order_number) + '.csv'
        print('output to', complete_path)
        self.__output.to_csv(complete_path, index=False, sep='\t')
