import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gradio as gr

# Function to scrape headlines from a news website
def scrape_news(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Will raise an error for invalid HTTP response (e.g., 404, 500)

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Inspect the page to figure out which HTML elements contain the headlines
        headlines = soup.find_all(['h2', 'h3', 'h4'])  # Searching for different headline levels

        # Create filename with current date and time
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        folder = "news_headlines"
        os.makedirs(folder, exist_ok=True)
        
        # Save the headlines to a txt file
        with open(os.path.join(folder, filename), "w") as file:
            if not headlines:
                file.write("No headlines found.\n")
            else:
                for idx, headline in enumerate(headlines, 1):
                    text = headline.get_text(strip=True)
                    if text:  # Ignore empty text
                        file.write(f"{idx}. {text}\n")
        
        # Return headlines to display on the webpage
        if not headlines:
            return "No headlines found."
        else:
            return "\n".join(f"{idx}. {headline.get_text(strip=True)}" for idx, headline in enumerate(headlines, 1))
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching the website: {e}"

# URL of the news website (change to any news website you like)
news_url = "https://www.bbc.com/news"  # Example URL: BBC News

# Create Gradio interface to display the news and refresh button
def show_news():
    return scrape_news(news_url)

interface = gr.Interface(fn=show_news, inputs=[], outputs="text", live=True)
interface.launch()
