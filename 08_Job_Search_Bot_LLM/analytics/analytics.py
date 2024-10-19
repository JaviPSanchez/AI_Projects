import os
import json
import requests
import pandas as pd
import folium
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from fastapi.staticfiles import StaticFiles
import re

app = FastAPI()

print('Loading templates...')
templates = Jinja2Templates(directory="templates")
print('Done!!!')

# Mount the static files directory to serve static content like map.html
app.mount("/static", StaticFiles(directory="static"), name="static")

coordinates_cache = {}
job_data_cache = None

# Load country coordinates from a local JSON file
def load_country_coordinates():
    with open('assets/countries.json', 'r') as file:
        data = json.load(file)
        for country in data:
            coordinates_cache[country['name']] = (country['latitude'], country['longitude'])

# Call the function to preload the coordinates
load_country_coordinates()

# Function to get latitude and longitude of a country from the cache
def get_country_coordinates(country_name: str):
    return coordinates_cache.get(country_name, None)

def process_data():
    global job_data_cache
    print("Calling process_data()...")

    # Disable caching for testing
    # if job_data_cache is not None:
    #     print("Using cached job data.")
    #     return job_data_cache

    with open('../data_folder/output/success.json', 'r') as data_file:
        data = json.load(data_file)

    df = pd.DataFrame(data)
    print("Original Job Locations: ")
    print(df['job_location'])

    if 'job_location' in df.columns:
        # Clean the job_location field to extract only the country name (removing anything in parentheses)
        df['location'] = df['job_location'].apply(lambda x: re.sub(r"\(.*\)", "", x).strip())
        print("Cleaned Job Locations: ")
        print(df['location'])
    else:
        raise KeyError("'job_location' column missing from data")

    job_counts = df['company'].value_counts().to_dict()
    total_jobs = len(df)  # Total number of jobs
    job_data_cache = (total_jobs, job_counts, df)
    
    print(f"Total jobs: {total_jobs}")
    print(f"Processed job data: {job_data_cache}")
    
    return job_data_cache


# Function to create a map of the countries where jobs were applied
def create_map(df):
    print("Generating the map...")
    m = folium.Map(location=[50, 10], zoom_start=2)  # World view map

    # Extract the countries from the job_location data
    country_counts = df['location'].value_counts()
    print(country_counts)

    for country, count in country_counts.items():
        # Fetch coordinates for the country from the cache
        print(f"Fetching coordinates for {country}...")
        coords = get_country_coordinates(country)
        
        if coords:
            lat, lon = coords
            print(f"Adding marker for {country}: {lat}, {lon} with {count} job(s)")
            # Add a marker to the map
            folium.Marker([lat, lon], popup=f"{country}: {count} job(s)").add_to(m)
        else:
            print(f"Coordinates not found for {country}")
    
    # Save the map
    map_path = os.path.join('static', 'map.html')
    m.save(map_path)
    print(f"Map saved to: {map_path}")
    return map_path


# Route for the main page with map
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: Optional[str] = None):
    print("Accessing the root route...")

    try:
        total_jobs, job_counts, df = process_data()
        print(f"Total jobs processed: {total_jobs}")  # Debugging
    except Exception as e:
        print(f"Error in process_data(): {e}")
        return HTMLResponse(content="Error loading data", status_code=500)

    if q:
        job_counts = {k: v for k, v in job_counts.items() if q.lower() in k.lower()}

    map_path = create_map(df)
    
    # Pass total_jobs to the template
    return templates.TemplateResponse("index.html", {
        "request": request,
        "job_counts": job_counts,
        "total_jobs": total_jobs,  # Make sure this is passed
        "map_path": map_path,
        "query": q or ""
    })

# Route to show all job links for a specific company
@app.get("/company/{company_name}", response_class=HTMLResponse)
async def company_jobs(request: Request, company_name: str):
    _, _, df = process_data()
    company_jobs = df[df['company'] == company_name]
    return templates.TemplateResponse("company_jobs.html", {
        "request": request,
        "company_name": company_name,
        "jobs": company_jobs.to_dict(orient='records')
    })
    
    
