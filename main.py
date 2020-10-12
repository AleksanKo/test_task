import argparse
import xml.etree.ElementTree as etree
from datetime import datetime
import pandas as pd

parser = argparse.ArgumentParser(description='Parsing file')

parser.add_argument('file', help='a path to the file to be parsed')
parser.add_argument('csv', help='a path to the CSV file where to save the results')
parser.add_argument('--filter', choices=['name','dates'], help='choose to filter by name or by dates')
parser.add_argument('--dates', nargs="+", help='filter by two dates')

args = parser.parse_args()

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
    return df[df['Persons'] == name] if name in list(df['Persons']) else 'No such person'

def filter_by_dates(df, dates):
    mask = (df['Dates'] >= dates[0]) & (df['Dates'] <= dates[1])
    return df.loc[mask]

def main():

    persons = []
    dates = []
    times = []

    with open('test.xml') as infile:
        for event, elem in etree.iterparse(infile,events=("start",)):
            if elem.tag == 'person':
                print(elem.tag, elem.find('start').text, elem.find('end').text)
                print(elem.find('start').text)
                #print('start',parse_time(elem.find('start').text))
                print('start', parse_time(elem.find('start').text))
                print(parse_date(elem.find('start').text))
                print('counting time',count_time(elem.find('start').text, elem.find('end').text))
                persons.append(elem.attrib['full_name'])
                dates.append(parse_date(elem.find('start').text))
                times.append(count_time(elem.find('start').text, elem.find('end').text))
                #persons.update({elem.attrib['full_name']:[parse_date(elem.find('start').text),]})

    df = pd.DataFrame({'Persons':persons,'Dates':dates,'Time': times})
    df['Dates'] = pd.to_datetime(df['Dates'])

    print(df.head())
    print(df.groupby('Dates').agg({'Time':'sum'}))

    #filter_by_dates(df,'2011-12-21','2019-12-22')
    #filter_by_name(df,'i.ivnov')

if __name__ == '__main__':
    main()

