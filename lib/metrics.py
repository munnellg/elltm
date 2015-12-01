from munkres import Munkres

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

def invert_probabilities(matrix):
    # Don't want to destroy the original matrix
    new_matrix = [] 

    for i in range(0, len(matrix)):
        new_matrix.append([])
        for j in range(0, len(matrix[i])):
            new_matrix[i].append(1-matrix[i][j])

    return new_matrix

def get_column_minimum(matrix, index):
    col = [row[index] for row in matrix]
    return min(col)

def subtract_from_column(matrix, index, value):
    for row in matrix:
        row[index] = row[index] - value

def duplicate_matrix(matrix):
    new_matrix = []

    # Subtract minimum from rows
    for row in range(0, len(matrix)):
        new_matrix.append([])
        for col in range(0, len(matrix[row])):
            new_matrix[row].append(matrix[row][col])

    return new_matrix

def reduce_rows(matrix):
    for row in matrix:
        minimum = min(row)
        for i in range(0, len(row)):
            row[i] = row[i]-minimum

def reduce_cols(matrix):
    for col in range(0, len(matrix[0])):
        minimum = get_column_minimum(matrix, col)
        subtract_from_column(matrix, col, minimum)

def assign_topics(matrix):
    # Initialize with no assignments
    assignments = [None] * len(matrix)

    # Attempt to assign all topics
    for row in range(0, len(matrix)):
        idx = -1
        while 0 in matrix[row][idx+1:]:
            idx = idx + matrix[row][idx+1:].index(0) + 1
            if idx not in assignments:
                assignments[row] = idx
                break

    return assignments

def draw_lines(matrix, assignments):
    marked_cols = []
    marked_rows = []

    # Mark all unassigned rows
    for i in range(0, len(assignments)):
        if assignments[i] == None:
            marked_rows.append(i)

            # Mark all cols having zeros in newly marked row
            for j in range(0, len(matrix[i])):
                if matrix[i][j] == 0 and j not in marked_cols:
                    marked_cols.append(j)
                    # Mark all rows having assignments in newly marked cols
                    if j in assignments:
                        marked_rows.append(assignments.index(j))
    vlines = marked_cols
    hlines = [i for i in range(0, len(matrix)) if i not in marked_rows]

    print "Horizontal Lines: {}".format(hlines)
    print "Vertical Lines: {}".format(vlines)

    return hlines, vlines

def find_unmarked_minimum(matrix, hlines, vlines):
    
    minimum = 10000

    for i in range(0, len(matrix)):
        if i in hlines:
            continue
        for j in range(0, len(matrix[i])):
            if matrix[i][j] < minimum and j not in vlines:
                minimum = matrix[i][j]

    return minimum

def reduce_marked_matrix(matrix, hlines, vlines, reduction):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if i not in hlines and j not in vlines:
                matrix[i][j] = matrix[i][j] - reduction
            if i in hlines and j in vlines:
                matrix[i][j] = matrix[i][j] + reduction
    return

def hungarian_method(matrix):
    # So we don't destroy the original matrix
    matrix = duplicate_matrix(matrix)

    # Reduce rows and columns
    reduce_rows(matrix)
    reduce_cols(matrix)

    print "Hungarian Matrix"
    print_matrix(matrix)
    print

    assignments = assign_topics(matrix)

    while None in assignments:
        hlines, vlines = draw_lines(matrix, assignments)
        
        minimum = find_unmarked_minimum(matrix, hlines, vlines)
        print minimum

        reduce_marked_matrix(matrix, hlines, vlines, minimum)
        print "Hungarian Matrix"
        print_matrix(matrix)
        print

        assignments = assign_topics(matrix)
        break

    return assignments

def compute_agreement(matrix, assignments):
    return matrix


def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print "{:8.3}".format(j),
        print

def test_hungarian():
    matrices = [
        [[0.0, 1.0, 1.0, 1.0],
          [1.0, 1.0, 1.0, 0.0],
          [0.0, 1.0, 1.0, 1.0],
          [1.0, 0.0, 0.0, 1.0]],
    
         [[0.0, 1.0, 1.0, 1.0],
          [1.0, 1.0, 1.0, 0.0],
          [0.0, 1.0, 0.0, 0.0],
          [1.0, 0.0, 0.0, 1.0]],

         [[80.0, 40.0, 50.0, 46.0],
          [40.0, 70.0, 20.0, 25.0],
          [30.0, 10.0, 20.0, 30.0],
          [35.0, 20.0, 25.0, 30.0]]
    ]
    munk = Munkres()

    for m in matrices:
        print "Test Matrix"
        print_matrix(m)
        print
        print munk.compute(m)
        print
        

def get_model_agreement(m1, m2, depth):
    sim_matrix = build_similarity_matrix(m1, m2, depth)

    print "Similarity Matrix"
    print_matrix(sim_matrix)
    print
    cost_matrix = invert_probabilities(sim_matrix)

    print "Inverse Similarity Matrix"
    print_matrix(cost_matrix)
    print

    m = Munkres()
    assignments = m.compute(cost_matrix)

    #assignments = hungarian_method(cost_matrix)

    print assignments

    agreement = compute_agreement(sim_matrix, assignments)

    return agreement
