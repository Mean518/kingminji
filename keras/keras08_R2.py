#1. 데이터
import numpy as np
x_train = np.array([1,2,3,4,5,6,7,8,9,10])
y_train = np.array([1,2,3,4,5,6,7,8,9,10])
x_test = np.array([11,12,13,14,15])
y_test = np.array([11,12,13,14,15])

# shift + del 열삭제/ 커서놓고 cntrol+c 하면 열 복사가 됨

#2. 모델구성
from keras.models import Sequential 
from keras.layers import Dense # DNN 구조의 가장 베이스가 되는 모델
model = Sequential()
model.add(Dense(5, input_dim=1)) #인풋레이어/ 5개의 노드 아웃풋/ # 10개짜리 한 덩어리 input하겠다
model.add(Dense(3)) # 인풋이 5, 아웃풋이 3개 노드인 아웃풋 히든레이어
model.add(Dense(100))  # 줄마다 W가 점점 바뀌고 있는것임
model.add(Dense(300))
model.add(Dense(500))
model.add(Dense(500))
model.add(Dense(300))
model.add(Dense(1)) # 아웃레이어

#3. 알아듣게 설명한 후 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mse'])
model.fit(x_train,y_train, epochs=200, batch_size=3)  # Dense보다 epochs가  중요한듯

#4. 성능평가/ --> 왜 metrics에서 r2를 안하고 따로 찾은거지?
# metrics = ['mse','rmse','r2'] 안하는 이유는...?
loss,mse = model.evaluate(x_test,y_test)  # evaluate반환하는건 loss, metrics 순임!
print('mse 는',mse)

#4. 성능평가 2
# y햇 만들어주기
y_predict = model.predict(x_test)
print(y_predict) # 예측값

# RMSE 구하기
from sklearn.metrics import mean_squared_error #MSE임

def RMSE(y_test, y_predict) :
    return np.sqrt(mean_squared_error(y_test, y_predict))

print('MSE 는', mean_squared_error(y_test, y_predict) )
print('RMSE 는', RMSE(y_test, y_predict) )

# R2 구하기
from sklearn.metrics import r2_score # ㅋㅋ이것도 metrics 안에 들어있네
r2 = r2_score(y_test, y_predict)
print('R2는 ', r2)

