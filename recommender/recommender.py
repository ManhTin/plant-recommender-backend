import numpy as np
import pandas as pd


class Recommender:

    def __init__(self, data_path):
        plants_df = pd.read_csv(data_path, sep=',', encoding='UTF-8',)
        self.ATTRIBUTES = [
            'height', 'width', 'water', 'light', 'humidity',
            'temperature', 'toxicity', 'difficulty', 'leaf_green',
            'leaf_multicolored', 'leaf_oblong', 'leaf_oval', 'leaf_teardrop',
            'leaf_triangular', 'leaf_spear', 'leaf_heart', 'leaf_wavy',
            'leaf_palmate', 'leaf_split', 'leaf_round', 'leaf_ribbon',
            'leaf_pattern', 'growth_cluster', 'growth_dense', 'growth_upright',
            'growth_shrubby', 'growth_cascading', 'growth_tree']
        self.PLANTS = plants_df[['id', 'name'] + self.ATTRIBUTES]

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

        # convert global plant_id to dataframe index for querying
        query_id = plant_id - 1
        # query item from id
        query_item = self.PLANTS.iloc[query_id][self.ATTRIBUTES]
        query_item = query_item.to_numpy()

        # compute cosine similarities between queryitem and all
        # other plants
        similarities = []
        for i in range(len(self.PLANTS)):

            # skip the query item
            if i != query_id:

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

        # return list of global ids of the top n elements
        return [pair[0] + 1 for pair in sorted_similarities]

    #  TODO generate recommendations based on user input and list of plants
