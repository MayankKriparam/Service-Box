#Single_phase_motor_page=1-5

#Importing the Libraries
import requests
from bs4 import BeautifulSoup

#Creating a base link
link = 'https://www.industrybuying.com/motors-power-transmission-548/single-phase-motor-2873/?page=1'

#A list to store all the data in form of a dictionary
my_list = []

base_result = requests.get(link)
base_src = base_result.content
soup = BeautifulSoup(base_src, 'lxml')

#Base variables defined to traverse to the next page
p=2

#Looping till the last page of the current directory
#soup.find('link', attrs={'rel':'next'}) != None
while(p<6):
    
    #Capturing the parent tag
    table = soup.find_all('div', attrs={'class':'AH_ProductView col-lg-3 col-md-3 col-sm-6 col-xs-6 productThumbnails'})
    
    #Extracting the useful info at a single page
    for i in range(len(table)):
        if(table[i].find('div', attrs={'class':'proPriceBox'}).div.text != 'Quote Only'):
            for row in table[i].find_all('div', attrs={'class':'prFeature'}):
                quote = {}
                quote['name'] = row.a.text
                quote['brand'] = row.span.text
                raw_price = table[i].find('div', attrs={'class':'proPriceBox'}).span.text
                #print(raw_price)
                #price = [x.replace('\n', '').replace(' ', '') for x in raw_price]       This doesn't work correctly
                price = raw_price.replace('\n', '').replace(' ', '')
                #print(price)
                quote['price'] = price
                my_list.append(quote)
    
    next_page = "?page=" + str(p)
    #print(next_page)
    current_page = "?page=" + str(p-1)
    #print(current_page)
    link = link.replace(current_page, next_page)
    #print(p)
    p = p + 1
    
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')


print(len(my_list))
print(my_list)
