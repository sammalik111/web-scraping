from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests

# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"

An example of that within the function would be:
    open("filename", "r", encoding="utf-8-sig")

There are a few special characters present from Airbnb that aren't defined in standard UTF-8 (which is what Python runs by default). This is beyond the scope of what you have learned so far in this class, so we have provided this for you just in case it happens to you. Good luck!
"""

def get_listings(html_file): 
    """
    Parses an HTML file to extract Airbnb listings' titles and IDs.

    Args:
        html_file (str): Path to the HTML file containing Airbnb listings.

    Returns:
        list: A list of tuples, each containing the listing title and listing ID.
    """
    # pass 
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup.prettify())
    
    # setup the pattern and list of tuples
    pattern = r'www\.airbnb\.com/rooms/(plus/)?(\d+)'

    tuples = []
    
    # get all the links
    links = soup.findAll('meta') 
    # loop through the links
    for link in links:
        print(link)
                
        # get just the link value
        href_val = link.get('content')
        # if the link value has the pattern
        if href_val is not None and re.search(pattern, href_val):
            print(href_val)
            # get the link value that matches the pattern
            val = re.search(pattern, href_val).group()
            # seperate into just the numeric value
            val = re.search(r'\d+', val).group()
            print(val)
            
            # Find the next <div> element immediately after the current link
            next_div = link.find_next('div')
            next_div = next_div.find_next('div')
            next_div = next_div.find_next('div')
            next_div = next_div.find_next('div')
            next_div = next_div.find_next('div')
            title = next_div.find_next('div').get_text()
            tuple = (title, val)
            tuples.append(tuple)
    return tuples    

def get_listing_data(listing_id): 
    """
    Retrieves specific details of an Airbnb listing based on its ID.

    Args:
        listing_id (str): The ID of the Airbnb listing.

    Returns:
        tuple: A tuple containing policy number, place type, number of reviews, and nightly price.
    """
    # pass
    html_file = 'html_files/listing_' + listing_id + '.html'
    
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
            
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # reviews num
    reviews = soup.find('span', {'class': '_s65ijh7'})
    if reviews is None:
        reviews = 0
    else:
        reviews = reviews.get_text()
        pattern = r'\d+'
        reviews = re.search(pattern, reviews).group()
    
    # price num
    price = soup.find('div', {'class': '_1jo4hgw'}).get_text()
    pattern = r'\d+'
    price = re.search(pattern, price).group()
    
    # policy num
    # classList = soup.findAll('span', {'class': 'll4r2nl dir dir-ltr'})
    # for items in classList:
    #     if items.get_text() == 'Pending' or items.get_text() == 'pending':
    #         policy = 'Pending'
    #         break
    #     elif items.get_text() == 'Exempt' or items.get_text() == 'exempt':
    #         policy = 'Exempt'
    #         break
    #     else:
    #         if re.search(r'STR-\d+', items.get_text()):
    #             policy = re.search(r'STR-\d+', items.get_text()).group()
    #             policy = policy.replace('STR-', '')
    #             break
    #         elif re.search(r'\d+-\d+STR', items.get_text()):  
    #             policy = re.search(r'\d+-\d+STR', items.get_text()).group()
    #             break
    
    policyLi = soup.find('li', {'class': 'f19phm7j dir dir-ltr'})
    policy = policyLi.find('span', {'class': 'll4r2nl dir dir-ltr'}).get_text()
    if policy == 'Pending' or policy == 'pending':
        policy = 'Pending'
    elif policy == 'Exempt' or policy == 'exempt':
        policy = 'Exempt'
    # print (policy)
            
            
    # place type
    subtitle = soup.find('h2', {'class': '_14i3z6h'}).get_text()
    if subtitle is None or subtitle == '':
        otherTitle = soup.find('div', {'class': '_kh3xmo'}).get_text()
        subtitle = otherTitle
        
    pattern = r'private'
    pattern2 = r'Private'
    pattern3 = r'shared'
    pattern4 = r'Shared'
    pattern5 = r'entire'
    pattern6 = r'Entire'
    if re.search(pattern, subtitle) or re.search(pattern2, subtitle):
        place_type = 'Private Room'
    elif re.search(pattern3, subtitle) or re.search(pattern4, subtitle):    
        place_type = 'Shared Room'
    elif re.search(pattern5, subtitle) or re.search(pattern6, subtitle):
        place_type = 'Entire Room'
        
        
    tuple = (policy, place_type, int(reviews), int(price))
    
    return tuple

def create_detailed_listing_data(html_file): 
    """
    Creates a complete list of Airbnb listings with additional details.

    Args:
        html_file (str): Path to the HTML file containing Airbnb listings.

    Returns:
        list: A list of tuples, each containing detailed listing information.
    """
    # pass
    tuples = []
    listings = get_listings(html_file)
    for listing in listings:
        listing_id = listing[1]
        listing_data = get_listing_data(listing_id)
        tuple = (listing[0], listing[1], listing_data[0], listing_data[1], listing_data[2], listing_data[3])
        tuples.append(tuple)
    return tuples

def output_csv(data, filename): 
    """
    Writes Airbnb listing data to a CSV file in ascending order of nightly rates.

    Args:
        data (list): A list of tuples containing listing information.
        filename (str): The name of the CSV file to be created.

    Returns:
        None
    """
    # Implementation details...

def validate_policy_numbers(data):
    """
    Validates policy numbers in Airbnb listing data.

    Args:
        data (list): A list of tuples containing listing information.

    Returns:
        list: A list of tuples with invalid policy numbers, containing listing name and ID.
    """
    # Implementation details...

# EXTRA CREDIT
def get_google_scholar_articles(query): 
    """
    Retrieves article titles from Google Scholar search results.

    Args:
        query (str): The search query for Google Scholar.

    Returns:
        list: A list of article titles from the first page of search results.
    """
    # Implementation details...

# Test cases and main function...

if __name__ == '__main__':
    unittest.main(verbosity=2)
    #main()
