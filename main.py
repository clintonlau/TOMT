from flask import Flask, request, render_template, abort
import joblib 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

MODEL_FILE_NAME = "./model_checkpoints/tfidf_ingredients_model.pkl"
ENCODING_FILE_NAME = "./encodings/tfidf_ingredients_encodings.pkl"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    # TODO: render a new template/web page to display information of the 5 predictions

    # get user query as a string, format of query should be comma separated ingredient list
    query = request.form.get('ingredients')
    query_encodings = model.transform([query])
    cos_sim_scores = list(map(lambda x: cosine_similarity(query_encodings, x), train_encodings))
    prediction_df = get_recommendations(5, cos_sim_scores)

    predictions = zip(list(prediction_df['recipe_name']), list(prediction_df['url']))
    # predictions = zip(['recipe-1'], ['https://cooking.nytimes.com/recipes/1016122-almost-from-scratch-corn-tortillas'])

    return render_template(
        'result.html', 
        predictions=predictions
    )


def get_recommendations(N, scores):
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    return train_recipes.iloc[top].reset_index(drop=True).copy()


if __name__ == '__main__':

    model = joblib.load(MODEL_FILE_NAME)
    print('Model loaded...')
    train_encodings = joblib.load(ENCODING_FILE_NAME)
    print('Training data loaded...')
    train_recipes = pd.read_pickle('./data/nytc_training.pkl')

    app.run(debug=True)