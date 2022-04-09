import numpy
import pandas

from rule import associationRules, printRules
from apriori import apriori, findFrequentOneItemsets


if __name__ == "__main__":
    min_sup = 5000
    min_conf = 0.9

    data = pandas.read_csv("./Wine Reviews csv Files/winemag-data-130k-v2.csv", encoding='UTF-8',
                           usecols=['province', 'region_1', 'region_2',
                                    'taster_name', 'taster_twitter_handle',
                                    'title', 'variety', 'winery'])
    dataset = numpy.array(data)

    frequent_one_itemsets = findFrequentOneItemsets(dataset, min_sup)

    frequent_itemsets = apriori(dataset, frequent_one_itemsets, min_sup)

    for item in frequent_itemsets.keys():
        print(item)

    rules_list = associationRules(frequent_itemsets, min_conf)

    printRules(frequent_itemsets, rules_list, len(dataset))
