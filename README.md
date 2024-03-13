# LinkedIn Profile Scraper

This project is a LinkedIn Profile Scraper built with Python using Selenium and BeautifulSoup libraries. It allows you to fetch LinkedIn profiles based on first name and last name, providing information such as name, profile URL, title, and location.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MunjPatel/LinkedInProfileScraper.git
    ```

2. Install dependencies:

    ```bash
    pip install pandas selenium
    ```

3. Ensure you have Chrome browser installed.

4. Download the ChromeDriver matching your Chrome browser version and place it in the project directory.

## Usage

1. Open the `instance.py` file.

2. Update the `first_name` and `last_name` variables with the names of the individuals whose LinkedIn profiles you want to fetch.

3. Run the `instance.py` file:

    ```bash
    python instance.py
    ```

4. The script will fetch LinkedIn profiles based on the provided names and print the results to the console.

## Options

- To run the script in headless mode, uncomment the `options.add_argument("--headless")` line in the `initilize_driver` function.

## Example

```python
profiles = PLinkedInProfileScraper()

profile_data = profiles.fetch_profiles(pprofile_scraper_instance=profiles, first_name="Munj", last_name="Patel")
print(profile_data)
