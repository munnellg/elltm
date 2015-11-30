def jaccard(s1, s2):
    intersect = [i for i in s1 if i in s2]
    return float(len(intersect))/(len(s1) + len(s2) - len(intersect))

def average_jaccard(s1, s2):
    jd = []
    for i in range(1, len(s1)+1):
        jd.append(jaccard(s1[:i], s2[:i]))

    return sum(jd)/len(s1)

def build_similarity_matrix(m1, m2, depth):
    similarity_matrix = []

    for i in range(0, m1.num_topics):
        similarity_matrix.append([])
        for j in range(0, m2.num_topics):
            t1 = [w[1] for w in m1.show_topic(i, topn=depth)]
            t2 = [w[1] for w in m2.show_topic(j, topn=depth)]
         
            similarity_matrix[i].append(average_jaccard(t1, t2))

    return similarity_matrix
