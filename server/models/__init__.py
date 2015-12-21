from .user import User
from .problem import Problem, ProblemTag
from .submission import Submission
from .contest import Contest
from .post import Post, Notification, Solution, PostTag
from .comment import Comment

model_list = [User, Problem, Submission, ProblemTag, Contest, Post, Notification, Solution, PostTag, Comment]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

