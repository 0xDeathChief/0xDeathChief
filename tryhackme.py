import requests
from bs4 import BeautifulSoup

# Your TryHackMe username
username = "ExploitByte"
profile_url = f"https://tryhackme.com/r/p/{username}"

def fetch_completed_rooms(username):
    url = f"https://tryhackme.com/p/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch TryHackMe profile: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find completed rooms (update this based on TryHackMe's structure)
    rooms_section = soup.find('div', class_='completed-rooms')
    if not rooms_section:
        return []

    rooms = [room.text.strip() for room in rooms_section.find_all('a')]
    return rooms

def update_readme(rooms):
    # Read the current README
    with open("README.md", "r") as file:
        lines = file.readlines()

    # Update the section for TryHackMe rooms
    start_marker = "<!-- TRYHACKME-ROOMS-START -->"
    end_marker = "<!-- TRYHACKME-ROOMS-END -->"
    start_index = lines.index(start_marker + "\n") + 1
    end_index = lines.index(end_marker + "\n")

    new_content = "\n".join([f"- {room}" for room in rooms]) + "\n"
    lines[start_index:end_index] = [new_content]

    # Write back to the README
    with open("README.md", "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    try:
        rooms = fetch_completed_rooms(username)
        update_readme(rooms)
        print("Updated README with completed rooms.")
    except Exception as e:
        print(f"Error: {e}")
