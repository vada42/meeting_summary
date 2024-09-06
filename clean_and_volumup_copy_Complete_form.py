import numpy as np
import noisereduce as nr
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydub import AudioSegment
import shutil
import io
import os
from fastapi.responses import FileResponse

def clean_up_audio(file: UploadFile):
    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="파일을 받지 못함.")
    try: # 파일 확장자 확인
        file_extension = os.path.splitext(file.filename)[1].lower()  # 파일 확장자 추출 및 소문자로 변환

        # 확장자에 맞는 형식 설정 (지원하는 파일 형식 지정)
        if file_extension == ".mp3":
            file_format = "mp3"
        elif file_extension == ".wav":
            file_format = "wav"
        elif file_extension =='m4a':
             file_format = "m4a"
        else:
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다. mp3 또는 wav 파일을 업로드하세요.")

        # 업로드된 파일을 BytesIO로 변환하여 AudioSegment에서 처리 가능하도록 함
        file_bytes = file.file.read()
        audio = AudioSegment.from_file(io.BytesIO(file_bytes), format=file_format)

        # 오디오를 numpy 배열로 변환 (int16으로 변환)
        samples = np.array(audio.get_array_of_samples()).astype(np.int16)

        # 샘플링 레이트 지정 (기본값: 44.1kHz)
        sampling_rate = audio.frame_rate

        # 노이즈 감소 적용
        reduced_noise = nr.reduce_noise(y=samples, sr=sampling_rate)

        # 노멀라이제이션 적용 (신호를 float32로 변환한 후 최대 진폭으로 나눔)
        normalized_signal = (reduced_noise / np.max(np.abs(reduced_noise))).astype(np.float32)

        # normalized_signal를 다시 int16로 변환하기 전에 스케일링
        scaled_signal = (normalized_signal * np.iinfo(np.int16).max).astype(np.int16)

        # scaled_signal를 AudioSegment로 변환
        final_audio = AudioSegment(
            scaled_signal.tobytes(), 
            frame_rate=sampling_rate, 
            sample_width=audio.sample_width, 
            channels=audio.channels
        )

        # 볼륨을 증가시키기 (예: +5dB)
        louder_audio = final_audio + 5

        # 노이즈 제거 후 볼륨을 증가시킨 오디오 저장
        output_path = "louder_cleaned_audio.mp3"
        louder_audio.export(output_path, format="mp3")

        # 처리된 파일 경로 반환
        return output_path
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
