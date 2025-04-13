import time
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired


# Function to login to Telegram using phone number and 2FA if necessary
def login_to_telegram():
    phone_number = input("Enter your phone number (with country code, e.g., +1): ")  # Get phone number from user input
    api_id = '23786344'  # Replace with your API ID
    api_hash = '90decd3d66ff2bbb1d0ade8bde0b71b0'  # Replace with your API Hash

    app = Client("my_account", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

    try:
        app.start()  # Starts the client
        print("Logged in successfully!")

        # Check if 2FA (two-step verification) is enabled
        if isinstance(app, SessionPasswordNeeded):
            password = input("Enter your 2FA password: ")
            app.check_password(password)
            print("Logged in successfully!")
            
    except PhoneCodeInvalid:
        print("Invalid OTP. Please try again.")
        return None
    except PhoneCodeExpired:
        print("OTP has expired. Please request a new one.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return app


# Function to create channels or supergroups with custom titles
def create_channel_or_group(client):
    print("Menu:")
    print("1. Create Channel")
    print("2. Create Supergroup")
    choice = input("Please choose an option (1 or 2): ").strip()

    if choice == '1':
        option = 'channel'
    elif choice == '2':
        option = 'supergroup'
    else:
        print("Invalid choice. Exiting.")
        return

    # Ask for how many channels or supergroups to create
    count = int(input(f"How many {option}s do you want to create? "))
    
    for i in range(count):
        title = f"{option.capitalize()} {i + 1}"
        print(f"Creating {option} '{title}' with title '{title}'...")

        if option == 'channel':
            # Corrected the call to create_channel with the right parameters
            client.create_channel(title=title, description='', is_private=True)
            print(f"Channel '{title}' created successfully!")

        elif option == 'supergroup':
            # Create a supergroup by first creating a normal group and then promoting it to a supergroup
            group = client.create_group(title=title, description='', is_private=True)
            # Promote the group to supergroup
            group.promote_to_supergroup()
            print(f"Supergroup '{title}' created successfully!")


# Start the login process
client = login_to_telegram()

# Proceed with creating channels or supergroups after successful login
if client:
    create_channel_or_group(client)
