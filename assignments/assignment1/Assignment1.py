# ## Loop for Sequence Types

# In[16]:


animals = ['cat', 'dog', 'monkey']
for animal in animals:
    print (animal)
for idx, animal in enumerate(animals, 1):
    print ('#%d: %s' % (idx, animal))


# ## Dictionary

# In[17]:


d = {'cat': 'cute', 'dog': 'furry'}
print (d['cat'])
print ('cat' in d)
d['fish'] = 'wet'
print (d['fish'])
# print (d['monkey']) 'raise KeyError: 'monkey'


# In[18]:


print (d.get('monkey', 'N/A'))
print (d.get('fish', 'N/A'))
del d['fish']
print (d.get('fish', 'N/A'))


# In[19]:


d = {'person': 2, 'cat': 4, 'spider': 8}
for animal in d:
    print ('A %s has %d legs' % (animal, d[animal]))
for animal, legs in d.items():
    print ('A %s has %d legs' % (animal, legs))


# ## Control Flow

# In[20]:


for i in range(10):
    print (i, end=', ')
print ()
for i in range(3, 10):
    print (i, end=', ')
print ()
for i in range(0, 10, 2):
    print (i, end=', ')
print ()

# In[21]:


i = 0
while i < 10:
    i += 1
    print (i, end='')
print ()

# ## Function

# In[22]:


def sign(x):
    if x > 0: return 'positive'
    elif x < 0: return 'negative'
    else: return 'zero'
for x in range(-1, 2):
    print (sign(x))


# In[23]:


class Student(object):
    def __init__(self, name):
        self.name = name
    def set_age(self, age):
        self.age = age
    def set_major(self, major):
        self.major = major
anna = Student('anna')
anna.set_age(21)
anna.set_major('physics')


# In[24]:


class MasterStudent(Student):
    def set_lab(self, lab):
        self.lab = lab

