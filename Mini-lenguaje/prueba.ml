program test:
    var int i;
    var int j;

    int uno(int x)
    start
        return x * 2;
    end

    int dos(int x)
    start
        return x + uno(x);
    end

    start
        i = 5;
        print(dos(i + 3 - 1));
    end
