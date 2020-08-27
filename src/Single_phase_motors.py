#Single_phase_motor_page=1

#Importing the Libraries
import requests
from bs4 import BeautifulSoup
#import csv

#Creating a base link
link = 'https://www.industrybuying.com/motors-power-transmission-548/single-phase-motor-2873/?page=1'
website_link = 'https://www.industrybuying.com/'

#A list to store all the data in form of a dictionary
my_list = []

base_result = requests.get(link)
base_src = base_result.content
base_soup = BeautifulSoup(base_src, 'lxml')

#Base variables defined to traverse to the next page
page=1

#Looping till the last page of the current directory
#soup.find('link', attrs={'rel':'next'}) != None
while(page<6):

    #Capturing the parent tag
    table = base_soup.find_all('div', attrs={'class':'AH_ProductView col-lg-3 col-md-3 col-sm-6 col-xs-6 productThumbnails'})

    #Extracting the useful info at a single page
    for i in range(len(table)):
        if(table[i].find('div', attrs={'class':'proPriceBox'}).div.text != 'Quote Only'):
            for row in table[i].find_all('div', attrs={'class':'prFeature'}):
                #print(i)
                quote = {}
                #quote['Name'] = row.a.text
                quote['Brand'] = row.span.text
                #quote['Product Link'] = row.a['href']
                #print(table[i].find('div', attrs={'class':"proPriceBox"}).span)

                #Extracting information from individual product pages

                #Defining the link for the product's page
                product_page_referral = row.a['href']
                #print(product_page_referral)
                product_page_link = website_link + (product_page_referral)
                #print(product_page_link)

                #Making a product soup --- I'm lovin' it xD
                product_result = requests.get(product_page_link)
                product_src = product_result.content
                product_soup = BeautifulSoup(product_src, 'lxml')

                #Line1495
                product_table = product_soup.find('div', attrs={'class':'tabDetailsContainer pad0'})
                product_subtable = product_table.find_all('div', attrs={'class':'filterRow'})


                for j in range(len(product_subtable)):
                    print(j)
                    if(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'SKU'):
                        quote['SKU'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Type of Product'):
                        quote['Type'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Pole'):
                        quote['Number of Poles'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Mounting'):
                        quote['Mounting'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Rated Voltage'):
                        quote['Rated Voltage'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Speed'):
                        quote['Synchronous Speed'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Casing'):
                        quote['Casing'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Body'):
                        quote['Body Type'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Winding'):
                        quote['Winding Type'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    elif(product_subtable[j].find('div', attrs={'class':'featureNamePr'}) == 'Rated Power'):
                        quote['Rated Power'] = product_subtable[j].find('div', attrs={'class':'featureValuePr'}).text
                    print("\n")


                if(table[i].find('span', attrs={'class':"rs"}) != None):
                    raw_price = table[i].find('span', attrs={'class':"rs"}).text
                    #print(raw_price)
                    price = raw_price.replace('\n', '').replace(' ', '').replace('Rs.', '').replace('/Piece', '')
                    #print(price)
                    quote['Price per piece(INR)'] = price
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
                    quote['Price per piece(INR)'] = raw_price_alt1
                my_list.append(quote)

    current_page = "?page=" + str(page)
    #print(current_page)
    next_page = "?page=" + str(page+1)
    #print(next_page)
    link = link.replace(current_page, next_page)
    print(page)
    page = page + 1

    result = requests.get(link)
    src = result.content
    base_soup = BeautifulSoup(src, 'lxml')


print(len(my_list))
#print(my_list)

#Field names for the csv file columns
#fields = ['Name', 'Brand', 'Price per piece(INR)']

#Name of the csv file generated
#filename = "Single_phase_motors.csv"

#Writing to the csv file
#with open(filename, 'w') as f:
#    writer = csv.DictWriter(f, fieldnames = fields)
#    writer.writeheader()
#    
#    writer.writerows(my_list)
