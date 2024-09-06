import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# from naver_speech import speaker_text_result
# .env 파일에서 환경 변수 로드
load_dotenv()

# .env 파일에서 API 키 로드
api_key = os.getenv("OPENAI_API_KEY")

# ChatOpenAI 모델 초기화
chat_model = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=api_key, temperature=0.7)

# JSON 형식으로 변환할 필드를 정의 (ResponseSchema를 사용)
class MeetingSummarySchema(BaseModel):
    회의내용: str = Field(..., description="회의의 주요 내용")
    결론_및_합의: str = Field(..., description="회의에서 내린 결론과 합의된 사항")
    해야_할_일: str = Field(..., description="회의 후 할 일 목록")
    참고_사항: str = Field(..., description="추가로 참고해야 할 사항들")

# Output parser 설정
response_schemas = [
    ResponseSchema(name="회의내용", description="회의의 주요 내용"),
    ResponseSchema(name="결론 및 합의", description="회의에서 내린 결론과 합의된 사항"),
    ResponseSchema(name="해야 할 일", description="회의 후 해야 할 일 목록"),
    ResponseSchema(name="참고 사항", description="추가로 참고해야 할 사항들"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 시스템 메시지: 요약 작업을 설명
system_message = SystemMessage(content="""당신은 회의를 요약하는 AI입니다.
                               회의의 핵심 내용을 간결하고 명확하게 요약하세요.
                               요약에는 '회의내용', '결론 및 합의', '해야 할 일', '참고 사항' 항목이 포함되어야 합니다.
                               요약을 반드시 JSON 형식으로 반환하세요.
                               형식: {"회의내용": "...", "결론 및 합의": "...", "해야 할 일": "...", "참고 사항": "..."}""")



# 사용자 입력 받기 (회의 내용)
def creat_summary(meeting_text):

    #user_input = meeting_text

    # 입력된 회의 내용을 시스템 메시지와 함께 전달
    messages = [
        system_message,
        HumanMessage(content=meeting_text)
    ]

    # 모델에 메시지를 보내고 요약된 결과 받기
    response = chat_model(messages)

    # 응답을 파싱하여 JSON으로 변환
    parsed_output = output_parser.parse(response.content)

    # 요약된 문장 출력 (JSON 형식으로 반환)
    # summary = response.content.strip()

    # 출력된 내용을 확인하기 위해 출력
    print("요약된 회의 내용 (JSON 형식):")
    print(parsed_output)

    # 파일을 저장할 폴더 경로 지정
    output_folder = "meeting_jsonfile"
    os.makedirs(output_folder, exist_ok=True)  # 폴더가 없으면 생성

    # 저장할 파일 경로 설정
    output_file_path = os.path.join(output_folder, "meeting_summary.json")

# JSON 형식으로 파일 저장
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(parsed_output, f, ensure_ascii=False, indent=4)

    # 결과 파일 경로 반환
    return output_file_path
