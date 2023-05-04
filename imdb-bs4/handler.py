import os
import json
import sys
from bs4 import BeautifulSoup
import boto3
import requests
import time


def scrape(event, context={}):
    data = rated_movies_scrape()
    save_file_to_s3( "top_rated_movies_" + time.strftime("%m-%d-%YT%H:%M:%S") + ".json", data)


def rated_movies_scrape():
    html = requests.get("https://www.imdb.com/chart/top/").content

    soup = BeautifulSoup(html, 'html.parser')

    top_rated_movies = soup.find("tbody", class_="lister-list")

    result = []

    for child in top_rated_movies.find_all("tr"):
        title = child.find("td", class_="titleColumn")
        result.append({
            'title': title.a.string,
            'year': title.span.string[1: -1],
            'rate': child.find("td", class_="imdbRating").strong.string,
        })

    print(result)
    return result


def save_file_to_s3(file_name, data):
    s3 = boto3.client('s3')

    s3.put_object(
        Body=json.dumps(data),
        Key=file_name,
        Bucket=os.getenv('S3_BUCKET_NAME'),
    )


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
