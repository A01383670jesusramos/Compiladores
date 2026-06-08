program test:

    int doble(int x)
    start
        return x + x;
    end

    int suma(int a, int b)
    start
        return a + b;
    end

    start
        x = doble(suma(10,20));
    end