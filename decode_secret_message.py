def merge_files(file1, file2, merged_file):
    """
    Merges two text files by alternating lines. If one file has more lines, append the rest.
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    merged_lines = []
    len1, len2 = len(lines1), len(lines2)
    min_len = min(len1, len2)

    # Alternate lines
    for i in range(min_len):
        merged_lines.append(lines1[i].rstrip('\n'))
        merged_lines.append(lines2[i].rstrip('\n'))

    # Append remaining lines from either file
    if len1 > min_len:
        merged_lines.extend(line.rstrip('\n') for line in lines1[min_len:])
    if len2 > min_len:
        merged_lines.extend(line.rstrip('\n') for line in lines2[min_len:])

    with open(merged_file, 'w', encoding='utf-8') as mf:
        mf.write('\n'.join(merged_lines) + '\n')
def decode_secret_message(input_file, output_file):
    """
    Reads a file with space-separated Unicode code points per line,
    decodes all lines into a complete message, writes to output,
    and prints the full decoded message.
    """
    decoded_lines = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            # Convert each number to a character
            chars = [chr(int(num)) for num in line.strip().split()]
            decoded_line = ''.join(chars)
            decoded_lines.append(decoded_line)

    # Join all decoded lines with newlines
    decoded_message = '\n'.join(decoded_lines)

    # Write the complete message to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(decoded_message + "\n")

    # Print the complete decoded message to the screen
    print(decoded_message)

if __name__ == "__main__":
    decode_secret_message("secret_message.txt", "decoded_message.txt")
    print("Decoding complete: decoded_message.txt created.")
