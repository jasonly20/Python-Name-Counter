# Python-Name-Counter
Steps:
1) First run the file with "python3 -preprocess [NAME OF .TXT FILE TO CHECK NAME COUNTS]
this command must be ran first or the program will throw an exception. This will also create a .csv file with all the names listed and their occurences from highest counts to lower.
2) -top N command argument takes in a positive number N and will return the top N names in the text file.
3) -grap10 [NAME OF .TXT FILE TO CHECK NAME COUNTS] command will output a graph created with the number of occurences between each pair of the top 10 results of names, and show how many times each pair occurred on the same text line.

The file "stopwords.txt" contains commonly used words that are not names in order to filter out unrelated text.
