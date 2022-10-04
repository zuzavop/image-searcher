import matplotlib.pyplot as plt
import csv 

ranks1 = []
ranks2 = []
diff = []


with open('sea_dataset_combine_scores.csv') as csv_file:
#with open('sea_dataset_normal.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line = 0

    previous_row = {}
    
    for row in csv_reader:
        if line > 1 and row[1] == previous_row[1]:
            ranks1.append(int(previous_row[3]))
            ranks2.append(int(row[3]))
            diff.append(int(previous_row[3]) - int(row[3]))

        previous_row = row
        line += 1

       

plt.rcParams["figure.figsize"] = (3,8)

data = [ranks1, ranks2, diff]

fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(data)

plt.show()
