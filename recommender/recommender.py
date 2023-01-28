import numpy as np
import pandas as pd


class Recommender:

    def __init__(self):
        plants_df = pd.read_csv('./data/plants_normalized.csv', sep=',', encoding='UTF-8',)
        self.ATTRIBUTES = ['height', 'width', 'water', 'light', 'humidity', 'temperature', 'toxicity', 'difficulty']
        self.PLANTS = plants_df[['id', 'name'] + self.ATTRIBUTES]

        self.NAMES = self.PLANTS['name']
        self.INDICES = pd.Series(self.PLANTS.index, index=self.PLANTS['name'])

    def get_cosine_similarity(self, x, y):

        numerator = np.dot(x, y)
        denominator = np.linalg.norm(x) * np.linalg.norm(y)

        # sanity check: x and y must be non-zero vectors
        if denominator > 0:
            sim = numerator / denominator
        else:
            raise AttributeError(
                "Not defined for vectors containing only zeros!")

        return sim

    def get_recommendations(self, plant_id, n=10):

        # query item from id
        query_item = self.PLANTS.loc[self.PLANTS.id == plant_id][self.ATTRIBUTES]
        query_item = query_item.to_numpy()

        # compute cosine similarities between queryitem and all
        # other plants
        similarities = []
        for i in range(len(self.PLANTS)):

            # skip the query item
            if i != plant_id - 1:

                # get the i-th item
                other_item = self.PLANTS.iloc[i][self.ATTRIBUTES]
                other_item = other_item.to_numpy()

                # compute cosine similarity between both items
                sim = self.get_cosine_similarity(query_item, other_item)

                # store result in list
                similarities.append((i, sim))

        # sort pairs w.r.t. second entry (cosine similarities) in
        # descending order (reverse=True)
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # take the top n elements
        sorted_similarities = sorted_similarities[:n]

        # get the corresponding plant indices
        plant_indices = [pair[0] for pair in sorted_similarities]

        # return the list of names
        return self.NAMES.iloc[plant_indices]
