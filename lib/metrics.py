from munkres import Munkres

# The Jaccard distance between two sets. Taken as the size of the
# intersection of two sets divided by the size of their union
def jaccard(s1, s2):
    # Get intersection of sets
    intersect = [i for i in s1 if i in s2]
    # Divide size of intersection by size of union
    return float(len(intersect))/(len(s1) + len(s2) - len(intersect))

# Get the Jaccard distance for gradually increasing subsets of the
# topics we are comparing. Accounts for elements further down the list
# being less important to the definition of a topic
def average_jaccard(s1, s2):
    jd = []

    # Iterate over subsets
    for i in range(1, len(s1)+1):
        # Get jaccard distance of this subset and store
        jd.append(jaccard(s1[:i], s2[:i]))

    # Get the average Jaccard distance
    return sum(jd)/len(s1)

# Build a matrix of the similarity between model topics using the
# Average Jaccard distance as a measure of relatedness
def build_similarity_matrix(m1, m2, depth):

    # Create empty matrix
    similarity_matrix = []

    # Iterate over each topic
    for i in range(0, m1.num_topics):
        similarity_matrix.append([])
        for j in range(0, m2.num_topics):
            # Get topic pair
            t1 = [w[1] for w in m1.show_topic(i, topn=depth)]
            t2 = [w[1] for w in m2.show_topic(j, topn=depth)]
         
            # Compute Average Jaccard distance and store in similarity matrix cell
            similarity_matrix[i].append(average_jaccard(t1, t2))

    # Return final matrix
    return similarity_matrix

# Used to invert the Average Jaccard matrix so that Munkres will find
# the maximum rather than the minimum agreement
def invert_probabilities(matrix):
    # Don't want to destroy the original matrix
    new_matrix = [] 

    for i in range(0, len(matrix)):
        new_matrix.append([])
        for j in range(0, len(matrix[i])):
            new_matrix[i].append(1-matrix[i][j])

    return new_matrix

# Compute the agreement of two models. Matrix is Average Jaccard
# distance between each topic. Assignments are topic pairings computed
# with Munkres
def compute_agreement(matrix, assignments):

    total = 0

    # Compute sum of Average Jaccard distances
    for pairing in assignments:
        total += matrix[pairing[0]][pairing[1]]

    # Return the average as the agreement between models
    return total/len(matrix)

# Print a matrix. Really just for testing purposes
def print_matrix(matrix):
    for i in matrix:
        for j in i:
            # Some pretty formatting for simple floating poing
            # matrices
            print "{:8.3}".format(j),
        print

# Establish which topics should be considered equivalent between two
# models by examining similarity matrix
def join_similar_topics(matrix, depth):
    # Compute topic similarity by finding lowest cost Average Jaccard distance
    m = Munkres()
    return m.compute(matrix)

def get_similar_topics(m1, m2, depth):
    # Build matrix of Average Jaccard distances between topics
    sim_matrix = build_similarity_matrix(m1, m2, depth)

    # Invert Jaccard indices for Munkres
    cost_matrix = invert_probabilities(sim_matrix)

    return join_similar_topics(cost_matrix, depth)

# Compute the similarity between two models as a single floating point
# value. Values closer to 1.0 indicate strong levels of similarity
def get_model_agreement(m1, m2, depth):

    # Build matrix of Average Jaccard distances between topics
    sim_matrix = build_similarity_matrix(m1, m2, depth)

    # Invert Jaccard indices for Munkres
    cost_matrix = invert_probabilities(sim_matrix)

    assignments = join_similar_topics(cost_matrix, depth)

    # Compute model agreement based on topic pairings and return
    return compute_agreement(sim_matrix, assignments)
