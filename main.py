from map import Map
from endpoint_secrets import kCandidateId

def main():
    print("Hi! Welcome to the Crossmint Map Generator!")
    print("Do you want to use the default candidateId? (y/n)")
    use_default = input()
    if use_default == "n":
        candidateId = input("Please enter the candidateId: ")
        map = Map(candidateId)
        map.getGoalMap()
    else:
        map = Map(kCandidateId)
        map.getGoalMap()
    print("To generate the goal map, type 'generate'")
    print("To delete all entities, type 'delete'")
    while True:
        action = input("What would you like to do? (generate/delete): ")
        if action == "generate":
            map.generateGoalMap()
        elif action == "delete":
            map.deleteAllEntities()
        else:
            print("Invalid action. Please try again.")
            return

main()