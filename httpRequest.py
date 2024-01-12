from ModemLib import ModemLib  # Import the ModemLib class

def main():
    try:
        # Initialize the ModemLib class
        modem = ModemLib()

        # Webhook.site URL
        webhook_url = "https://webhook.site/a0559e00-7985-4099-b8f5-d5161b4b771f"

        # Send HTTP GET request
        print("HTTP GET Request:")
        get_response = modem.perform_http_request(webhook_url, method='GET')
        print_response(get_response)

        # Send HTTP POST request
        print("\nHTTP POST Request:")
        post_data = "sample_data=12345"
        post_response = modem.perform_http_request(webhook_url, method='POST', data=post_data)
        print_response(post_response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the modem connection
        modem.close_connection()

def print_response(response):
    # Print the HTTP request response to the console
    print("Response:")
    for line in response['response']:
        print(line)

if __name__ == "__main__":
    main()
