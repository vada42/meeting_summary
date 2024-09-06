from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile, Body
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
from clean_and_volumup_copy_Complete_form import clean_up_audio
from naver_speech_Complete_form import speaker_text_result
from openai_summary_3_Complete_form import creat_summary

# powershell-> ngrok http http://localhost:8080
# uvicorn main_copy3_Complete_form:app --reload --port 8080 

app = FastAPI()
@app.get('/')
def  open():
    return {"message":"opening"}

@app.post('/cleaning_summary/')
async def cleaning_audio(file: UploadFile = File(...)):
    cleaning_audio = clean_up_audio(file)
    meeting_text = speaker_text_result(cleaning_audio)
    summary_file_path = creat_summary(meeting_text)


    if summary_file_path and os.path.exists(summary_file_path):
        return FileResponse(path=summary_file_path, media_type='application/json', filename="meeting_summary.json")
    else:
        return {"error": "요약 파일 생성 중 오류가 발생했습니다."}
    
# mp3 , wav 다 받음
# json 파일 생성 문제 해결됨