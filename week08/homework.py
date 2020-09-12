###
#容器序列：list, tuple, dict, collections.deque
#扁平序列：str
#可变序列：list, dict, collections.deque
#不可变序列：str, tuple

########
def simple_map(func,iter):
    return (func(e) for e in iter)
print(simple_map(str,[1,2,3]))




#######
import time
def timer(func):
    def inner(*args,**kwargs):
        start = time.time()
        func(*args,**kwargs)
        print(time.time() - start)
    return inner

@timer
def test_timer(t):
    return t
print(test_timer(3))
