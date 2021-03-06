import tensorflow as tf
import numpy as np
tf.set_random_seed(777)

x_data = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=np.float32)
y_data = np.array([[0],[1],[1],[0]],dtype=np.float32)
y_data = y_data.reshape(-1,1)

x = tf.placeholder(tf.float32, shape=[None,2])
y = tf.placeholder(tf.float32, shape=[None,1])

w1 = tf.Variable(tf.random_normal([2,100]), name='weight1')
b1 = tf.Variable(tf.random_normal([100]), name='bias')
layer1 = tf.sigmoid(tf.matmul(x,w1) + b1)
# model.add(Dense(100, input_dim=2))

w2 = tf.Variable(tf.random_normal([100,50]), name='weight1')
b2 = tf.Variable(tf.random_normal([50]), name='bias')
layer2 = tf.sigmoid(tf.matmul(layer1,w2) + b2)
# model.add(Dense(50, input_dim=100))

w3 = tf.Variable(tf.random_normal([50,1]), name='weight2')
b3 = tf.Variable(tf.random_normal([1]), name='bias2')
hypothesis = tf.sigmoid(tf.matmul(layer2,w3) + b3)
# model.add(Dense(1))

cost = -tf.reduce_mean(y* tf.log(hypothesis) + (1-y) * tf.log(1-hypothesis))  # sigmoid에 대한 정의
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.5e-6)
model = optimizer.minimize(cost)

predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, y), dtype=tf.float32))
mapping = {x:x_data, y:y_data}

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for step in range(2001) :
        _, mse = sess.run([model, cost], feed_dict=mapping)
        if step % 500 == 0 :
            print('step은',step,' mse는',mse) #'  기울기는',weight,'  절편은', bias)

    real_y, h, pre, acc = sess.run([y,hypothesis, predicted, accuracy], feed_dict=mapping)
    print(f'acc는 {acc}')  #, real_y는 {real_y}, pre는 {pre}')

