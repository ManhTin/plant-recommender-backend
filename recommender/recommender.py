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
        """Compute cosine similarity between two numpy vectors."""
        numerator = np.dot(x, y)
        denominator = np.linalg.norm(x) * np.linalg.norm(y)

        # sanity check: x and y must be non-zero vectors
        if denominator > 0:
            sim = numerator / denominator
        else:
            raise AttributeError(
                "Not defined for vectors containing only zeros!")

        return sim

    def get_recommendations_by_id(self, plant_id, n=10, similar_first=True):
        """
        Get list of ids of similar plants for a plant with a given plant_id.
        n = number of recommendations
        similar_first = sort recommendations by best recommendations first
        excluded_ids = list of plant ids to exclude from recommendations
        """
        # convert global plant_id to dataframe index for querying
        query_id = plant_id - 1
        # query item from id
        query_item = self.PLANTS.iloc[query_id][self.ATTRIBUTES]
        query_item = query_item.to_numpy()

        return self.__get_recommendations(query_item, query_id, n=n, similar_first=similar_first)

    def get_recommendations_by_profile(self, user_profile, n=10, similar_first=True):
        """
        Get list of ids of similar plants for a user_profile.
        n = number of recommendations
        similar_first = sort recommendations by best recommendations first
        excluded_ids = list of plant ids to exclude from recommendations
        """
        user_profile_df = self.__parse_user_profile_to_df(user_profile)
        # convert profile to numpy array
        query_item = user_profile_df.to_numpy()

        return self.__get_recommendations(
            query_item, n=n, similar_first=similar_first, excluded_ids=user_profile['owned_plants'])

    def __get_recommendations(self, query_item, item_id=None, n=10, similar_first=True, excluded_ids=None):
        """
        Build list of recommendations for a given query item using cosine similarity.
        n = number of recommendations
        similar_first = sort recommendations by best recommendations first
        excluded_ids = list of plant ids to exclude from recommendations
        """
        if excluded_ids is None:
            excluded_ids = []
        # compute cosine similarities between queryitem and all
        # other plants
        similarities = []
        for i in range(len(self.PLANTS)):

            # skip the query item
            if i != item_id and i+1 not in excluded_ids:

                # get the i-th item
                other_item = self.PLANTS.iloc[i][self.ATTRIBUTES]
                other_item = other_item.to_numpy()

                # compute cosine similarity between both items
                sim = self.get_cosine_similarity(query_item, other_item)

                # store result in list
                similarities.append((i, sim))

        # sort pairs w.r.t. second entry (cosine similarities) in descending order by default
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=similar_first)

        # take the top n elements
        sorted_similarities = sorted_similarities[:n]

        # return list of global ids of the top n elements
        return [pair[0] + 1 for pair in sorted_similarities]

    def __parse_user_profile_to_df(self, user_profile=None):
        """
        Parse user_profile into dataframe. Keep profile attributes from user_profile and
        replace the rest of the attributes which are optical attributes with the average
        of the liked plants attributes too build the profile.
        """
        # attributes we got from the user survey
        profile_attributes = user_profile['profile']
        liked_plants = self.PLANTS[self.PLANTS['id'].isin(user_profile['liked_plants'])]
        # build profile df from average of liked plants attributes
        profile = liked_plants[self.ATTRIBUTES].mean()
        # replace attributes in profile w/ attributes from profile_attributes and keep the rest
        profile.update(profile_attributes)

        return profile[self.ATTRIBUTES]
