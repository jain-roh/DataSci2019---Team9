import luigi
import pandas as pd
import requests
import csv
import numpy as np
import dropbox
import os
from dropbox.files import WriteMode
dbx = dropbox.Dropbox('aDf1htlkmN8AAAAAAAAC-_IjjyFsEJBJU6fY86Y32dr1LH3kVthriApkX9h08kmf')
class Task0(luigi.Task):
    def run(self):
        #dbx = dropbox.Dropbox('aDf1htlkmN8AAAAAAAAC-_IjjyFsEJBJU6fY86Y32dr1LH3kVthriApkX9h08kmf')

        #xls = 'data_final.csv'



        dbx.files_download_to_file(os.getcwd()+'/data_final.csv', '/DataScienceTeam9/'+ 'data_final.csv')

    def output(self):
        return luigi.LocalTarget(os.getcwd()+"/data_final.csv")

class Task1(luigi.Task):
    def requires(self):
        yield Task0()

    def run(self):
        df_data = pd.read_csv(Task0().output().path)
        df_data.loc[(df_data['Location'].str.contains("No location")==True),'Status'] = 'Inactive'
        df_data.loc[(df_data['Location'].str.contains("No Location")==True),'Status'] = 'Inactive'
        df_data.loc[(df_data['Status'].isnull()),'Status'] = 'Active'

        cols = df_data.columns.tolist()
        column_to_move = "Status"
        new_position = 4
        cols.insert(new_position, cols.pop(cols.index(column_to_move)))
        df_data = df_data[cols]

        df_data.to_csv(self.output().path,index=False, encoding='utf8')
        print('Task1 Completed')

    def output(self):
        return luigi.LocalTarget(os.getcwd()+"/data_final_status.csv")

class Task2(luigi.Task):
    def requires(self):
        yield Task1()
    def run(self):
        df = pd.read_csv(Task1().output().path)
        df['Finance']=df.iloc[:,5:57].sum(axis=1)
        df['Technology']=df.iloc[:,57:107].sum(axis=1)
        df.insert(loc=111, column='diff',value='')
        df.insert(loc=112, column='Percent',value='')
        df['diff'] = df['Finance']-df['Technology']
        df['Percent'] = ((df['Technology'])/(df['Finance']+df['Technology']))*100
        df.loc[((df['Finance'] >= 25)&(df['Technology'] >= 25)),'Fintech'] = 'True'
        df.loc[((df['Finance'] >= 25)&(df['Technology'].between(15, 25, inclusive=True))&(df['Percent'].between(43, 55, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'] >= 25)&(df['Finance'].between(15, 25, inclusive=True))&(df['Percent'].between(43, 55, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Finance'] >= 15)&(df['Technology'].between(10, 15, inclusive=True))&(df['Percent'].between(42, 58, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'] >= 15)&(df['Finance'].between(10, 15, inclusive=True))&(df['Percent'].between(42, 58, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Finance'] >= 10)&(df['Technology'].between(10, 15, inclusive=True))&(df['Percent'].between(40, 60, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'] >= 10)&(df['Finance'].between(10, 15, inclusive=True))&(df['Percent'].between(40, 60, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Finance'] >= 10)&(df['Technology'].between(5, 10, inclusive=True))&(df['diff'].between(0,4, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'] >= 10)&(df['Finance'].between(5, 10, inclusive=True))&(df['diff'].between(0,-5, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'].between(5, 10, inclusive=True))&(df['diff'].between(-5,3, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Finance'].between(5, 10, inclusive=True))&(df['diff'].between(-3,3, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Finance'] == 0)&(df['diff'].between(-6, 0, inclusive=True))),'Fintech'] = '1'
        df.loc[((df['Technology'] == 0)&(df['diff'].between(0, 3, inclusive=True))),'Fintech'] = '1'
        df.loc[(df['Position'].str.contains("Teller")==True),'Fintech'] = '0'
        df.loc[(df['Position'].str.contains("client-service")==True),'Fintech'] = '0'
        df.loc[(df['Position'].str.contains("teller")==True),'Fintech'] = '0'
        df.loc[(df['Position'].str.contains("customer")==True),'Fintech'] = '0'
        df.loc[(df['Position'].str.contains("Banker")==True),'Fintech'] = '0'
        df.loc[(df['Fintech'].isnull()),'Fintech'] = '0'
        #df.to_csv("Z:/ADS/Assignemnt2/luigi/fintech.csv",index=False, encoding='utf8')

        df.to_csv(self.output().path,index=False, encoding='utf8')
        print('Task2 Completed')

    def output(self):
        return luigi.LocalTarget(os.getcwd()+"/fintech.csv")

