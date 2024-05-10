import requests
import window
import traceback

if __name__ == '__main__':
    try:
        while True:
            try:
                if requests.get('http://example.com/').status_code == 200:
                    window.run()
                    break

                elif not window.no_internet.run():
                    break

            except requests.exceptions.ConnectionError:
                if not window.no_internet.run():
                    break

    except Exception as e:
        traceback.print_exc()
