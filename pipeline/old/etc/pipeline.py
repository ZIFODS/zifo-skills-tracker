# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from shutil import copyfile
from pandas import read_csv
import csv
import numpy
import math
from pyrsistent import v
from operator import length_hint

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------


def main():

    neo4J_input_file = 'Zifo Europe - Skills Survey(1-77).csv'
    neo4J_output_file = 'neo4jimport.csv'
    neo4J_input_path = 'input\\' + neo4J_input_file

    neo4J_import = 'C:\\Users\\AlistairEuanDean\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-1629f80b-e432-4270-87aa-abc9dce06770\\import\\'

    ## neo4J_input = 'input\\Zifo Europe - Skills Survey(1-77).csv'

    dfSkillsData = loadData(neo4J_input_path)

    copyFileToImportFolder(
        neo4J_input_path, neo4J_import + neo4J_output_file)

# ------------------------------------------------------------------------------
# Revenue
# ------------------------------------------------------------------------------


def loadData(path):

    series = loadCsvSkills(path)

    # open the file in the write mode
    with open('output\\neo4jimport.csv', 'w', newline='', encoding="utf-8") as f:
        # create the csv writer
        writer = csv.writer(f)
        headers = ['id', 'email', 'fullname', 'science_apps', 'services', 'methodogies', 'process',
                   'other_products', 'regulatory', 'data_management', 'languages', 'programming', 'misc', 'infrastructure']
        writer.writerow(headers)

        count = series.shape[0]

        for i in range(1, count, 1):
            row = series.values[i]

            id = i
            email = row[2]
            name = row[3]

            scientificProductsApplicationsList = parselist(row[4])
            servicesList = parselist(row[5])
            methodologiesList = parselist(row[6])
            RandDProcessesList = parselist(row[7])
            ProductsAndApplicationsList = parselist(row[8])
            RegulationsList = parselist(row[9])
            DataManagementList = parselist(row[10])
            LanguagesList = parselist(row[11])
            ProgrammingLanguagesList = parselist(row[12])
            MiscellaneousList = parselist(row[13])
            InfrastructureList = parselist(row[14])

            if length_hint(scientificProductsApplicationsList) > 0:
                for x in scientificProductsApplicationsList:
                    data = [id, email, name, x, '', '',
                            '', '', '', '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(servicesList) > 0:
                for x in servicesList:
                    data = [id, email, name, '', x, '',
                            '', '', '', '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(methodologiesList) > 0:
                for x in methodologiesList:
                    data = [id, email, name, '', '', x,
                            '', '', '', '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(RandDProcessesList) > 0:
                for x in RandDProcessesList:
                    data = [id, email, name, '', '', '',
                            x, '', '', '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(ProductsAndApplicationsList) > 0:
                for x in ProductsAndApplicationsList:
                    data = [id, email, name, '', '', '',
                            '', x, '', '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(RegulationsList) > 0:
                for x in RegulationsList:
                    data = [id, email, name, '', '', '',
                            '', '', x, '', '', '', '', '']
                    writer.writerow(data)

            if length_hint(DataManagementList) > 0:
                for x in DataManagementList:
                    data = [id, email, name, '', '', '',
                            '', '', '', x, '', '', '', '']
                    writer.writerow(data)

            if length_hint(LanguagesList) > 0:
                for x in LanguagesList:
                    data = [id, email, name, '', '', '',
                            '', '', '', '', x, '', '', '']
                    writer.writerow(data)

            if length_hint(ProgrammingLanguagesList) > 0:
                for x in ProgrammingLanguagesList:
                    data = [id, email, name, '', '', '',
                            '', '', '', '', '', x, '', '', ]
                    writer.writerow(data)

            if length_hint(MiscellaneousList) > 0:
                for x in MiscellaneousList:
                    data = [id, email, name, '', '', '',
                            '', '', '', '', '', '', x, '']
                    writer.writerow(data)

            if length_hint(InfrastructureList) > 0:
                for x in InfrastructureList:
                    data = [id, email, name, '', '', '',
                            '', '', '', '', '', '', '', x]
                    writer.writerow(data)


# ------------------------------------------------------------------------------
# split strings
# ------------------------------------------------------------------------------
def copyFileToImportFolder(frompath, topath):
    copyfile(frompath, topath)


# ------------------------------------------------------------------------------
# split strings
# ------------------------------------------------------------------------------

def parselist(input):
    if isNaN(input) is False:
        return list(filter(None, input.split(";")))
    else:
        return input

# ------------------------------------------------------------------------------
# Test is a String is NaN
# ------------------------------------------------------------------------------


def isNaN(string):
    return string != string


# ------------------------------------------------------------------------------
# Get and Process data Series
# ------------------------------------------------------------------------------

def loadCsvSkills(file):
    series = read_csv(file, header=None,
                      parse_dates=[0], index_col=0, squeeze=True)

    return series

# ------------------------------------------------------------------------------
# Program main function (entry point)
# ------------------------------------------------------------------------------


main()
