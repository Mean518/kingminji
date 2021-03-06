'''
m28_eval1   _boston_회귀
m28_eval2   _cancer_이진분류
m28_eval3   _iris_다중분류
만들것

SelectFromModel 적용시켜서
1. 회귀     m29_eval1   _boston_회귀
2. 이진분류 m29_eval2   _cancer_이진분류
3. 다중분류 m29_eval3   _iris_다중분류

1. eval에 'loss'와 다른 지표 1개 더 추가
2. earlyStopping 적용
# 3. plot으로 그릴 것

4. 결과는 주석으로 소스 하단에 표시

m27 ~ 29까지 완벽 이해할 것
'''
# 이진분류_boston
from xgboost import XGBRegressor, plot_importance # 중요한걸 그리겠네
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score, r2_score
import numpy as np
# 이중분류 모델
dataset = load_boston()
x = dataset.data
y = dataset.target


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=66)


model = XGBRegressor(n_estimators=100, learning_rate=0.01) # 나무의 개수는 결국 epo다
model.fit(x_train, y_train, verbose=True, eval_metric=['logloss','rmse'], eval_set=[(x_train,y_train),(x_test,y_test)]
        , early_stopping_rounds=100) 

y_pred = model.predict(x_test)
r2 = r2_score(y_test, y_pred)
print('r2 score :%.2f%%' %(r2*100.0))



thresholds = np.sort(model.feature_importances_)

print(thresholds)

for thresh in thresholds : # 컬럼수만큼 돈다! 빙글빙글
    selection = SelectFromModel(model, threshold=thresh, prefit=True)
    selection_x_train = selection.transform(x_train)
    # print(selection_x_train.shape) # 칼럼이 하나씩 줄고 있는걸 알 수 있음 (가장 중요 x를 하나씩 지우고 있음)
    
    selection_model = XGBRegressor()
    selection_model.fit(selection_x_train, y_train)

    select_x_test = selection.transform(x_test)
    x_pred = selection_model.predict(select_x_test)

    score = r2_score(y_test, x_pred)
    print('R2는',score)
    print("Thresh=%.3f, n=%d, R2: %.2f%%" %(thresh, selection_x_train.shape[1], score*100.0))

