import kakao_utils
import sys
sys.path.append('C:/Users/user/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages')
import beepy

# 컴퓨터에 내장된 소리를 출력
def beepsound():
    beepy.beep(sound=6)
    
# 카카오톡 메시지로 '졸음 방지 베타파' 영상 링크를 전송    
def send_music_link():
    KAKAO_TOKEN_FILENAME = "C:/Users/user/Desktop/Python work spapce/kakao_token.json"# "<kakao_token.json 파일이 있는 경로를 입력하세요.>" 
    KAKAO_APP_KEY = "3b34f2e7f557ef84bf043fccf76e1791"
    tokens = kakao_utils.update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)
    

    # 텍스트 메시지 보내기
    template = {
          "object_type": "text",
          "text": "당신은 30초 이상 졸았습니다. 졸지 마세요!!!!",
          "link": {
            "web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o",
            "mobile_web_url": "https://www.youtube.com/watch?v=7Q2N7919o5o"
          },
          "button_title": "잠깨는 노래 듣기"
    }

    # 카카오 메시지 전송
    res = kakao_utils.send_message(KAKAO_TOKEN_FILENAME, template)
    if res.json().get('result_code') == 0:
        print('텍스트 메시지를 성공적으로 보냈습니다.')
    else:
        print('텍스트 메시지를 보내지 못했습니다. 오류메시지 : ', res.json())



# 테스트 ↓

# beepsound() 함수 호출
beepsound()

# send_music_link() 함수 호출
send_music_link()