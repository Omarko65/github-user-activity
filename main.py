import argparse
from cachetools import cached, TTLCache
import requests

def parse_command(command_str):
    parser = argparse.ArgumentParser(description="Github User Activity Tracker")
    parser.add_argument("username", type=str, help="A unique identifier for the task")
    parser.add_argument("activity", type=str, nargs="?", choices=["Refresh", "ListAll", "CreateEvent", "PullRequestEvent", "IssuesEvent", "ForkEvent", "DeleteEvent", "PushEvent", "WatchEvent"], help="Refresh Cache, ListAll activities, or list activity by event type")

    command_args = command_str.split()
    args = parser.parse_args(command_args)
    return args

cached_data = TTLCache(maxsize=3, ttl=900)

@cached(cache=cached_data)
def get_activity(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"Error Message": "Invalid username"}

#Custom message to print
def event_msg(actions, activity=None):
    if len(actions) == 1: return([{"Error Message": "Invalid Username"}])
    action_list = []
    activity_list = []
    for dict in actions:
        for key, val in dict.items():
            if key == 'CreateEvent':
                branch = dict['payload'].count('branch')
                action_list.append(f"Created new repository {dict['name']}")
                if branch > 1: action_list.append(f"Created {branch-1} new branch ")
                if activity == 'CreateEvent': activity_list.append(f"Created new repository {dict['name']}")
                if activity == 'CreateEvent' and branch > 1: activity_list.append(f"Created {branch-1} new branch ")

            elif key == 'WatchEvent':
                action_list.append(f"Starred {dict['name']} repo")
                if activity == 'WatchEvent': activity_list.append(f"Starred {dict['name']} repo")

            elif key == 'PushEvent':
                action_list.append(f"Pushed {val} commits to {dict['name']}")
                if activity == 'PushEvent': activity_list.append(f"Pushed {val} commits to {dict['name']}")
                    
            elif key == 'DeleteEvent':
                action_list.append(f"Deleted {val} branches in {dict['name']}")
                if activity == 'DeleteEvent': activity_list.append(f"Deleted {val} branches in {dict['name']}")

            elif key == 'ForkEvent':
                action_list.append(f"Forked {dict['name']}")
                if activity == 'ForkEvent': activity_list.append(f"Forked {dict['name']}")

            elif key == 'IssuesEvent':
                action_list.append(f"Created {val} issue")
                if activity == 'IssuesEvent': activity_list.append(f"Created {val} issue")

            elif key == 'PullRequestEvent':
                action_list.append(f"Created {val} Pull Request")
                if activity == 'PullRequestEvent': activity_list.append(f"Created {val} Pull Request")

    if activity:
        return activity_list
    else:
        return action_list
        
    
        

# Data sorting algorithm
def sort_data(data):
    if len(data) == 1: return({"Error Message": "Invalid username"})
    repo_id = []
    repos = []
    for event in data:
        # loop through returned data and match repo id with repo we have
        if event["repo"]["id"] in repo_id:
            event_id = event["repo"]["id"]
            # save repo id
            for repo in repos:
                # checking repos dict for repo
                if repo["id"] == event_id:
                    try:
                        repo[event["type"]] += 1
                        if event["type"] == "CreateEvent": repo["payload"].append(event["payload"]["ref_type"])


                        # update event type if it exits
                    except KeyError:
                        repo[event["type"]] = 1
                        if event["type"] == 'CreateEvent': repo["payload"] = [event['payload']['ref_type']]

                        # initialize event type if it doesn't exist
            
        else:
            # create repo dict if we don't have the repo id 
            repo = {
                'name': event["repo"]["name"],
                'id': event["repo"]["id"],
                event["type"]: 1
            }
            if event["type"] == 'CreateEvent': repo["payload"] = [event['payload']['ref_type']]
            # add repo to repos gotten
            repos.append(repo)
            repo_id.append(event["repo"]["id"])
        
    return (repos)


def main():
    print("Welcome to Github User Activity Tracker!!!")
    print("Type 'exit' to end session")
    
    while True:
        command = input("\ngithub-activity ")
        events = []
        repos = []
        
        if command.strip() == 'exit':
            print("Goodbye!!!")
            break
             
        try:
            args = parse_command(command)
            url = f"https://api.github.com/users/{args.username}/events"
            data = get_activity(url)
            

            datas = sort_data(data)
            if args.activity is None:
                results = event_msg(datas) 
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'CreateEvent':
                results = event_msg(datas, 'CreateEvent')
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'PullRequestEvent':
                results = event_msg(datas, 'PullRequestEvent')
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'IssuesEvent':
                results = event_msg(datas, 'IssuesEvent')
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'WatchEvent':
                results = event_msg(datas, 'WatchEvent')
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'PushEvent':
                results = event_msg(datas, 'PushEvent')                
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'DeleteEvent':
                results = event_msg(datas, 'DeleteEvent')
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'ForkEvent':
                results = event_msg(datas, 'ForkEvent')
                [print(result) for result in results] if results else print('Activity not found')
                
            elif args.activity == 'ListAll':
                results = event_msg(datas)
                [print(result) for result in results] if results else print('Activity not found')
            elif args.activity == 'Refresh':
                cached_data.clear()
                data = get_activity(url)
                print("Activities refreshed successfully")

        except SystemExit:
            print("Invalid command. Please check your input.")

if __name__ == "__main__":
    main()
