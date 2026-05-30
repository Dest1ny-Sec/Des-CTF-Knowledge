# 【传智杯WP】“传智杯”大学生IT技能大赛（程序设计挑战赛）省赛第二场C组WP

> 原文: https://www.ctfiot.com/307077.html
> ID: 307077

A — 《小苯点兵点将》

T =int(input())for_inrange(T): l, r =map(int,input().split()) print("YES"if(l +2) //3<= r //3else"NO")

B — 《小苯的迷宫行走》

import sysdata= list(map(int, sys.stdin.read().split()))ptr =0t =data[ptr]ptr +=1mask = (1<<30) -1for_inrange(t): n =data[ptr] m =data[ptr+1] ptr +=2 total = n * m end= ptr + total ans =0 whileptr <end: ans |=data[ptr] ifans == mask: ptr =end break ptr +=1 ptr =end print(ans)

C — 《小苯的好数》

importsysimportmathdata= list(map(int, sys.stdin.read().split()))ptr=0T= data[ptr]ptr+=1for_ in range(T): n= data[ptr] q= data[ptr +1] ptr+=2 a= data[ptr:
ptr + n] ptr+= n prefix=[0] * (n + 1) for i in range(n): x = a[i] ifx %2==0: prefix[i+1] = prefix[i] +1 else: s= math.isqrt(x) ifs %2==1and s * s == x: prefix[i+1] = prefix[i] +1 else: prefix[i+1] = prefix[i] for__ in range(q): l= data[ptr] r= data[ptr +1] ptr+=2 print(prefix[r] - prefix[l-1])

D — 《小苯的ovo》

importsysinput= sys.stdin.read().split()ptr=0T= int(input[ptr])ptr+=1for_ in range(T): n= int(input[ptr]) k= int(input[ptr+1]) ptr+=2 s= input[ptr] ptr+=1 ifn <3: print(0) continue cost=[] fori in range(n -2): cnt=0 ifs[i] != 'o': cnt+=1 ifs[i+1] != 'v': cnt+=1 ifs[i+2] != 'o': cnt+=1 cost.append(cnt) max_m= n //3 INF= float('inf') dp=[[INF] * (max_m + 1) for _ in range(n + 1)] dp[0][0] =0 best=[INF] * (max_m + 1) best[0] = 0 for i in range(1, n + 1): current_max_m = min(max_m, i // 3) for m in range(current_max_m + 1): dp[i][m] = dp[i-1][m] ifi >=3and (i-3) < len(cost): prev_i= i -3 c= cost[prev_i] form in range(1, current_max_m +1): prev_m= m -1 ifprev_m <= (prev_i) //3and dp[prev_i][prev_m] + c < dp[i][m]: dp[i][m] = dp[prev_i][prev_m] + c form in range(current_max_m +1): ifdp[i][m] < best[m]: best[m] = dp[i][m] ans=0 form in range(max_m, -1, -1): ifbest[m] <= k: ans= m breakprint(ans)

E — 《小苯的水瓶》

importsysinput=sys.stdin.read().split()idx =0T =int(input[idx])idx +=1for_ inrange(T): n =int(input[idx]) m =int(input[idx+1]) k =int(input[idx+2]) idx +=3 a = list(map(int, input[idx:
idx+n])) idx += n a.sort() prefix = [0] * (n +1) fori inrange(n): prefix[i+1] = prefix[i] + a[i] sum_a = prefix[-1] low =0 k_plus_m = k +m total_available=sum_a +k_plus_m max_possible=total_available// n high =max_possible best=0 whilelow <= high: mid = (low + high)// 2 required_total = mid * n ifsum_a + k < required_total: high = mid -1 continue lo, hi_c =0, n whilelo < hi_c: md_c = (lo + hi_c)// 2 ifa[md_c] < mid: lo = md_c +1 else: hi_c =md_c c=lo sum_d=mid * c - prefix[c] ifsum_d <= k_plus_m: best =mid low=mid +1 else: high = mid -1print(best)

F — 《小苯的旅行计划》

importsysfromcollections import dequeinput= sys.stdin.read().split()ptr=0T= int(input[ptr])ptr+=1for_ in range(T): n= int(input[ptr]) m= int(input[ptr+1]) ptr+=2 adj=[[] for _ in range(n+1)] for__ in range(n-1): u= int(input[ptr]) v= int(input[ptr+1]) w= int(input[ptr+2]) adj[u].append( (v, w) ) adj[v].append( (u, w) ) ptr+=3 LOG=20 parent=[0]*(n+1) weight = [0]*(n+1) depth_level = [0]*(n+1) depth_weight = [0]*(n+1) visited = [False]*(n+1) children = [[] for _ in range(n+1)] root=1 q= deque([root]) visited[root] = True parent[root] =0 whileq: u= q.popleft() forv, w in adj[u]: ifnot visited[v] and v != parent[u]: parent[v] = u weight[v] = w depth_level[v] = depth_level[u] +1 depth_weight[v] = depth_weight[u] + w visited[v] = True children[u].append(v) q.append(v) up=[[0]*(n+1) for _ in range(LOG)] up[0] = parent[:] fork in range(1, LOG): forv in range(1, n+1): up[k][v] = up[k-1][up[k-1][v]] diff=[0]*(n+1) S = 0 for __ in range(m): a = int(input[ptr]) b = int(input[ptr+1]) ptr +=2 x, y = a, b if depth_level[x] < depth_level[y]: x, y = y, x for k in reversed(range(LOG)): if depth_level[x] - (1 << k) >= depth_level[y]: x = up[k][x] ifx == y: lca= x else: fork in reversed(range(LOG)): ifup[k][x] != up[k][y]: x= up[k][x] y= up[k][y] lca= up[0][x] S+= depth_weight[a] + depth_weight[b] -2* depth_weight[lca] diff[a] +=1 diff[lca] -=1 diff[b] +=1 diff[lca] -=1 order=[] q= deque([root]) whileq: u= q.popleft() order.append(u) forv in children[u]: q.append(v) forv in reversed(order): ifv != root: diff[parent[v]] += diff[v] max_reduce=0 forv in range(2, n+1): current= weight[v] * diff[v] ifcurrent > max_reduce: max_reduce= current print(S - max_reduce)


```
T =int(input())for_inrange(T): l, r =map(int,input().split()) print("YES"if(l +2) //3<= r //3else"NO")
import sysdata= list(map(int, sys.stdin.read().split()))ptr =0t =data[ptr]ptr +=1mask = (1<<30) -1for_inrange(t): n =data[ptr] m =data[ptr+1] ptr +=2 total = n * m end= ptr + total ans =0 whileptr <end: ans |=data[ptr] ifans == mask: ptr =end break ptr +=1 ptr =end print(ans)
importsysimportmathdata= list(map(int, sys.stdin.read().split()))ptr=0T= data[ptr]ptr+=1for_ in range(T): n= data[ptr] q= data[ptr +1] ptr+=2 a= data[ptr:
ptr + n] ptr+= n prefix=[0] * (n + 1) for i in range(n): x = a[i] ifx %2==0: prefix[i+1] = prefix[i] +1 else: s= math.isqrt(x) ifs %2==1and s * s == x: prefix[i+1] = prefix[i] +1 else: prefix[i+1] = prefix[i] for__ in range(q): l= data[ptr] r= data[ptr +1] ptr+=2 print(prefix[r] - prefix[l-1])
importsysinput= sys.stdin.read().split()ptr=0T= int(input[ptr])ptr+=1for_ in range(T): n= int(input[ptr]) k= int(input[ptr+1]) ptr+=2 s= input[ptr] ptr+=1 ifn <3: print(0) continue cost=[] fori in range(n -2): cnt=0 ifs[i] != 'o': cnt+=1 ifs[i+1] != 'v': cnt+=1 ifs[i+2] != 'o': cnt+=1 cost.append(cnt) max_m= n //3 INF= float('inf') dp=[[INF] * (max_m + 1) for _ in range(n + 1)] dp[0][0] =0 best=[INF] * (max_m + 1) best[0] = 0 for i in range(1, n + 1): current_max_m = min(max_m, i // 3) for m in range(current_max_m + 1): dp[i][m] = dp[i-1][m] ifi >=3and (i-3) < len(cost): prev_i= i -3 c= cost[prev_i] form in range(1, current_max_m +1): prev_m= m -1 ifprev_m <= (prev_i) //3and dp[prev_i][prev_m] + c < dp[i][m]: dp[i][m] = dp[prev_i][prev_m] + c form in range(current_max_m +1): ifdp[i][m] < best[m]: best[m] = dp[i][m] ans=0 form in range(max_m, -1, -1): ifbest[m] <= k: ans= m breakprint(ans)
importsysinput=sys.stdin.read().split()idx =0T =int(input[idx])idx +=1for_ inrange(T): n =int(input[idx]) m =int(input[idx+1]) k =int(input[idx+2]) idx +=3 a = list(map(int, input[idx:
idx+n])) idx += n a.sort() prefix = [0] * (n +1) fori inrange(n): prefix[i+1] = prefix[i] + a[i] sum_a = prefix[-1] low =0 k_plus_m = k +m total_available=sum_a +k_plus_m max_possible=total_available// n high =max_possible best=0 whilelow <= high: mid = (low + high)// 2 required_total = mid * n ifsum_a + k < required_total: high = mid -1 continue lo, hi_c =0, n whilelo < hi_c: md_c = (lo + hi_c)// 2 ifa[md_c] < mid: lo = md_c +1 else: hi_c =md_c c=lo sum_d=mid * c - prefix[c] ifsum_d <= k_plus_m: best =mid low=mid +1 else: high = mid -1print(best)
importsysfromcollections import dequeinput= sys.stdin.read().split()ptr=0T= int(input[ptr])ptr+=1for_ in range(T): n= int(input[ptr]) m= int(input[ptr+1]) ptr+=2 adj=[[] for _ in range(n+1)] for__ in range(n-1): u= int(input[ptr]) v= int(input[ptr+1]) w= int(input[ptr+2]) adj[u].append( (v, w) ) adj[v].append( (u, w) ) ptr+=3 LOG=20 parent=[0]*(n+1) weight = [0]*(n+1) depth_level = [0]*(n+1) depth_weight = [0]*(n+1) visited = [False]*(n+1) children = [[] for _ in range(n+1)] root=1 q= deque([root]) visited[root] = True parent[root] =0 whileq: u= q.popleft() forv, w in adj[u]: ifnot visited[v] and v != parent[u]: parent[v] = u weight[v] = w depth_level[v] = depth_level[u] +1 depth_weight[v] = depth_weight[u] + w visited[v] = True children[u].append(v) q.append(v) up=[[0]*(n+1) for _ in range(LOG)] up[0] = parent[:] fork in range(1, LOG): forv in range(1, n+1): up[k][v] = up[k-1][up[k-1][v]] diff=[0]*(n+1) S = 0 for __ in range(m): a = int(input[ptr]) b = int(input[ptr+1]) ptr +=2 x, y = a, b if depth_level[x] < depth_level[y]: x, y = y, x for k in reversed(range(LOG)): if depth_level[x] - (1 << k) >= depth_level[y]: x = up[k][x] ifx == y: lca= x else: fork in reversed(range(LOG)): ifup[k][x] != up[k][y]: x= up[k][x] y= up[k][y] lca= up[0][x] S+= depth_weight[a] + depth_weight[b] -2* depth_weight[lca] diff[a] +=1 diff[lca] -=1 diff[b] +=1 diff[lca] -=1 order=[] q= deque([root]) whileq: u= q.popleft() order.append(u) forv in children[u]: q.append(v) forv in reversed(order): ifv != root: diff[parent[v]] += diff[v] max_reduce=0 forv in range(2, n+1): current= weight[v] * diff[v] ifcurrent > max_reduce: max_reduce= current print(S - max_reduce)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070235-wxsync-2026-05-c3d27a950a637fbdace028f04c9f6219.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070236-wxsync-2026-05-1744d45535172547071c0b85c9361dfb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070238-wxsync-2026-05-78c00666cfcd3737355e29dd8c8a6633.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070240-wxsync-2026-05-b3d174f3145c11e5488d0920043a033b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070241-wxsync-2026-05-4339c07929fedff0836fe751a7bc96e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070243-wxsync-2026-05-1f3967bad6a0037869ab043921d6ed26.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1778070244-wxsync-2026-05-8ed298cb060b526eda0dfd53d4e5ca15.png)