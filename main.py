from map import Map
from endpoint_secrets import kCandidateId

def main():
    print("Hi! Welcome to the Crossmint Map Generator!")
    print("Do you want to use the default candidateId? (y/n)")
    use_default = input()
    if use_default == "n":
        candidateId = input("Please enter the candidate ID: ")
        map = Map(candidateId)
        map.getGoalMap()
    else:
        map = Map(kCandidateId)
        map.getGoalMap()
    print("To generate the goal map, type 'generate'")
    print("To delete all entities, type 'delete'")
    print("To exit, type 'exit'")
    while True:
        action = input("What would you like to do? (generate/delete/exit): ")
        if action == "generate":
            map.generateGoalMap()
        elif action == "delete":
            map.deleteAllEntities()
        elif action == "exit":
            print("Goodbye!")
            return
        else:
            print("Invalid action. Please try again.")
            return

main()