class Task3(luigi.Task):
    def requires(self):
        yield Task2()
    def run(self):
        df1 = pd.read_csv(Task2().output().path)
        df1['Payment Non 0']=df1.iloc[:,5:16].astype(bool).sum(axis=1)
        df1['Blockchain Non 0']=df1.iloc[:,16:21].astype(bool).sum(axis=1)
        df1['Trading Non 0']=df1.iloc[:,21:36].astype(bool).sum(axis=1)
        df1['Investment Non 0']=df1.iloc[:,37:44].astype(bool).sum(axis=1)
        df1['Lending Non 0']=df1.iloc[:,44:53].astype(bool).sum(axis=1)
        df1['Insurance Non 0']=df1.iloc[:,53:59].astype(bool).sum(axis=1)
        df1['Data & analytics Non 0']=df1.iloc[:,59:80].astype(bool).sum(axis=1)
        df1['Security Non 0']=df1.iloc[:,80:96].astype(bool).sum(axis=1)
        df1['Software Non 0']=df1.iloc[:,96:108].astype(bool).sum(axis=1)


        df1.loc[(df1['Payment Non 0']>2),'Payment Hit']=1
        df1.loc[(df1['Payment Hit'].isnull()),'Payment Hit']=0

        df1.loc[(df1['Blockchain Non 0']>2),'Blockchain Hit']=1
        df1.loc[(df1['Blockchain Hit'].isnull()),'Blockchain Hit']=0

        df1.loc[(df1['Lending Non 0']>2),'Lending Hit']=1
        df1.loc[(df1['Lending Hit'].isnull()),'Lending Hit']=0

        df1.loc[(df1['Investment Non 0']>2),'Investment Hit']=1
        df1.loc[(df1['Investment Hit'].isnull()),'Investment Hit']=0

        df1.loc[(df1['Lending Non 0']>2),'Lending Hit']=1
        df1.loc[(df1['Lending Hit'].isnull()),'Lending Hit']=0

        df1.loc[(df1['Insurance Non 0']>2),'Insurance Hit']=1
        df1.loc[(df1['Insurance Hit'].isnull()),'Insurance Hit']=0

        df1.loc[(df1['Data & analytics Non 0']>2),'Data & analytics Hit']=1
        df1.loc[(df1['Data & analytics Hit'].isnull()),'Data & analytics Hit']=0

        df1.loc[(df1['Security Non 0']>2),'Security Hit']=1
        df1.loc[(df1['Security Hit'].isnull()),'Security Hit']=0

        df1.loc[(df1['Software Non 0']>2),'Software Hit']=1
        df1.loc[(df1['Software Hit'].isnull()),'Software Hit']=0

        df1.to_excel(self.output().path,index=False, encoding='utf8')
    def output(self):
        return luigi.LocalTarget(os.getcwd()+"/Fintech_Data.xlsx")

class Task4(luigi.Task):
    def requires(self):
        yield Task3()
    def run(self):
        file = ''
        try:
            dbx = dropbox.Dropbox('aDf1htlkmN8AAAAAAAAC-_IjjyFsEJBJU6fY86Y32dr1LH3kVthriApkX9h08kmf')

            with open(Task3().output().path, 'rb') as upxlsx:
                dbx.files_upload(upxlsx.read(),'/DataScienceTeam9/Fintech_Data.xlsx', mode=dropbox.files.WriteMode("overwrite"))

        except Exception as e:
            print(e)
        print('success')
    def output(self):
        return luigi.LocalTarget(os.getcwd()+"/Fintech_Data.xlsx")
class Task5(luigi.Task):
    def requires(self):
        yield Task4()
    def run(self):
        try:
            os.remove(os.getcwd()+'/data_final.csv')
            os.remove(os.getcwd()+'/Fintech_Data.xlsx')
            os.remove(os.getcwd()+"/fintech.csv")
            os.remove(os.getcwd()+"/data_final_status.csv")
            os.system('python -m webbrowser -t "https://us-east-1.online.tableau.com/t/r7odinson/views/DataScienceAssignment2/JobCategories?iframeSizedToWindow=true&:embed=y&:showAppBanner=false&:display_count=no&:showVizHome=no"')
            print('Please check your Browser')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    luigi.run()
