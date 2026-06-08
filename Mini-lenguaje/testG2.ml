program test:

    int cinco()
    start
        return 5;
    end

    int doble(int x)
    start
        return x + x;
    end

    start
        x = doble(cinco());
        print(x);
    end
