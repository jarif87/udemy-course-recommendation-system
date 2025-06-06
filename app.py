from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dashboard import getvaluecounts, getlevelcount, getsubjectsperlevel, yearwiseprofit
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize global variables
df = None
cosine_simi = None
course_index = None

def getcosinemat(df):
    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    return cvmat

def getcleantitle(df):
    df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)
    return df

def cosinesimmat(cv_mat):
    return cosine_similarity(cv_mat)

def readdata():
    try:
        return pd.read_csv('UdemyCleanedTitle.csv')
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

def searchterm(term, df):
    result_df = df[df['course_title'].str.contains(term, case=False, na=False)]
    top6 = result_df.sort_values(by='num_subscribers', ascending=False).head(6)
    return top6

def extractfeatures(recdf):
    course_url = list(recdf['url'])
    course_title = list(recdf['course_title'])
    course_price = list(recdf['price'])
    return course_url, course_title, course_price

def recommend_course(title, numrec=6):
    global df, cosine_simi, course_index
    matches = df[df['course_title'].str.lower().str.contains(title.lower(), regex=False, na=False)]
    
    if matches.empty:
        return "No courses found with that title. Try a different keyword."
    
    idx = course_index[matches['course_title'].iloc[0]]
    scores = list(enumerate(cosine_simi[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:]
    selected_indices = [i[0] for i in sorted_scores]
    selected_scores = [i[1] for i in sorted_scores]
    rec_df = df.iloc[selected_indices][['course_title', 'url', 'price', 'num_subscribers']].copy()
    rec_df['Similarity_Score'] = selected_scores
    return rec_df.head(numrec)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    global df, cosine_simi, course_index
    df = readdata()
    if df.empty:
        logging.error("Empty DataFrame loaded")
        return render_template('index.html', showerror=True, coursename="Data Loading Error")
    df = getcleantitle(df)
    cvmat = getcosinemat(df)
    cosine_simi = cosinesimmat(cvmat)
    course_index = pd.Series(df.index, index=df['course_title']).drop_duplicates()

    if request.method == 'POST':
        my_dict = request.form
        titlename = my_dict['course']
        try:
            recdf = recommend_course(titlename, numrec=6)
            
            if isinstance(recdf, str):
                resultdf = searchterm(titlename, df)
                course_url, course_title, course_price = extractfeatures(resultdf)
                coursemap = dict(zip(course_title, course_url))
                if len(coursemap) != 0:
                    return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)
                else:
                    return render_template('index.html', showerror=True, coursename=titlename)
            
            course_url, course_title, course_price = extractfeatures(recdf)
            dictmap = dict(zip(course_title, course_url))
            if len(dictmap) != 0:
                return render_template('index.html', coursemap=dictmap, coursename=titlename, showtitle=True)
            else:
                return render_template('index.html', showerror=True, coursename=titlename)

        except Exception as e:
            logging.error(f"Error in recommend_course: {e}")
            resultdf = searchterm(titlename, df)
            course_url, course_title, course_price = extractfeatures(resultdf)
            coursemap = dict(zip(course_title, course_url))
            if len(coursemap) != 0:
                return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)
            else:
                return render_template('index.html', showerror=True, coursename=titlename)

    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    df = readdata()
    if df.empty:
        logging.error("Empty DataFrame loaded in dashboard")
        return render_template('dashboard.html', error="Failed to load dataset. Please check the CSV file.")
    
    try:
        valuecounts = getvaluecounts(df)
        levelcounts = getlevelcount(df)
        subjectsperlevel = getsubjectsperlevel(df)
        yearwiseprofitmap, subscriberscountmap, profitmonthwise, monthwisesub = yearwiseprofit(df)
        
        if not all([valuecounts, levelcounts, subjectsperlevel, yearwiseprofitmap]):
            logging.warning("Some dashboard data is empty")
            return render_template('dashboard.html', error="Some data could not be processed. Check logs for details.")
        
        return render_template('dashboard.html', 
                              valuecounts=valuecounts, 
                              levelcounts=levelcounts,
                              subjectsperlevel=subjectsperlevel, 
                              yearwiseprofitmap=yearwiseprofitmap,
                              subscriberscountmap=subscriberscountmap, 
                              profitmonthwise=profitmonthwise,
                              monthwisesub=monthwisesub)
    except Exception as e:
        logging.error(f"Error in dashboard route: {e}")
        return render_template('dashboard.html', error="An error occurred while loading the dashboard. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)