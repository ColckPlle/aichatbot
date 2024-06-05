import pandas as pd

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드한다
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 레벤슈타인 거리를 계산
    def calc_distance(self, a, b):
        if a == b: return 0
        a_len = len(a)
        b_len = len(b)
        if a == "": return b_len
        if b == "": return a_len

        matrix = [[] for i in range(a_len+1)]
        for i in range(a_len+1):
            matrix[i] = [0 for j in range(b_len+1)]
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j
        for i in range(1, a_len+1):
            ac = a[i-1]
            for j in range(1, b_len+1):
                bc = b[j-1]
                cost = 0 if (ac == bc) else 1
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,
                    matrix[i][j-1] + 1,
                    matrix[i-1][j-1] + cost
                ])
        return matrix[a_len][b_len]

    def find_best_answer(self, input_sentence):
            min_distance = float('inf')
            best_match_index = -1
            for i, question in enumerate(self.questions):
                distance = self.calc_distance(input_sentence, question)
                if distance < min_distance:
                    min_distance = distance
                    best_match_index = i
            print(f"레벤슈타인 거리: {min_distance}")
            return self.answers[best_match_index]

# 데이터 파일의 경로를 지정합니다.
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)