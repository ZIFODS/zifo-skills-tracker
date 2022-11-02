'''
Pipeline Script
'''
import pandas as pd
import numpy as np

def main():
    '''
    Main method
    '''
    neo4j_input_file = 'Zifo Europe - Skills Survey(1-77).csv'
    neo4j_input_path = 'input/' + neo4j_input_file
    loadData(neo4j_input_path)


def loadData(path):
    '''
    Loads data from survey csv export
    Arguments
    ------
    path : str - path of csv export
    '''
    # open the file to read from
    readdata = pd.read_csv(path, header=0)
    namedata = readdata[["ID", "Email", "Name"]]
    namedata.columns = ["id","email","fullname"]

    #apply lambda function
    readdata = readdata.drop(['ID','Start time','Completion time', "Name", "Email"], axis=1)
    readdata = readdata.apply(lambda x: split_strings(x))
    
    #rename headers
    headers = ['science_apps', 'services', 'methodogies', 'process',
                'other_products', 'regulatory', 'data_management', 'languages', 'programming',
                'misc', 'infrastructure']
    readdata.columns = headers
    readdata = readdata.apply(lambda x: x.fillna({i: [] for i in x.index}))

    # create new column with maximum length of list on each row
    readdata["max_length"] = readdata.apply(lambda x: x.map(len).max(), axis=1)

    # extend all lists on each row to length in max length column
    readdata = readdata.apply(lambda x: x.iloc[:-1].apply(lambda y: extend_list(y, x["max_length"])), axis=1)

    #explode the columns
    readdata_sep = pd.DataFrame()
    for col in headers:
        col_sep = readdata[col].explode().to_frame()
        readdata_sep = pd.concat([readdata_sep, col_sep])

    #remove na values
    readdata_sep = readdata_sep.dropna(how="all")

    # combine namedata and readdata_sep using pd.join
    readdata = namedata.join(readdata_sep)

    #save to csv
    outputpath = 'pipeline/src/input/neo4jimport.csv'
    readdata.to_csv(outputpath, index=False)

def split_strings(input):
    '''
    Splits the strings by semicolon

    Arguments
    ------------
    input : str - item in the list
    '''
    return input.str.split(';')


def extend_list(list_value, max_length):
    '''
    Extends the list to be length of the list in the series with the highest length

    Arguments
    ----------
    list_value : list - items from the list
    max_length : int - length of the longest list

    Returns
    ---------
    list_value : list
    '''
    list_value.extend([np.nan for _ in range(max_length - len(list_value))])
    return list_value
    

def isNaN(string):
    '''
    Checks if item is a string or a NaN value
    
    Arguments
    ------
    string : any

    Returns
    --------
    boolean - if string is NaN
    '''
    return string != string

main()
