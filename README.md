# Image Scraper Web App

This is an end-to-end Image Scraping web application built using Flask and BeautifulSoup.

## Features
- User can enter any image keyword
- App scrapes images from Google Images
- Images are downloaded automatically
- Images are displayed on the web page
- API endpoint available for scraping

## Tech Stack
- Python
- Flask
- BeautifulSoup
- Requests
- HTML

## How to Run Project

1. Clone the repository
2. Create virtual environment
3. Install requirements
   pip install -r requirements.txt
4. Run the app
   python app.py
5. Open browser
   http://127.0.0.1:5000

## API Endpoint

POST: /api/scrape  
Body:
{
  "query": "nokia 2690"
}

Response:
{
  "query": "nokia 2690",
  "total_images": 20
}

## Project Type
End-to-End Python Web Scraping Project
