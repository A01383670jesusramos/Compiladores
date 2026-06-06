program test:
    var int x;

    start
        x = 0;

        while (x < 5)
            while (x < 3)
                x = x + 1;

        print(x);
    end