import numpy as np
import matplotlib.pyplot as plt
import scipy.io

mat = scipy.io.loadmat('amp_data.mat')
actual_data = np.asmatrix(mat['amp_data'])

'''
PLOTTING
'''

flattened_data = actual_data.flatten().tolist()[0]
print("Flattened the list")

# We need to make the list sparser so that the line thing can handle it
def reduce(f, lst):
    reduced_list = []
    for n in range(0, len(lst) - 2, 2):
        reduced_list.append(f(lst[n], lst[n+1]))
    return reduced_list

reduced_list = reduce(lambda x, y: (x + y)/2, flattened_data)
print("Reduced the list")

plt.subplot(2, 1, 1)
plt.plot(range(len(reduced_list)), reduced_list, '-')
plt.title('A tale of 2 subplots')
print("Finished the first plot")

plt.subplot(2, 1, 2)
plt.hist(flattened_data, 500)
print("Finished the second plot")

plt.show()


'''
SHUFFLING
'''
def parse_data(lst):
    parsed = []
    for index in range(0, len(lst)-21, 21):
        parsed.append(lst[index:index+21].flatten().tolist())
    return np.array(parsed)

def split(lst, training=0.7, testing=0.15, validation=0.15):

    shuffled_data = np.random.permutation(lst)
    #print('shuffled')
    parsed_data = parse_data(shuffled_data)
    #print(parsed_data.shape)
    #print('parsed')

    lst_length = len(parsed_data)

    train_index = int(lst_length*training)
    test_index = train_index + int(lst_length*testing)
    validation_index = test_index + int(lst_length*validation)
    return {"train": {"x": parsed_data[0:train_index][:, 0:20], "y": parsed_data[0:train_index][:, 20]},
            "test": {"x": parsed_data[train_index:test_index][:, 0:20], "y": parsed_data[train_index:test_index][:, 20]},
            "val": {"x": parsed_data[test_index:validation_index][:, 0:20], "y": parsed_data[test_index:validation_index][:, 20]}
            }

data = split(actual_data)

x = np.array([x/20 for x in range(20)])
y = data['train']['x'][0].tolist()

A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]

print(m, c)

x_test = np.array([x/20 for x in range(21)])
plt.plot([x/20 for x in range(21)], y + [data['train']['y'][0]], 'o', label='Original data')
plt.plot([x/20 for x in range(21)], m*x_test + c, 'r', label='Fitted line')
plt.legend()

plt.show()
