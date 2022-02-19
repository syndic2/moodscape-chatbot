class CopingCategoryTechnique:

    def __init__(self, category):
        self.category= category
        self.questions= []
        self.average_score= 0

class CopingStyle:
    
    def __init__(self, style):
        self.style= style
        self.category_techniques= []

    def add_category(self, category_technique):
        self.category_techniques.append(category_technique)