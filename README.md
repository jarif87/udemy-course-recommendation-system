# Udemy Course Recommendation System

A web application built with Flask to analyze Udemy course data and provide course recommendations. The dashboard visualizes key metrics such as subscribers by domain, courses by level, and profit trends, using Chart.js for interactive charts. The recommendation system suggests courses based on user input.

## Features
- **Interactive Dashboard**: Visualizes course data with seven charts:
  - Subscribers by domain (doughnut chart)
  - Courses by level (doughnut chart)
  - Subscribers by year (bar chart)
  - Profit by year (bar chart)
  - Profit by month (bar chart)
  - Subscribers by month (bar chart)
  - Subscribers per subject category (line chart)
- **Course Recommendation**: Suggests relevant courses based on user queries (not fully implemented in provided code).
- **Robust Error Handling**: Handles missing or invalid data gracefully, displaying "No data available" for empty charts.
- **Logging**: Backend logs errors and data processing details for debugging.

## Tech Stack
- **Backend**: Python, Flask, Pandas
- **Frontend**: HTML, Bootstrap 4, Chart.js
- **Data Processing**: Pandas for analyzing `UdemyCleanedTitle.csv`
- **Dependencies**: Listed in `requirements.txt`

## Project Structure
```
udemy-course-recommendation-system/
│
├── app.py                  # Main Flask application
├── dashboard.py            # Data processing for dashboard
├── templates/
│   ├── dashboard.html      # Dashboard template
│   └── index.html          # Home page (assumed)
├── static/                 # Static files (if any)
├── UdemyCleanedTitle.csv   # Dataset
├── dashboard.log           # Backend logs
├── app.log                 # Flask logs
├── requirements.txt        # Dependencies
├── Procfile                # Heroku process configuration
├── README.md               # Project documentation
└── .gitignore              # Git ignore file

```

## Prerequisites
- Python 3.8+
- Git
- Web browser (Chrome, Firefox, etc.)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/udemy-course-recommendation-system.git
   cd udemy-course-recommendation-system

2. **Create a Virtual Environment**
```

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install Dependencies**
```
pip install -r requirements.txt

```
4. **Prepare the Dataset**

* Ensure UdemyCleanedTitle.csv is in the project root.

* Required columns: course_id, course_title, url, price, num_subscribers, subject, level, published_timestamp.

* Example format:

```
course_id,course_title,url,price,num_subscribers,subject,level,published_timestamp
1,Python Course,http://example.com,10.0,100,Programming,Beginner,2020-01-01T12:00:00Z
```

5. **Run the Application**

```
python app.py
```

## Usage

- Dashboard: View visualizations of Udemy course data metrics. If data is missing, charts display "No data available."

- Logs: Check app.log and dashboard.log for debugging data processing or Flask errors.

- Recommendation: Enter a query on the home page (if implemented) to get course suggestions

