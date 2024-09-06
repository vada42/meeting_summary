import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("NAVER_SPEECH_API_KEY")
class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/8969/8aab31fbcb5a766f78f3192626130c6af6771fdd9cf717e057dd199a751ff36a'
    # Clova Speech secret key
    secret = api_key

    # def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None, sed=None):
    #     request_body = {
    #         'url': url,
    #         'language': 'ko-KR',
    #         'completion': completion,
    #         'callback': callback,
    #         'userdata': userdata,
    #         'wordAlignment': wordAlignment,
    #         'fullText': fullText,
    #         'forbiddens': forbiddens,
    #         'boostings': boostings,
    #         'diarization': diarization,
    #         'sed': sed,
    #     }
    #     headers = {
    #         'Accept': 'application/json;UTF-8',
    #         'Content-Type': 'application/json;UTF-8',
    #         'X-CLOVASPEECH-API-KEY': self.secret
    #     }
    #     return requests.post(headers=headers,
    #                          url=self.invoke_url + '/recognizer/url',
    #                          data=json.dumps(request_body).encode('UTF-8'))

    # def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
    #                        wordAlignment=True, fullText=True, diarization=None, sed=None):
    #     request_body = {
    #         'dataKey': data_key,
    #         'language': 'ko-KR',
    #         'completion': completion,
    #         'callback': callback,
    #         'userdata': userdata,
    #         'wordAlignment': wordAlignment,
    #         'fullText': fullText,
    #         'forbiddens': forbiddens,
    #         'boostings': boostings,
    #         'diarization': diarization,
    #         'sed': sed,
    #     }
    #     headers = {
    #         'Accept': 'application/json;UTF-8',
    #         'Content-Type': 'application/json;UTF-8',
    #         'X-CLOVASPEECH-API-KEY': self.secret
    #     }
    #     return requests.post(headers=headers,
    #                          url=self.invoke_url + '/recognizer/object-storage',
    #                          data=json.dumps(request_body).encode('UTF-8'))

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        if not os.path.exists(file):
            return {"error": "파일 찾지못함(naver_speech.py/req_upload)"}
        try:

            request_body = {
                'language': 'ko-KR',
                'completion': completion,
                'callback': callback,
                'userdata': userdata,
                'wordAlignment': wordAlignment,
                'fullText': fullText,
                'forbiddens': forbiddens,
                'boostings': boostings,
                'diarization': diarization,
                'sed': sed,
            }
            headers = {
                'Accept': 'application/json;UTF-8',
                'X-CLOVASPEECH-API-KEY': self.secret
            }
            files = {
                'media': open(file, 'rb'),
                'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
            }
            response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
            return response
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}
    
def speaker_text_result(file_path):
    #파일 유효성 확인
    if not os.path.exists(file_path):
        return "Error: 파일잘못됨(naver_speech.py/speaker_text_result)."
    res = ClovaSpeechClient().req_upload(file=file_path, completion='sync')
    result = res.json()

    # API 호출이 성공적으로 이루어졌는지 확인
    if res.status_code != 200:
        return f"Error: {res.status_code}, {result}"

    # Extract speaker-segmented results
    segments = result.get('segments', [])
    speaker_segments = []

    speaker_text_result = ""

    for segment in segments:
        speaker_label = segment['speaker']['label']
        text = segment['text']
        speaker_segments.append({'speaker': speaker_label, 'text': text})


    # Print speaker-segmented results
    for speaker_segment in speaker_segments:
        speaker_label = speaker_segment['speaker']
        text = speaker_segment['text']
        speaker_text_result += f'Speaker {speaker_label}: {text}\n'# 회의 내용을 speaker_text_result 에 저장

    #print(speaker_text_result)
    return speaker_text_result