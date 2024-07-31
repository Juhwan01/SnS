from langchain_openai import ChatOpenAI
from langchain_teddynote.models import MultiModal
from dotenv import load_dotenv

load_dotenv()

system_prompt = """
당신은 인기 있는 라이프스타일 인플루언서입니다. 일상의 순간들을 진솔하고 매력적으로 공유하는 것으로 유명합니다.
당신의 포스트는 항상 진실되고, 개인적이며, 팔로워들과 깊은 유대감을 형성합니다.
트렌디하면서도 당신만의 독특한 개성을 잃지 않는 방식으로 콘텐츠를 만듭니다.
"""

user_prompt = """
제공된 이미지를 당신의 일상 중 한 순간으로 간주하고, 인스타그램 포스트를 위한 다음 내용을 생성해주세요:

1. 해시태그 (최대 5개):
   - 당신의 일상, 감정, 경험을 반영하는 태그
   - 개인적이고 친근한 느낌의 태그 포함
   - 트렌디하면서도 자연스러운 태그 사용
   - 한글 또는 영어 사용 가능
   - 각 태그 앞에 '#' 기호 사용

2. 캡션 (200자 이내, 한국어):
   - 이미지와 관련된 개인적인 이야기나 감정을 공유
   - 친근하고 대화하는 듯한 톤 사용
   - 팔로워들과 소통하는 느낌을 주는 문구 포함 (예: 질문하기)
   - 자연스럽게 이모지 사용

결과는 다음 형식으로 제공해주세요:
해시태그: #태그1 #태그2 #태그3 #태그4 #태그5
캡션: [생성된 캡션]

주의: 이미지에 텍스트가 포함된 경우, 그 내용을 직접 인용하지 마세요. 대신 그 상황에 대한 당신의 개인적인 생각이나 느낌을 표현하세요.
"""


# LLM 및 멀티모달 객체 설정
llm = ChatOpenAI(
    temperature=0.1,  # 창의성 조절
    max_tokens=2048,  # 최대 토큰 수 설정
    model_name="gpt-4o"  # 멀티모달 기능을 지원하는 모델 이름
)

# 멀티모달 객체 생성
multimodal_llm_with_prompt = MultiModal(
    llm, system_prompt=system_prompt, user_prompt=user_prompt
)

image_path = "img3.png"

answer = multimodal_llm_with_prompt.invoke(image_path)

print (answer)
