# 20-07-06_29

from keras.preprocessing.text import Tokenizer
import numpy as np

docs = ['너무 재밌어요', '참 최고에요', '참 잘 만든 영화에요',
        '추천하고 싶은 영화입니다', '한 번 더 보고 싶네요', '글쎄요',
        '별로에요', '생각보다 지루해요', '연기가 어색해요',
        '재미없어요', '너무 재미없다', '참 재밌네요']

# 긍정 1, 부정 0
labels = np.array([1,1,1,1,1,0,0,0,0,0,0,1])

# 토큰화
token = Tokenizer()
token.fit_on_texts(docs)
print(token.word_index)

# <너무 2번, 참 2번 일 때,>
# {'너무': 1, '참': 2, '재밌어요': 3, '최고에요': 4, '잘': 5, '만든': 6, '영화에요': 7, '추천하고': 8, '싶은': 9, '영화입니다': 10, ' 10, '한번': 11, '더': 12, '보고': 13, '싶네요': 14, '글쎄요': 15, '별로에요': 16, '생각보다': 17, '지루해요': 18, '연기가': 9  해 
# 19, '어색해요': 20, '재미없어요': 21, '재미없다': 22, '재밌네요': 23}

# <너무 2번, 참 3번 일 때,> : 단어가 많은 것이 맨 앞 인덱스로 정렬
# {'참': 1, '너무': 2, '재밌어요': 3, '최고에요': 4, '잘': 5, '만든': 6, '영화에요': 7, '추천하고': 8, '싶은': 9, '영화입니다': 10, '한번': 11, '더': 12, '보고': 13, '싶네요': 14, '글쎄요': 15, '별로에요': 16, '생각보다': 17, '지루해요': 18, '연기가': 
# 19, '어색해요': 20, '재미없어요': 21, '재미없다': 22, '재밌네요': 23}

x = token.texts_to_sequences(docs)
print(x)
# [[2, 3], [1, 4], [1, 5, 6, 7], [8, 9, 10], [11, 12, 13, 14], [15], [16], [17, 18], [19, 20], [21], [2, 22], [1, 23]]
from keras.preprocessing.sequence import pad_sequences
pad_x = pad_sequences(x, padding='post', value=0)   # Defalut (0과 pre : 그만큼 이 조합이 많이 쓰인 다는 것)
print(pad_x)
print('==================================================================================')
pad_x = pad_sequences(x, padding='pre', value=0)   # Defalut (0과 pre : 그만큼 이 조합이 많이 쓰인 다는 것)
print(pad_x)
'''
pad_sequence '와꾸 맞춰주기'
# padding = 'post' (0 이 뒤로 채워진다)
(2,) : [3, 7],0,0,0
(1,) : [2] ,0,0,0,0
(3,) : [4,5,11],0,0
(5,) : [5,4,3,2,6 ]
>> (4,5)

# padding='pre' (시계열에 적합. 그러나 다른 것도 보통 이렇게 한다)
(2,) : 0,0,0,[3, 7]
(1,) : 0,0,0,0,[2]
(3,) : 0,0,[4,5,11]
(5,) : [5,4,3,2,6]
>> (4,5)
'''

# 원핫 인코딩하면 너무 용량많아지고 데이터 낭비가 심해지니까 벡터화를 시키는게 좋은데, 그게 바로바로 embedding!!!

word_size = len(token.word_index) + 1
print('전체 토큰 사이즈 :',word_size)  # 25개  # (12, 5)

from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten, LSTM

model = Sequential()
# model.add(Embedding(25, 100, input_length=5)) # 모델 엮기 위한 와꾸 맞춰주는 과정 # (None, 5, 10)
# 전체단어의 개수, 출력 노드의 숫자(?), (12,5)와꾸
# param은 input*output = 25 * 100 = 2500임
# 벡터화 시키는 종류 (아무래도 25개 이상이 acc1이 될거고 cost 생각하면 25를 넣는게 좋겠지)
model.add(Embedding(25, 100)) # LSTM 과 엮는경우 input_length 명시 안해줘도 된다 (얘는 3차원에서 두번째 자릿값을 주는거라서)
# model.add(Flatten()) # 임베딩 자체가 몇차원인지 모르니까(-> 3차원이네..) fatten 한대
# 자연어처리 시계열 느낌이라 (최근 데이터가 중요해서인가..? ) 주로 lstm쓴다. 아니면 한글이 동사가 뒤에 있어서?
model.add(Dense(3, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.summary()
'''
model.compile(optimizer='adam', loss='binary_crossentropy',
            metrics=['acc'])
model.fit(pad_x, labels, epochs=30)
acc = model.evaluate(pad_x,labels)[1]
print('acc :',acc)
'''