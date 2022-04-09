import matplotlib.pyplot as plt

x = [1.66, 3.49, 3.49, 1.66, 3.68, 3.68, 3.74, 3.74, 3.49, 3.49, 3.49, 1.66, 3.49]
y = [0.69, 1.0, 1.0, 0.69, 0.954, 0.954, 1.0, 1.0, 1.0, 1.0, 1.0, 0.69, 1.0]

plt.xlabel('lift')
plt.ylabel('cosine')
plt.legend()
plt.scatter(x, y)
plt.show()

