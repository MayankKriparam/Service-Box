#Single_phase_motor_page=1

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
page=1

#Looping till the last page of the current directory
#soup.find('link', attrs={'rel':'next'}) != None
while(page<6):

    #Capturing the parent tag
    table = soup.find_all('div', attrs={'class':'AH_ProductView col-lg-3 col-md-3 col-sm-6 col-xs-6 productThumbnails'})

    #Extracting the useful info at a single page
    for i in range(len(table)):
        if(table[i].find('div', attrs={'class':'proPriceBox'}).div.text != 'Quote Only'):
            for row in table[i].find_all('div', attrs={'class':'prFeature'}):
                #print(i)
                quote = {}
                quote['name'] = row.a.text
                quote['brand'] = row.span.text
                #print(table[i].find('div', attrs={'class':"proPriceBox"}).span)

                if(table[i].find('span', attrs={'class':"rs"}) != None):
                    raw_price = table[i].find('span', attrs={'class':"rs"}).text
                    #print(raw_price)
                    price = raw_price.replace('\n', '').replace(' ', '')
                    #print(price)
                    quote['price'] = price
                elif(table[i].find('div', attrs={'class':"proPriceSpan family"}) != None):
                    raw_price = table[i].find('div', attrs={'class':"proPriceSpan family"}).text
                    #print(raw_price)
                    #raw_price_alt = raw_price.replace('Price Range:', '').replace(' ', '').replace('\n', '')
                    raw_price_alt = raw_price.replace(',', '')
                    numbers = []
                    for word in raw_price_alt.split():
                       if word.isdigit():
                          numbers.append(int(word))
                    #print (numbers)
                    raw_price_alt1 = max(numbers)
                    #print(raw_price_alt1)
                    quote['price'] = raw_price_alt1
                my_list.append(quote)

    current_page = "?page=" + str(page)
    #print(current_page)
    next_page = "?page=" + str(page+1)
    #print(next_page)
    link = link.replace(current_page, next_page)
    #print(page)
    page = page + 1

    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')


#print(len(my_list))
#print(my_list)

