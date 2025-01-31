import csv
import sys
import copy

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
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Agent
    # States = people
    # Actions = movies
    # Transition model (in a finite tree of actors and movies, this may be what the tree looks like after making a certain action or which nodes are explored)
    
    # Initial state = source
    # Goal state = target

    # Goal test = if statement that checks if we have gotten to target
    
    # Using iterative search, similar to breadth-first search
    depth = 1
    depth_limit = 1000000

    front = QueueFrontier()
    explored = set()
    path = list()

    # NODE STRUCTURE
    # State = source id, distance from source
    # Parent = movie, list of people preceding it
    # Action = people ahead of it

    # Add root node
    front.add(Node(
        (source, 0), 
        [None, []], 
        neighbors_for_person(source))
    )

    while True:

        if front.empty():
            depth += 1
        else:
            next = front.remove()

        print(depth)

        if depth == depth_limit:
            return None
        
        if next.state[0] == target:
            return path
        else:
            for pair in next.action:

                history = list(copy.deepcopy(next.parent[1]))
                history.append(next.state[0])

                added_node = Node(
                    (pair[1], len(next.parent[1]) + 1), # Distance from source
                    [pair[0], history], # The movie, along with the people before it
                    neighbors_for_person(pair[1])
                )
                
                if added_node.state[0] not in explored:
                    if added_node.state[0] == target:
                        path.append((added_node.parent[0], added_node.state[0]))
                        return path
                    else:
                        # This is where depth comes into play
                        if added_node.state[1] == depth:
                            front.add(added_node)
                        
            explored.add(next.state[0])

        if len(explored) != 1:
            path.append((next.parent[0], next.state[0]))


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
