program test:
    int factorial(int n)
    start
        if (n == 0){
            return 1;
        }
        else {
            return n * factorial(n - 1);
        }
    end

    start
        y = factorial(5);
    end