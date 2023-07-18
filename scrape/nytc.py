import requests
from bs4 import BeautifulSoup
import numpy as np
import extruct

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
}

class NYTC():
    def __init__(self, url) -> None:
        self.url = url
        self.page = requests.get(url, headers=headers)
        self.recipe_soup = BeautifulSoup(self.page.text, 'html.parser')
        self.data = extruct.extract(
            self.page.text,
            syntaxes=['json-ld'],
            uniform=True,
        )['json-ld'][0]
        self.type = self.data['@type'][0]

    def recipe_name(self):
        try:
            return self.data['name']
        except:
            return np.nan
    
    def nutrition(self):
        try:
            
            return self.data['nutrition']
        except:
            return np.nan
        
    def category(self):
        try:
            return self.data['recipeCategory']
        except:
            return np.nan
        
    def cuisine(self):
        try:
            return self.data['recipeCuisine']
        except:
            return np.nan
    
    def ingredient(self):
        try:
            return self.data['recipeIngredient']
        except:
            return np.nan
    
    def instruction(self):
        try:
            instructions = self.data['recipeInstructions']
            if instructions and isinstance(instructions[0], dict):
                instructions = [instruction['text'] for instruction in instructions]
            return instructions
        except:
            return np.nan
