import csv
from math import log2

def kappa(ratings, num_cat=2):
    """ mean of annotations
        pairwise cohen's kappa
        ex
        [1, 2, 3, 4], n list of num-cat numbers, 3"""
    
    def score(two_scores, num_cat):
        p_e = 1/num_cat
        p_0 = len([1 for i in range(len(two_scores)) if two_scores[1] == two_scores[2])
        ḱ = (p_0 - p_e) / (1 - p_e)
        return k

    pairwise_k = [score([ratings[i], ratings[j]]) for i in range(len(two_scores))
                                            for j in range(i + 1, len(two_scores))]

    return sum(pairwise_k)/len(pairwise_k)

def MAP(retrieved_objects_by_voter, object_ratings_by_voter):
    """ relevance. average of annotation score >= 1
        irrelevance. average < 1"""

    assert(2 <= len(retrieved_objects_by_voter) == 
                len(objects_ratings_by_voter) <= 3))

    #assert all rated same number

    n_voter = len(retrieved_objects_by_voter)

    def AP(retrieved_objects_by_voter, object_ratings_by_voter)
        relevant_objects = [obj for i, obj in enumerate(objects)
                            for j, objects in enumerate(retrieved_objects_by_voter)
                            if objects_ratings_by_voter[j][i] >= 1]
            
        relevant_objects = set(relevant_objects)
        all_objects = set([obj for obj in objects for objects in retrieved_objects_by_voter])

        numer = len(all_objects.intersection(relevant_objects))
        denom = len(all_objects)

        return numer/denom

    APs = []
    for i in range(1, 12):
        res = AP(retrieved_objects_by_voter[:i], object_ratings_by_voter[:i])
        APs.append(res)

    MAP = sum(APs)/len(APs)

    return MAP


def NDCG():
    """Rm average of relevance annotation
       Rm >= 2 -> 3
       0.5 < RM < 2 -> 2
       0 < Rm <= 0.5 -> 1
       else -> 0
       compute NDCG@5, NDCG@10
    """
    #DCG = sum 1 -> p of rel_i / log_2 (i + 1), p position
    pass


def main():
    #IO
    #input. csv.
    #relevance annotation.tsv: query, url, docID, SE, annotations [1;2;]..
    #SE_ranking.csv:  rank, SE1_docID, SE2_docID
    #RM_ranking.csv : docID, VSM_rank, BM25_rank
    

    #output: EVA_query_n_ID.csv
    #measure, score
    #kappa[2,5], MAP-ba,bi,VSM,BM25, NDCG@[5,10]-SE1,SE2,VSM,BM25
    pass

if __name__ == "__main__":
    main()