
# coding: utf-8
from bs4 import BeautifulSoup
import requests, csv, json, time, datetime, os

import calendar
# ###http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20170605&stockNo=2330


#standard web crawing process
def get_webmsg (date_str, stock_id):
    # date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
    print(date_str)
    #url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+stock_id
    payload = {'response': 'json', 'date': date_str, 'stockNo' : stock_id}
    url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY'
    res = requests.get(url_twse, payload)
    if res.status_code == requests.codes.ok:
        return res.json()
    return False



def write_csv(stock_id,directory,filename,smt) :
    writefile = directory + filename               #set output file name
    outputFile = open(writefile,'a+',newline='')
    outputWriter = csv.writer(outputFile)
    head = ''.join(smt['title'].split())
    outputWriter.writerow([head,""])
    outputWriter.writerow(smt['fields'])
    for data in (smt['data']):
        outputWriter.writerow(data)

    outputFile.close()

#create a directory in the current one doesn't exist
def makedirs (directory):
    if not os.path.isdir(directory):
        os.makedirs (directory)  # os.makedirs able to create multi folders

def getdateandwrite(stock_id):
    begin_date = datetime.datetime.strptime('2010-01-01', "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())), "%Y-%m-%d")
    temp = {}
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        Y = begin_date.strftime("%Y")
        m = int(begin_date.strftime("%m"))
        filename = stock_id+'.csv'          #setting file name
        smt = get_webmsg(date_str, stock_id)           #put the data into smt 
        write_csv (stock_id,directory, filename, smt)    # write files into CSV
        begin_date += datetime.timedelta(days=calendar.mdays[m])
        time.sleep(1)
    return True

def processCSV(stock_id):
    openfile = directory + stock_id+'.csv'
    writefile = directory + stock_id+'-1.csv'
    with open(openfile) as f:
        myCsv = csv.reader(f)
        headers = next(myCsv)
        outputFile = open(writefile,'a+',newline='')
        outputWriter = csv.writer(outputFile)
        for row in myCsv:
            if(len(row) > 3 and row[0]!="日期"):
                outputWriter.writerow(row)
    return True
if __name__ == "__main__":

    id_list = ['3481','2409'] #inout the stock IDs
    now = datetime.datetime.today()
    '''
    for stock_id in id_list:
        for year in range (2004,now.year+1):
            for month in range(1,13):
                for day in range(1, calendar.mdays[month]):
                if (now.year == year and month > now.month) :break  # break loop while month over current month
                yy  = str(year)
                mm  = month
                directory = 'D:/stock/'+stock_id +'/'+yy +'/'       #setting directory
                filename = str(yy)+str("%02d"%mm)+'.csv'          #setting file name
                smt = get_webmsg(now, stock_id)           #put the data into smt 
                makedirs (directory)                  #create directory function
                write_csv (stock_id,directory, filename, smt)    # write files into CSV
                time.sleep(1)
    '''
    directory = './stock/'      #setting directory
    #makedirs (directory)                  #create directory function

    for stock_id in id_list:
        #getdateandwrite(stock_id)
        #processCSV(stock_id)
