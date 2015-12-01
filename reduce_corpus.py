reduction_factor = 0.1

if __name__ == "__main__":

    handles = []
    
    for i in range(1, int(1/reduction_factor)):
        handles.append(open("reduced_{}.txt".format(int(i*reduction_factor*100)), "w"))

        
