# Google Search Extractor

A simple Flask web application that accepts a search query, fetches Google search results via SerpAPI, returns structured JSON output, and allows saving the results locally.

## Features

- one input field for search query
- backend API endpoint `/api/search`
- results returned in structured JSON format
- automatic download of `results.json`
- unit tests with `pytest`

## Project structure

```text
GOOGLE-SERP-TEST/
│
├── app/
│   ├── main.py
│   ├── search.py
│   └── templates/
│       └── index.html
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md