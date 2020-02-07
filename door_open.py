import configuration
import requests


def doorOpen():
    try:
        rep = requests.post(configuration.door_url,
                            data={'secret': configuration.door_serect},
                            # cert=("data/self_cert.pem", "data/self_key.pem"),
                            verify=False)
    except requests.exceptions.RequestException as e:
        print(e)
        return False
    if rep.status_code == 200 and rep.json().get('ok'):
        return True
    print(rep)
    return False


if __name__ == "__main__":
    if doorOpen():
        print("OK")
    else:
        print("Fail")
