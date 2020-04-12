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


    relevant_objects = [obj for i, obj in enumerate(objects)
                        for j, objects in enumerate(retrieved_objects_by_voter)
                        if objects_ratings_by_voter[j][i] >= 1]
        
    relevant_objects = set(relevant_objects)
    all_objects = set([obj for obj in objects for objects in retrieved_objects_by_voter])

    precision = [0 for _ in range(n_voter)]
    recall    = [0 for _ in range(n_voter)]



    for i in range(n_voter):
        precision[i] =    #Relevant U retrieved  / retrieved
        recall[i]    =    #relevant U retrieved  / relevant

    #AP: compute at every position

    pass

def NDCG():
    """Rm average of relevance annotation
       Rm >= 2 -> 3
       0.5 < RM < 2 -> 2
       0 < Rm <= 0.5 -> 1
       else -> 0
       compute NDCG@5, NDCG@10
    """
    pass


