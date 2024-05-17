import sys;
from collections import deque

children = int(input())
want = list(map(int, input().split()))

index = 0;
count = [0 for _ in range(children)]
ans = [0 for _ in range(children)]
time = 1

while True:
    if 0 not in ans:
        break;
    

    index = index % children
    if want[index] > count[index]:
        count[index] = count[index]+1
    else:
        index = index+1
        continue

    if want[index] == count[index]:
        ans[index] = time

    index = index+1
    time = time+1
print(ans)
        
