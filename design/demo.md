# Demo Usage

[2618. 租购](https://acm.sjtu.edu.cn/OnlineJudge/problem/2618)
```
@run {
    n: r(1000, 2000)    \n
    @loop n {                   # you may also write @for n, in the new version;
        a: r(1e2, 1e8)
        %delta = r(1e2, 1e8)     # '%' defines a hidden variable, which is not outputted;
        b: a + delta    \n
    }
}
```

[1008. LSZ的雪地脚印](https://acm.sjtu.edu.cn/OnlineJudge/problem/1008)
```
@path "./1008.in"
@run {
    n: r(1, 100)
    m: r(1, 100)                \n
    @loop n {
        c: rstr("X\-", len=m)   \n
    }
}
```