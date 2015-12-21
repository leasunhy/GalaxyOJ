from .user import User
from .problem import Problem
from .submission import Submission

model_list = [User, Problem, Submission]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

