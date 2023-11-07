from flask import Flask, request, jsonify, render_template
import joblib 
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

MODEL_FILE_NAME = "./model_checkpoints/tfidf_ingredients_model.pkl"
ENCODING_FILE_NAME = "./encodings/tfidf_ingredients_encodings.pkl"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    # get user query as a string
    json_ = request.json
    print(json_)
    query = ...
    query_encodings = model.transform([query])
    cos_sim_scores = list(map(lambda x: cosine_similarity(query_encodings, x), train_encodings))
    pred_df = get_recommendations(5, cos_sim_scores)
    return render_template()


def get_recommendations(N, scores):
    test_ingredients = 'masa harina'

    # use our pretrained tfidf model to encode our input ingredients
    ingredients_tfidf = model.transform([test_ingredients])

    # calculate cosine similarity between actual recipe ingreds and test ingreds
    cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), train_df)
    scores = list(cos_sim)

    # load in recipe dataset
    df_recipes = nytc_features # pd.read_csv(config.PARSED_PATH)
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(columns = ['recipe', 'ingredients', 'score', 'cuisine'])
    count = 0
    for i in top:
        recommendation.at[count, 'recipe'] = (df_recipes['recipe_name'][i])
        
        recommendation.at[count, 'ingredients'] = (df_recipes['ingredient_parsed'][i])
        
        recommendation.at[count, 'cuisine'] = df_recipes['cuisine'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        
        count += 1
    return recommendation



if __name__ == '__main__':

    model = joblib.load(MODEL_FILE_NAME)
    print('Model loaded...')
    train_encodings = joblib.load(ENCODING_FILE_NAME)
    print('Training data loaded...')
    train_df = pd.read_pickle('./data/nytc_training.pkl')

    app.run(debug=True)