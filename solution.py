# Each entry of the data set consists of following fields separated by ;
# character:
#
#     datacenter                                            
#     hostname                                              
#     disk serial                                           
#     disk age (in s)                                       
#     total reads                                           
#     total writes                                          
#     average IO latency from 5 minutes (in ms)             
#     total uncorrected read errors                         
#     total uncorrected write errors                        
#
# The proper solution (a script in Python) should output following
# information:
#
##     How many disks are in total and in each DC                              
##     Which disk is the youngest/oldest one and what is its age (in days)     
##     What's the average disk age per DC (in days)                            
##     How many read/write IO/s disks processes on average                     
##     Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)
##     Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)
#
## There should also be tests that verify if parts of the script are processing data properly.



######################### SOLUTION ###########################

# %% Wstęp
from IPython.display import display
import math
import pandas as pd

#przypisanie nagłówków
head = ['datacenter',                                           
    'hostname',                                              
    'disk serial',                                           
    'disk age (in s)',                                       
    'total reads',                                           
    'total writes',                                          
    'average IO latency from 5 minutes (in ms)',            
    'total uncorrected read errors',                         
    'total uncorrected write errors',]

#odczyt pliku
df=pd.read_csv('datacopy.raw',sep=';',names=head)
df
# %%How many disks are in total and in each DC   

#długość kolumny z indeksami = ilości wierszy
Total_number_of_disks=len(df.index) 
display(Total_number_of_disks)

# #nowa kolumna ['count']
df['count']=1
#grupowanie po wartosciach kolumny 'datacenter' i zliczanie dysków, wyswietlamy kolumne count
df.groupby(['datacenter']).count()['count']


# %% Which disk is the youngest/oldest one and what is its age (in days)

#za pomocą metody max() znajdujemy najwieksza wartosc w podanej kolumnie
oldest_disk=df['disk age (in s)'].max()
display(round(oldest_disk/86400))
#za pomocą metody min() znajdujemy najmniejsza wartosc w podanej kolumnie
youngest_disk=df['disk age (in s)'].min()
#wyswietlamy wynik z dokladnoscia do dnia zaokragalajac w górę aby uniknac wartosci 0
display(math.ceil(youngest_disk/86400))


# %%What's the average disk age per DC (in days)

#wyświetlamy średnią wieku dysków w każdym DC, za pomocą grupowania i metody mean()
#uzyskany wynik przekładamy na dni i zaokrąglamy
average_per_DC=round((df.groupby('datacenter')['disk age (in s)'].mean())/86400)
display(average_per_DC)


# %% How many read/write IO/s disks processes on average
averageIO=pd.DataFrame()                                           #tworzymy nową dataframe
averageIO['disk serial']=df['disk serial']                         #na bazie poprzedniej
averageIO['Avr_reads/s']=df['total reads']/df['disk age (in s)']   #średnia odczytów/s
averageIO['Avr_writes/s']=df['total writes']/df['disk age (in s)'] #średnia zapisów/s
display(averageIO)

#Łączna średnia odczytu wszystkich dysków 
total_reads_average=averageIO['Avr_reads/s'].mean()
print(f"{round(total_reads_average,2)}/s")

#łączna średnia zapisu wszystkich dysków
total_writes_average=averageIO['Avr_writes/s'].mean()
print(f"{round(total_writes_average,2)}/s")


# %% Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)
#TOP 5 wyświetlamy 2 kolumny, sortujemy wedlug polecenia,wyswietlamy top 5
display(averageIO[['Avr_reads/s','disk serial']].sort_values(by=['Avr_reads/s'],ascending=False).head(5))   #READS
display(averageIO[['Avr_writes/s','disk serial']].sort_values(by=['Avr_writes/s'],ascending=False).head(5))  #WRITES

#WORST 5
display(averageIO[['Avr_reads/s','disk serial']].sort_values(by=['Avr_reads/s'],ascending=True).head(5))   #READS
display(averageIO[['Avr_writes/s','disk serial']].sort_values(by=['Avr_writes/s'],ascending=True).head(5))  #WRITES


# %%Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)
# tworzymy nową dataframe errors na podstawie danych z df
# za pomocą polecenia loc wyszukujemy wiersze w ktorych w wystąpiły błędy odczytu lub zapisu
errors=df.loc[(df['total uncorrected read errors']!=0) | (df['total uncorrected write errors']!=0)]
#wyświetlamy interesujące nas wartości (wszystkie wiersze, oraz kolumny 2,7,8)
display(errors.iloc[:,[2,7,8]])            

# %%TESTY

#1 Czy liczba dysków jest równa oczekiwanej
assert Total_number_of_disks == 25000
#2 Czy łączna liczba dysków każdego DC jest równa oczekiwanej
assert sum(df.groupby(['datacenter']).count()['count'])==25000
#3 Czy Najstarszy dysk w przeliczeniu na dni ma ich 2074
assert round(oldest_disk/86400)==2074
#4 -,,- najmłodszy -,,- 0
assert math.ceil(youngest_disk/86400)==1
#5 Czy średnia wieku wszystkich dysków jest równa 735
assert sum(average_per_DC)/5==735
#6 Sprawdzanie danych na konkretnych komórkach
assert df.iloc[100]['total reads']/df.iloc[100]['disk age (in s)']==averageIO.iloc[100]['Avr_reads/s']
#7 Czy liczba występujących błędów jest równa liczbie niesprawnych dysków
assert len(errors.index)==8


# %%
