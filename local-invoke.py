from main import generate_response

"""
Entry point for local testing.

Call with: python local-invoke.py
"""


def main():
    print("Calling handler")
    response = generate_response()
    print(response)


if __name__ == "__main__":
    main()

