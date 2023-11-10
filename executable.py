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
    # pass
    sorted_tuples = sorted(data, key=lambda x: x[5])
    
    # Add labels
    labels = "Listing Title,Listing ID,Policy Number,Place Type,Number of Reviews,Nightly Rate"

    # Open the output file in write mode
    with open(filename, 'w') as outfile:
        # Write the labels as the first line in the file
        outfile.write(labels + '\n')
        # Write each sorted tuple to the file
        for item in sorted_tuples:
            outfile.write(','.join(map(str, item)) + '\n')

def validate_policy_numbers(data):
    """
    Validates policy numbers in Airbnb listing data.

    Args:
        data (list): A list of tuples containing listing information.

    Returns:
        list: A list of tuples with invalid policy numbers, containing listing name and ID.
    """
    # pass 
    lists = []
    for item in data:
        if  item[2] == 'Pending' or item[2] == 'Exempt':
            continue
        else:
            if re.search(r'20\d\d-00\d\d\d\dSTR', item[2]) or re.search(r'STR-000\d\d\d\d', item[2]):
                continue
            else:
                lists.append((item[0], item[1]))
    return lists

# EXTRA CREDIT
def get_google_scholar_articles(query): 
    """
    Retrieves article titles from Google Scholar search results.

    Args:
        query (str): The search query for Google Scholar.

    Returns:
        list: A list of article titles from the first page of search results.
    """
    # pass
    # Create a URL for the Google Scholar search
    url = f'https://scholar.google.com/scholar?q={query}'

    try:
        # Send a GET request to Google Scholar
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the titles on the first page of results
            titles = [title.text for title in soup.find_all('h3', {'class': 'gs_rt'})]

            return titles

        else:
            print(f"Failed to retrieve Google Scholar results. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


# Test cases and main function...
class TestCases(unittest.TestCase):

    def test_get_listings(self):
        # call get_listings("html_files/search_results.html")
        # and save to a local variable
        listings = get_listings("html_files/search_results.html")

         # check that the number of listings extracted is correct (18 listings)
        self.assertEqual(len(listings), 18)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)

        # check that each item in the list is a tuple
        for listing in listings:
            self.assertEqual(type(listing), tuple)
        # check that the first title and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[0], ('Loft in Mission District', '1944564'))
        # check that the last title and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[-1], ('Guest suite in Mission District', '467507'))

    def test_get_listing_data(self):
        html_list = ["467507",
                     "1550913",
                     "1944564",
                     "4614763",
                     "6092596"]
        
        # call get_listing_data for i in html_list:
        listing_informations = [get_listing_data(id) for id in html_list]

        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 4)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
            self.assertEqual(type(listing_information[3]), int)

        # check that the first listing in the html_list has the correct policy number
        self.assertEqual(listing_informations[0][0], 'STR-0005349')
        # check that the last listing in the html_list has the correct place type
        self.assertEqual(listing_informations[-1][1], 'Entire Room')
        # check that the third listing has the correct cost
        self.assertEqual(listing_informations[2][3], 181)

    def test_create_detailed_listing_data(self):
        # call create_detailed_listing_data on "html_files/search_results.html"
        # and save it to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # check that we have the right number of listings (18)
        self.assertEqual(len(detailed_data), 18)

        for item in detailed_data:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6
            self.assertEqual(len(item), 6)

        # check that the first tuple is made up of the following:
        # ('Loft in Mission District', '1944564', '2022-004088STR', 'Entire Room', 422, 181)
        self.assertEqual(detailed_data[0], ('Loft in Mission District', '1944564', '2022-004088STR', 'Entire Room', 422, 181))
        # check that the last tuple is made up of the following:
        # ('Guest suite in Mission District', '467507', 'STR-0005349', 'Entire Room', 324, 165)
        self.assertEqual(detailed_data[-1], ('Guest suite in Mission District', '467507', 'STR-0005349', 'Entire Room', 324, 165))

    def test_output_csv(self):
        # call create_detailed_listing_data on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # call output_csv() on the variable you saved
        output_csv(detailed_data, "test.csv")

        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)

        # check that there are 19 lines in the csv
        self.assertEqual(len(csv_lines), 19)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Listing Title', 'Listing ID', 'Policy Number', 'Place Type', 'Number of Reviews', 'Nightly Rate'])
        # check that the next row is Private room in Mission District,23672181,STR-0002892,Private Room,198,109
        self.assertEqual(csv_lines[1], ['Private room in Mission District', '23672181', 'STR-0002892', 'Private Room', '198', '109'])
        # check that the last row is Guest suite in Mission District,50010586,STR-0004717,Entire Room,70,310
        self.assertEqual(csv_lines[-1], ['Guest suite in Mission District', '50010586', 'STR-0004717', 'Entire Room', '70', '310'])

    def test_validate_policy_numbers(self):
        # call get_detailed_listing_data on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_detailed_listing_data("html_files/search_results.html")

        # call validate_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = validate_policy_numbers(detailed_data)

        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that the elements in the list are tuples
        self.assertEqual(type(invalid_listings[0]), tuple)
        # and that there are exactly two element in each tuple
        self.assertEqual(len(invalid_listings[0]), 2)
        
    def test_get_google_scholars(self):
        self.assertEqual(len(get_google_scholar_articles('airbnb')), 10)
        results = get_google_scholar_articles('airbnb')
        self.assertEqual(results[0], 'Progress on Airbnb: a literature review')
        self.assertEqual(results[5], 'Why tourists choose Airbnb: A motivation-based segmentation study')



if __name__ == '__main__':
    unittest.main(verbosity=2)
    #main()
