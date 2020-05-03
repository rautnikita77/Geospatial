import pandas as pd
from sklearn.preprocessing import OneHotEncoder

arr_test = [[1, 2, 1], [1, 2, 2], [1, 2, 2]]
arr_train = [[1, 2, 1], [1, 2, 2], [1, 2, 3]]
df_train = pd.DataFrame(data=arr_train, columns=['a', 'b', 'c'])
df_test = pd.DataFrame(data=arr_test, columns=['a', 'b', 'c'])
print(df_test)
enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(pd.DataFrame(df_train['c']))
one_hot = enc.transform(pd.DataFrame(df_train['c'])).toarray()
one_hot = pd.DataFrame(data=one_hot, columns=['1', '2', '3'])
print(one_hot)
df_train = pd.concat((df_train, one_hot), axis=1, sort=False)
print(df_train)

one_hot = enc.transform(pd.DataFrame(df_test['c'])).toarray()
one_hot = pd.DataFrame(data=one_hot, columns=['1', '2', '3'])
print(one_hot)
df_test = pd.concat((df_test, one_hot), axis=1, sort=False)
print(df_test)


