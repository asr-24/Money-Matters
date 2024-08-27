from dotenv import load_dotenv
import os

load_dotenv()

internal_integration_secret = os.getenv("Internal_Integration_Secret")

print("Internal Integration Secret: ", internal_integration_secret)

