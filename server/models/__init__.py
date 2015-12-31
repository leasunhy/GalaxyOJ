from .user import User
from .problem import Problem, ProblemTag
from .submission import Submission
from .contest import Contest
from .post import Post, Notification, Solution, PostTag, Tutorial
from .comment import Comment
from .standing import Standing

model_list = [User, Problem, Submission, ProblemTag, Contest,
        Post, Notification, Solution, PostTag, Comment, Tutorial, Standing]
model_dict = dict(map(lambda x: (x.__name__, x), model_list))

