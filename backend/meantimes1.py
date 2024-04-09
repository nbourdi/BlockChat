# Read the execution times from the file
with open('execution_times.txt', 'r') as file:
    lines = file.readlines()

# Extract execution times and convert them to floats
execution_times = [float(line.split(":")[1].strip().split()[0]) for line in lines if line.startswith("Execution time")]

# Calculate the mean execution time
mean_execution_time = sum(execution_times) / len(execution_times)

print(f"Mean Execution Time for transaction : {mean_execution_time} seconds")

# Read the execution times from the file
with open('execution_times2.txt', 'r') as file:
    lines = file.readlines()

# Extract execution times and convert them to floats
execution_times = [float(line.split(":")[1].strip().split()[0]) for line in lines if line.startswith("Execution time")]

# Calculate the mean execution time
mean_execution_time = sum(execution_times) / len(execution_times)

print(f"Mean Execution Time for BLOCKS : {mean_execution_time} seconds")
