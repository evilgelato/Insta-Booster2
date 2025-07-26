import requests
import uuid

class Zefame:
    def __init__(self, url_video,service_id):
        self.url_video = url_video
        self.url = "https://zefame-free.com/api_free.php?action=order"
        self.uuid = str(uuid.uuid4())
        self.data = {
            "service": service_id,
            "link": url_video,
            "uuid": self.uuid,
            "postId": url_video.split("/")[4]
        }
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referrer": "https://zefame.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        }
        self.session = requests.session()

    def send_boost(self):
        try:
            response = self.session.post(self.url, data=self.data, headers=self.headers, timeout=15)
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get('success') == True:
                    return True
                elif (
                    isinstance(resp_json.get('data'), dict) and
                    resp_json['data'].get('timeLeft') is not None
                ):
                    return resp_json['data']['timeLeft']
                else:
                    return False
        except Exception as e:
            print("Error:", e)
        return False