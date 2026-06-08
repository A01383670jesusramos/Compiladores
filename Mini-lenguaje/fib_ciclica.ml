program test:
    var int a;
    var int b;
    var int c;
    var int i;

    int fibonacci(int n)
    start
        a = 0;
        b = 1;
        i = 2;
        if (n <= 1){
            return n;
        }
        while (i <= n){
            c = a + b;
            a = b;
            b = c;
            i = i + 1;
        }
        return b;
    end

    start
        y = fibonacci(7);
    end