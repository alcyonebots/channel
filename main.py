from pyrogram import Client
import asyncio

api_id = 123456   # Replace with your API ID
api_hash = "your_api_hash"  # Replace with your API Hash
session_name = "session"

# Phone number for login
phone_number = "+1234567890"  # Replace with your phone number

app = Client(session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)

async def send_file_to_user(file_path, user_id):
    # Send the links file to @voniq's DM
    await app.send_document(user_id, file_path)

async def main():
    async with app:
        # Login Process
        if not app.is_connected:
            print("Logging in...")
            await app.start()

        # Check for 2FA
        if await app.is_user_authorized():
            print("Already logged in.")
        else:
            # The app will automatically handle OTP and 2FA
            print("Logging in via phone number...")
            await app.sign_in(phone_number)

        print("What do you want to create?")
        print("1. Private Channels")
        print("2. Private Supergroups")
        choice = input("Enter 1 or 2: ")

        count = int(input("How many to create? "))

        # List to store the created links
        links = []

        for i in range(1, count + 1):
            if choice == "1":
                title = f"Channel {i}"
                # Creating a private channel (by default channels are private)
                new_channel = await app.create_channel(title=title, description="", is_megagroup=False)
                links.append(f"Channel {i}: https://t.me/{new_channel.username}")
                print(f"Created Private Channel: {title}")
            elif choice == "2":
                title = f"Group {i}"
                # Creating a private supergroup (is_megagroup=True means it's a supergroup)
                new_group = await app.create_channel(title=title, description="", is_megagroup=True)
                links.append(f"Group {i}: https://t.me/{new_group.username}")
                print(f"Created Private Supergroup: {title}")
            else:
                print("Invalid choice.")
                break

        # Save the links to a file
        with open("links.txt", "w") as f:
            for link in links:
                f.write(f"{link}\n")
        
        print("Links saved to links.txt")

        # Send the file to @voniq's DM (replace with the user ID of @voniq)
        await send_file_to_user("links.txt", "@voniq")

if __name__ == "__main__":
    asyncio.run(main())
