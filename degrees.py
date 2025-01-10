import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    '''
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    '''
    if len(sys.argv) != 4:
        sys.exit("Usage: python degrees.py [directory] [source] [target]")
    #directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    directory = sys.argv[1]
    source = sys.argv[2]
    target = sys.argv[3]

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # TESTING -------------------------------------------------------------------

    data = open("data.csv", "a")

    #source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
        #target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
        data.write(f"\"{source}\",\"{target}\",N\n")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        data.write(f"\"{source}\",\"{target}\",{degrees}\n")

    data.write("\n")
    data.close()


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairsp
    that connect the source to the target.

    If no possible path, returns None.
    """
    
    front = QueueFrontier()
    explored = set()
    path = list()

    front.add(Node(source, None, neighbors_for_person(source)))

    while True:

        path_data = open("path_data.csv", "a")
        path_data.write(f"\"{source}\",\"{target}\",{front.frontier}\n")
        path_data.close()

        if front.empty():
            return None
        
        next = front.remove()

        if next.state == target:
            return path
        else:
            for pair in next.action:
                added_node = Node(pair[1], pair[0], neighbors_for_person(pair[1]))
                if added_node.state not in explored and front.contains_state(added_node.state) == False:
                    if added_node.state == target:
                        path.append((added_node.parent, added_node.state))
                        return path
                    else:
                        front.add(added_node)
                        
            explored.add(next.state)

        if len(explored) != 1:
            path.append((next.parent, next.state))


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:

        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
