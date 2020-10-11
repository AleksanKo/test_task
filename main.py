import xml.etree.ElementTree as etree
from datetime import datetime
import pandas as pd

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

def filter_by_name(name):
    pass


def filter_by_dates(df, *dates):
    if len(dates) == 2:
        mask = (df['Dates'] >= dates[0]) & (df['Dates'] <= dates[1])
        print(df.loc[mask])
        print(type(dates))
        return df.loc[mask]
    if type(dates) == str:
        print(df[df['Dates']==dates])
        return df[df['Dates']==dates]
    else:
        print('lol')

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
    #the most importnant part - make a function? or return?
    print(df.groupby('Dates').agg({'Time':'sum'}))

    filter_by_dates(df,'2011-12-21','2019-12-22')
if __name__ == '__main__':
    main()

