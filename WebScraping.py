#importing required libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Fetch the webpage content
webpage = requests.get("https://www.failory.com/startups/india").text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')

# Print the parsed data of html
print(soup.prettify())

# Find all <h3> elements which contain the startup names
articles = soup.find_all('h3')

# Initialize a list to store startup data
data = []

# Loop through each <h3> element to extract startup details
for article in articles:
    startup = {}  # Dictionary to store details of a single startup
    
    # Extract the startup name and remove numbering (e.g., "1) Urban Company" -> "Urban Company")
    startup["name"] = article.text.strip().split(')', 1)[-1].strip()
    
    # Extract the description (the <p> element that comes immediately after the <h3>)
    description = article.find_next('p')
    startup["description"] = description.text.strip() if description else None
    
    # Extract details from the <ul>
    details = article.find_next('ul')
    if details:
        for li in details.find_all('li'):
            key, value = li.text.split(':', 1)     # Split the text into key and value
            key = key.strip()        # Remove extra spaces from the key
            value = value.strip()     # Remove extra spaces from the value

            # Add key-value pairs to the startup dictionary if the key is relevant
            if key in ["Started in", "Founders", "Industries", "Number of employees", "Funding"]:
                startup[key] = value
    
    data.append(startup)   # Append the extracted startup details to the data list


# Print each startup's details (for debugging or verification purposes)
for startup in data:
    print(startup)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(data)

# Rename columns for better readability
df.rename(columns={
    "name": "Company Name",
    "description": "Description",
    "Started in": "Year Founded",
    "Founders": "Founder(s)",
    "Industries": "Industry",
    "Number of employees": "Employee Count",
    "Funding": "Funding Amount"
}, inplace=True)

# Define the desired column order
desired_order = ["Company Name", "Year Founded", "Founder(s)", "Industry", "Funding Amount", "Description", "Employee Count"]

# Reorder the DataFrame columns
df = df[desired_order]

# Display the DataFrame
print(df)

# Save the DataFrame to a text file
df.to_csv('output.txt', sep='\t', index=False)

# Ensure all values in "Number of employees" are strings
if "Employee Count" in df.columns:
    df["Employee Count"] = df["Employee Count"].astype(str)
    df["Employee Count"] = df["Employee Count"].apply(lambda x: f'"{x}"')

# Save the DataFrame to a CSV file
df.to_csv("startups.csv", index=False)


