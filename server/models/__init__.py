from .user import User
from .problem import Problem, ProblemTag
from .submission import Submission

model_list = [User, Problem, Submission, ProblemTag]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

