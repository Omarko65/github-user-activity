import argparse
from cachetools import cached, TTLCache
import requests

def parse_command(command_str):
    parser = argparse.ArgumentParser(description="Github User Activity Tracker")
    parser.add_argument("username", type=str, help="A unique identifier for the task")
    parser.add_argument("activity", type=str, nargs="?", choices=["Refresh", "ListAll"], help="Filter activity by event type")

    command_args = command_str.split()
    args = parser.parse_args(command_args)
    return args

cached_data = TTLCache(maxsize=3, ttl=120)

@cached(cache=cached_data)
def get_activity(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"Error Message": "Invalid username"}

def main():
    print("Welcome to Github User Activity Tracker!!!")
    print("Type 'exit' to end session")
    
    while True:
        command = input("\ngithub-activity ")
        events = []
        
        if command.strip() == 'exit':
            print("Goodbye!!!")
            break
             
        try:
            args = parse_command(command)
            url = f"https://api.github.com/users/{args.username}/events"
            data = get_activity(url)
    
            if args.activity is None:
                print(data) 
            elif args.activity == 'Refresh':
                cached_data.clear()
                data = get_activity(url)
                print("Activities refreshed successfully")
            elif args.activity == 'ListAll':
                print(data)
            else:
                events = [event for event in data if event['type'] == args.activity]
                print(events)

        except SystemExit:
            print("Invalid command. Please check your input.")

if __name__ == "__main__":
    main()
