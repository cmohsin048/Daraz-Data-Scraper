<h1>Daraz Landline Phones Data Scraper</h1>
This repository contains a web scraper designed to extract data from Daraz.pk. The scraper navigates through multiple pages, collecting detailed information about each product, including the product URL, ID, category, sub-category, rating, reviews, sales, and more. The data is then stored in a Mongodb database for further analysis.
<h2>Features</h2>
<ol>
  <li><h4>Multi-Page Scraping:</h4> The scraper navigates through multiple pages of the Daraz categories, extracting product URLs.</li>
  <li><h4>Detailed Product Data Extraction:</h4> For each product, the scraper collects information such as brand, price, delivery fee, title, total sales, rating, and reviews.</li>
  <li><h4>Error Handling:</h4> The scraper includes robust error handling and retry mechanisms to ensure data accuracy and completeness.</li>
  <li><h4>Database Integration:</h4> Extracted data is stored in a MongoDB database, with updates made for existing records to track sales over time.</li>
  <li><h4>Headless Browsing:</h4> Uses headless ChromeDriver for efficient and automated web scraping.</li>
</ol>
<h2>Technologies Used</h2>
<ol>
  <h4>Python</h4>
  <h4>Selenium WebDriver</h4>
  <h4>MongoDB</h4>
  <h4>ChromeDriver</h4>
</ol>
<h2>Installation</h2>
<ol>
  <li><h4>Clone the repository:</h4> git clone https://github.com/your-username/daraz-landline-phones-scraper.git
</li>
  <li>
    <h4>Install the required packages:</h4> pip install -r requirements.txt
  </li>
  <li>
    Set up your MongoDB connection string in the script.
  </li>
</ol>
<h2>Usage
</h2>
<ol>
  <li><h4>run the script</h4> python scraper.py</li>
  <li>The scraped data will be stored in your specified MongoDB collection.</li>
</ol>

</p>


