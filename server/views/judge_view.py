from . import judge

from .. import q

def hello_world(word):
    for i in range(18):
        print("Haha")

@judge.route('/test')
def test(submission_id):
    # get url that the person has entered
    job = q.enqueue_call(
        #TODO
        func=hello_world, args=("haha",), result_ttl=5000
    )
    print(job.get_id())
    return redirect('/')


