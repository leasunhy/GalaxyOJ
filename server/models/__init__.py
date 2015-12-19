from .user import User
from .problem import Problem

model_list = [User, Problem]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

