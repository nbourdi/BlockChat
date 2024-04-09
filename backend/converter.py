# Open the text file
with open('trans4.txt', 'r') as file:
    lines = file.readlines()

# Initialize an empty list to store the converted lines
converted_lines = []

# Loop through each line in the file
for line in lines:
    # Check if the line starts with "id4"
    if line.startswith("id3"):
        # Extract the message part and remove any leading/trailing whitespace
        message = line.split(" ", 1)[1].strip()
        # Create the formatted line and append it to the converted_lines list
        formatted_line = f'node.create_transaction(receiver_address=sorted_peers[3].public_key, type_of_transaction="message", amount=None, message="{message}")'
        converted_lines.append(formatted_line)
    elif line.startswith("id2"):
        # Extract the message part and remove any leading/trailing whitespace
        message = line.split(" ", 1)[1].strip()
        # Create the formatted line and append it to the converted_lines list
        formatted_line = f'node.create_transaction(receiver_address=sorted_peers[2].public_key, type_of_transaction="message", amount=None, message="{message}")'
        converted_lines.append(formatted_line)
    elif line.startswith("id1"):
        # Extract the message part and remove any leading/trailing whitespace
        message = line.split(" ", 1)[1].strip()
        # Create the formatted line and append it to the converted_lines list
        formatted_line = f'node.create_transaction(receiver_address=sorted_peers[1].public_key, type_of_transaction="message", amount=None, message="{message}")'
        converted_lines.append(formatted_line)
    elif line.startswith("id0"):
        # Extract the message part and remove any leading/trailing whitespace
        message = line.split(" ", 1)[1].strip()
        # Create the formatted line and append it to the converted_lines list
        formatted_line = f'node.create_transaction(receiver_address=sorted_peers[0].public_key, type_of_transaction="message", amount=None, message="{message}")'
        converted_lines.append(formatted_line)


# Write the converted lines to a new file
with open('converted_output4.py', 'w') as output_file:
    output_file.write('\n'.join(converted_lines))
