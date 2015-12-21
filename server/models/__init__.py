from .user import User
from .problem import Problem, ProblemTag
from .submission import Submission
from .contest import Contest

model_list = [User, Problem, Submission, ProblemTag, Contest]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

