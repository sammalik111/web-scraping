Airbnb Data Scraper
This Python script is designed to scrape data from Airbnb listings in San Francisco, validate policy numbers, and output the data to a CSV file. Below are the functions and their descriptions:

Functions
get_listings(html_file)
Input: HTML file path
Output: List of tuples containing listing title and listing ID
Description: Parses an HTML file, extracts listing titles and IDs from the content, and returns them as a list of tuples.
get_listing_data(listing_id)
Input: Listing ID as a string
Output: Tuple containing policy number, place type, number of reviews, and nightly price
Description: Scrapes specific details (policy number, place type, number of reviews, and nightly price) for a given listing ID from Airbnb listings.
create_detailed_listing_data(html_file)
Input: HTML file path
Output: List of tuples containing detailed listing information
Description: Combines the output of get_listings() and get_listing_data() to create a complete list of Airbnb listings with additional details. Returns a list of tuples with six elements each.
output_csv(data, filename)
Input: List of tuples and a filename for the CSV output
Output: CSV file containing listing data
Description: Writes the data in ascending order of nightly rates to a CSV file with specified column headers.
validate_policy_numbers(data)
Input: List of tuples containing listing information
Output: List of tuples with invalid policy numbers
Description: Validates policy numbers in the data and returns a list of tuples containing the names and IDs of listings with invalid policy numbers.
get_google_scholar_articles(query) (Extra Credit):
Input: Query string for Google Scholar search
Output: List of article titles from the first page of search results
Description: Sends a request to Google Scholar with the provided query, retrieves article titles from the first page of search results, and returns them as a list.
Important Note
If you encounter "encoding errors" while opening, reading, or writing files, use encoding="utf-8-sig" as an argument in your open() function. This is necessary to handle special characters present in Airbnb data.

Running the Script
Ensure you have the required Python libraries (BeautifulSoup, re, os, csv, unittest, requests) installed.

Uncomment the line main() at the end of the script to run the scraping and data validation process. This will create a CSV file named airbnb_dataset.csv and print listings with invalid policy numbers.

For unit testing, run the script with unittest.main(verbosity=2) uncommented. This will execute a set of tests to check the functionality of the script.

Enjoy scraping Airbnb data in San Francisco!
