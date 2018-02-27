# HackerCamp-Summer-2018-Submission---Analytics-

The problem was deduplication of the data .The approached used to solve is Unsupervised Learning .
Using a Kmeans clustering algorithm on the data , so as to compare the records within each cluster rather than comparing it to every other record in the data .
the score function used is as follows :

Score = (2*distance b/w person’s names + distance b/w DOB + distance b/w gender + 2*distance b/w father’s name) /6 .
The distance used to calculated was Levenshtein distance .

This approach was able to identify almost 98% of the duplicates in the data .




