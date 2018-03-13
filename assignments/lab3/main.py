
# coding: utf-8

# In[45]:


import numpy as np


# In[46]:


M = np.arange(2, 27)


# In[47]:


M = M.reshape((5, 5))
print (M)


# In[48]:


M[1:-1, 1:-1] = 0
print (M)


# In[49]:


M = np.matmul(M, M)
print (M)


# In[55]:


v = M[0]
mfunc = np.vectorize(lambda x: x**2)
m = np.sqrt(sum(mfunc(v)))
print (m)

