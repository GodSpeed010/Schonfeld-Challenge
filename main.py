import heapq
import csv

'''Assumption made: When comparing query results for 2 different securities,
if both securities have a street ID which has a full match with the query,
then the order in the output for the full-match queries does not matter.
'''

QUERY = "abc"


class Node(object):
    def __init__(self, security_id, char_matches, priority_weight):
        self.security = security_id
        self.char_matches = char_matches
        self.priority_weight = priority_weight

    def __repr__(self):
        return f'security-id: {self.security}'

    # Return True if self should be placed 'higher' than other
    def __lt__(self, other):
        if self.char_matches > other.char_matches:
            return True
        elif self.char_matches < other.char_matches:
            return False
        else:  # matches lengths equal
            if self.char_matches == len(QUERY):
                return True  # both were full matches
            else:  # partial matches of equal match_length
                return True if (self.priority_weight < other.priority_weight) else False


# Credit to https://www.interviewbit.com/blog/longest-common-substring/ for this algorithm
# Returns length of longest common substring
def longest_common_substr(str1, str2, N, M):
    LCSuff = [[0 for k in range(M + 1)] for l in range(N + 1)]
    mx = 0
    for i in range(N + 1):
        for j in range(M + 1):
            if (i == 0 or j == 0):
                LCSuff[i][j] = 0
            elif (str1[i - 1] == str2[j - 1]):
                LCSuff[i][j] = LCSuff[i - 1][j - 1] + 1
                mx = max(mx, LCSuff[i][j])
            else:
                LCSuff[i][j] = 0
    return mx


def main():
    # row_index to priority
    priorities = {
        'root_symbol': 1,
        'bbg': 2,
        'symbol': 3,
        'ric': 4,
        'cusip': 5,
        'isin': 6,
        'bb_yellow': 7,
        'bloomberg': 8,
        'spn': 9,
        'security_id': 10,
        'sedol': 11
    }
    heap = []
    data_path = input('Enter path to data csv: ')
    row_index = 0

    with open(data_path, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        next(datareader)  # Skip column title row

        for row in datareader:
            print('Row', row_index)
            row_index += 1

            # Longest substring match across all Street IDs for this security
            max_char_matches = 0
            # The priority 'weight' of this security. Calculated by adding the weights for all columns that had
            # any match for the query. Lower weight means greater priority.
            priority_weight = 0

            # Iterate over all Street IDs
            for i, street_id in enumerate(row[1:]):
                if street_id == '': continue

                char_matches = longest_common_substr(street_id.lower(), QUERY.lower(), len(street_id), len(QUERY))
                max_char_matches = max(max_char_matches, char_matches)

                # If there was any match
                if char_matches > 0:
                    priority_weight += i
                    # Assuming that the order of full matches in the output does not matter, breaking here would
                    # increase efficiency because this is a full-match, and no other Street ID for this row can have
                    # a better match.
                    if char_matches == len(QUERY): break

            # If there was any query match for this security, push to heap
            if max_char_matches > 0:
                security_id = row[0]
                heapq.heappush(heap, Node(security_id, max_char_matches, priority_weight))

    print_output(heap)


def print_output(heap):
    print(len(heap), 'results')
    # print out security for results, starting from 'most relevant'
    for i in range(len(heap)):
        print(i, heapq.heappop(heap))


if __name__ == '__main__':
    main()
