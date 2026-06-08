program test:
    var int i;
    var int result;

    int factorial(int n)
    start
        result = 1;
        i = 2;
        while (i <= n) {
            result = result * i;
            i = i + 1;
        }
        return result;
    end

    start
        y = factorial(5);
    end