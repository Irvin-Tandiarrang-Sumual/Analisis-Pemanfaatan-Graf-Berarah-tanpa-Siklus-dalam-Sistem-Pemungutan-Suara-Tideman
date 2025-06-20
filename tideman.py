import csv
import sys
import json
# Global data structures
preferences = []       # preferences[i][j] is number of voters who prefer candidate i over j
locked = []            # locked[i][j] is True if i is locked in over j (i → j)
candidates = []        # list of candidate names
pairs = []             # list of winning candidate pairs
pair_count = 0         # total number of pairs
candidate_count = 0    # number of candidates

# Class to represent a pair of candidates (winner beats loser)
class Pair:
    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser

# Update the ranks array with the index of the candidate that matches the name
def vote(rank, name, ranks):
    for i in range(candidate_count):
        if name == candidates[i]:
            ranks[rank] = i
            return True
    return False

# Update global preferences matrix based on a single voter's ranks
def record_preferences(ranks):
    for i in range(candidate_count): 
        found = False
        for j in range(candidate_count):  
            if ranks[j] == i:
                found = True
            elif found:  # If i was found earlier, i is preferred over ranks[j]
                preferences[i][ranks[j]] += 1

# Add all pairs of candidates where one is preferred over the other
def add_pairs():
    global pair_count
    for i in range(candidate_count):
        for j in range(i + 1, candidate_count):
            if preferences[i][j] > preferences[j][i]:
                pairs.append(Pair(i, j))
                pair_count += 1
            elif preferences[j][i] > preferences[i][j]:
                pairs.append(Pair(j, i))
                pair_count += 1

# Sort the pairs in decreasing order of strength of victory
def sort_pairs():
    def get_strength(pair):
        return preferences[pair.winner][pair.loser]
    pairs.sort(key=get_strength, reverse=True)

# Lock pairs into the candidate graph without creating cycles
def lock_pairs():
    for pair in pairs:
        locked[pair.winner][pair.loser] = True     
        if path_exists(pair.loser, pair.winner):
            locked[pair.winner][pair.loser] = False

# Recursive function to check whether a path exists 
# from one candidate to another (to avoid cycles)
def path_exists(from_cand, to_cand, visited=None):
    if visited is None:
        visited = set()
    
    if to_cand in visited:
        return True
        
    visited.add(from_cand)
    
    for i in range(candidate_count):
        if locked[i][from_cand]:
            if path_exists(i, to_cand, visited.copy()):
                return True
    return False

# Print the winner: the candidate with no edges pointing to them (i.e., source of the graph)
def print_winner():
    for i in range(candidate_count):
        if all(not locked[j][i] for j in range(candidate_count)):
            print(f"Winner: {candidates[i]}")
            return
        
def main():
    global preferences, locked, candidates, candidate_count
    
    # Require a CSV file as input
    if len(sys.argv) < 2:
        print("Usage: python tideman.py input.csv")
        sys.exit(1)

    try:
        # Open and parse the input CSV file
        with open(sys.argv[1]) as f:
            reader = csv.reader(f)
            candidates = next(reader)  # First row is the list of candidates
            candidate_count = len(candidates)
            
            # Initialize preferences and locked graph with default values
            preferences = [[0 for _ in range(candidate_count)] for _ in range(candidate_count)]
            locked = [[False for _ in range(candidate_count)] for _ in range(candidate_count)]
            
            # Process each voter's ballot
            for ballot in reader:
                if len(ballot) != candidate_count:
                    print(f"Invalid ballot: {ballot}")
                    continue
                
                # Convert names to ranks
                ranks = [0] * candidate_count
                for rank, name in enumerate(ballot):
                    if not vote(rank, name, ranks):
                        print(f"Invalid candidate: {name}")
                        sys.exit(3)
                
                # Update preferences based on this voter's ranks
                record_preferences(ranks)
                
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)

    add_pairs()     
    # Untuk melihat pairs sebelum sorting
    # print("Pairs (before sorting):")
    # for pair in pairs:
    #     print(f"{candidates[pair.winner]} beats {candidates[pair.loser]} with margin {preferences[pair.winner][pair.loser] - preferences[pair.loser][pair.winner]}")

    sort_pairs()    
    # Untuk melihat pairs setelah sorting
    # print("\nPairs (after sorting):")
    # for pair in pairs:
    #     margin = preferences[pair.winner][pair.loser] - preferences[pair.loser][pair.winner]
    #     print(f"{candidates[pair.winner]} > {candidates[pair.loser]} (margin: {margin})")

    lock_pairs()    
    print_winner()

    # Untuk melihat hasil dari preferences matrix
    # print("Preferences Matrix:")
    # print("            ", "  ".join(f"{name:8}" for name in candidates))
    # for i, row in enumerate(preferences):
    #     print(f"{candidates[i]:8} ", "  ".join(f"{val:8}" for val in row))

    # Untuk melihat hasil dari locked matrix
    # print("Locked Matrix:")
    # print("        ", "  ".join(f"{name:8}" for name in candidates))
    # for i, row in enumerate(locked):
    #     print(f"{candidates[i]:8} ", "  ".join(f"{'T' if val else 'F':8}" for val in row))

    # Simpan hasil ke file JSON
    # Agar bisa ditampilkan visualisasi grafnya dengan visualisasi_tideman.py
    with open("hasil_tideman.json", "w") as f:
        json.dump({
            "candidates": candidates,
            "locked": locked
        }, f)


if __name__ == "__main__":
    main()
