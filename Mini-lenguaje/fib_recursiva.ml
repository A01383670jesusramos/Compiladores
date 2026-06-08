program test:
    var int result;

    int fibonacci(int n)
    start
        if (n <= 1){
            result = n;
        }
        else {
            result = fibonacci(n - 1) + fibonacci(n - 2);
        }
        return result;
    end

    start
        y = fibonacci(7);
    end