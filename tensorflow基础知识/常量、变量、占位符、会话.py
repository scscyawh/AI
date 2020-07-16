import tensorflow as tf
# 常量
a = tf.constant(2)

# 变量(定义变量后必须初始化)
b = tf.Variable(4.0, tf.float32)
c = tf.Variable(1.0, tf.float32)
result = tf.add(b, c)

# 占位符也是变量(tf特有数据类型，有些变量定义时不知道数值，需要通过外部输入
# 比如训练数据，这时候就用到了占位符。用sess.run时必须通过feed_dict传参数。
# 函数接口为 tf.placeholder(数据类型，数据形状，名字)
d = tf.placeholder(tf.float32)
e = tf.placeholder(tf.float32)
f = tf.multiply(d, e)

# 创建session（理解，所有的语句都是静态模型，需要放在session里启用模型）
sess = tf.Session()

# 所有变量初始化
init = tf.global_variables_initializer()
# 启用初始化
sess.run(init)
# 启用模型并输出结果
print('常量 a=', sess.run(a))
print('变量 b+c=', sess.run(result))
print('占位符 d*e=', sess.run(f, feed_dict={d: 8.0, e: 3.5}))
sess.close()
