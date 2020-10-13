import argparse
import xml.etree.ElementTree as etree
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser(description='Parsing file')

parser.add_argument('file', help='a path to the file to be parsed')
parser.add_argument('csv', help='a path to the CSV file where to save the results')
parser.add_argument('-n','--name', help='filter by name')
parser.add_argument('-d','--dates', nargs="+", help='filter by two dates')

args = parser.parse_args()

name = args.name
dates = args.dates

def parse_date(line):
    date = datetime.strptime(line,'%d-%m-%Y %H:%M:%S').strftime('%d-%m-%Y')
    return date

def parse_time(line):
    time = datetime.strptime(line,'%d-%m-%Y %H:%M:%S').strftime('%H:%M:%S')
    return time

def count_time(start,end):
    start_time = datetime.strptime(start,'%d-%m-%Y %H:%M:%S')
    end_time = datetime.strptime(end, '%d-%m-%Y %H:%M:%S')
    return end_time - start_time

def filter_by_name(df, name):
    print(df[df['Persons'] == name] if name in list(df['Persons']) else 'No such person')
    return df[df['Persons'] == name] if name in list(df['Persons']) else 'No such person'

def filter_by_dates(df, dates):
    mask = (df['Dates'] >= dates[0]) & (df['Dates'] <= dates[1])
    print(df.loc[mask] if not df.loc[mask].empty else 'No results for given dates')
    return df.loc[mask]

def parsing_file():

    persons = []
    dates = []
    times = []

    with open('test.xml') as infile:
        for event, elem in etree.iterparse(infile,events=("start",)):
            if elem.tag == 'person':
                #print(elem.tag, elem.find('start').text, elem.find('end').text)
                #print(elem.find('start').text)
                #print('start',parse_time(elem.find('start').text))
                #print('start', parse_time(elem.find('start').text))
                #print(parse_date(elem.find('start').text))
                #print('counting time',count_time(elem.find('start').text, elem.find('end').text))
                persons.append(elem.attrib['full_name'])
                dates.append(parse_date(elem.find('start').text))
                times.append(count_time(elem.find('start').text, elem.find('end').text))
                #persons.update({elem.attrib['full_name']:[parse_date(elem.find('start').text),]})
    df = pd.DataFrame({'Persons':persons,'Dates':dates,'Time': times})
    df['Dates'] = pd.to_datetime(df['Dates'])
    return df

def main():

    df = parsing_file()

    if name:
        filter_by_name(df, name)
    elif dates:
        filter_by_dates(df, dates)
    else:
        return df.groupby('Dates').agg({'Time':'sum'})

if __name__ == '__main__':
    main()

