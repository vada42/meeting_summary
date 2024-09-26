<img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white"/> 3.10.14


<img src="https://img.shields.io/badge/openai-412991?style=flat-square&logo=openai&logoColor=white"/> gpt4-turbo


<img src="https://img.shields.io/badge/naver-03C75A?style=flat-square&logo=naver&logoColor=white"/> naver clova speech


<img src="https://img.shields.io/badge/pytorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/> import 
'2.3.0+cu121'


이 코드는 받은 회의 음성파일을 회의 요약록으로 반환하는 코드입니다
<img width="250" alt="image" src="https://github.com/user-attachments/assets/da29cc8e-8c8f-4409-aec3-375fde002258">
```
pip install fastapi==0.112.2
pip install noisereduce==3.0.2
pip install pydub==0.25.1
pip install requests==2.32.3
pip install langchain==0.2.16
pip install pydantic==2.8.2
```
실행에 앞서 필요한 모듈입니다
막약 해당 모듈들을 다운로드 받고 실행을 했을 때 작동이 안된 경우 requirements.txt 안에 있는 모듈들을 설치합니다
터미널 창에서 실행 해주시길 바랍니다
```
pip install -r requirements.txt
```
회의 음성파일을 받고 최종 결과물을 아래와 같은 양식의 string타입으로 반환됩니다
###### 회의내용: XR 박유진, 정민주, 조여원, AI 장재웅, TA 정보형으로 구성된 TT 빵빵토 팀은 메타버스 공간에서 사용할 수 있는 운전면허 필기 및 장내 기능 시험 연습 플랫폼 '장필 기정' 개발에 대해 논의했습니다. 이 플랫폼은 멀티플레이 형식의 필기 시험 및 모션 인식 기술을 활용한 장내 기능 시험을 제공할 예정입니다. 팀 구성원 각자의 역할과 플랫폼의 개발 순서, 기능에 대해 상세히 설명하였습니다.\n\n결론 및 합의: 개발할 주요 기능들을 확정하고, 각 팀원의 역할 분담을 명확히 하였습니다. 필기 시험은 게임 형식으로, 장내 기능 시험은 모션 인식을 활용하여 현실감 있게 구현하기로 결정하였습니다.\n\n해야 할 일: AI 장재웅은 모션 인식과 CTS 문제 제공을, 나머지 팀원들은 앱의 주요 기능 구현 및 데이터 연동을 맡게 됩니다. 또한, 유니티 팀은 데이터 연동 전 주요 UI 관련 기능을 완성하고, 필기 및 기능 시험의 멀티플레이 및 데이터 연동 기능 개발을 우선순위로 설정하여 진행합니다.\n\n참고 사항: 네트워크를 활용한 멀티플레이 기능의 목적과 구체적인 사용 방법에 대한 질문이 제기되었으며, 이는 추후 논의가 필요함을 시사합니다. 또한, 필기와 기능 시험의 채점 방식이 개별적으로 이루어질 것임이 확인되었습니다.

터미널 창에서 아래와 같이 진행경과를 확인할수 있습니다
<img width="1100" alt="image" src="https://github.com/user-attachments/assets/634a4ed3-fc4c-492a-bc91-6f38792f8fd8">

회의음성파일은 mp3, wav를 받을 수 있고 문제없이 작동하는 것을 확인할 수 있었습니다
m4a형식도 받을 수 있게끔 했지만 아직까지는 파악하지 못한 문제가 있기 때문에 작동하지 않습니다
가능하면 mp3와 wav 파일형식을 이용하십시오
<img width="680" alt="image" src="https://github.com/user-attachments/assets/7c5ab9f9-af61-44e7-b825-5214aaa72ddd">

회의음질이 좋지 않을 경우를 대비해서 음질향상과 볼륨크기를 키워주는 코드들이 clean_and_volumup_copy_Complete_form.py 에 내재되어 있습니다
<img width="509" alt="image" src="https://github.com/user-attachments/assets/51a0a635-db55-4a94-83cc-b6329b4994ac">

화자분할과 STT는 naver clova의 clova의 speech를 사용합니다
초기에는 whisper 모델을 사용했지만 성능이 좋지 않아서 clova의 speech를 사용하게되었습니다
https://api.ncloud-docs.com/docs/ai-application-service-clovaspeech-longsentence






