def show_ids(label, left, right):
    same = left is right
    left_id = id(left)
    right_id = id(right)
    print(
        f"{label}: id(left)={left_id} ({hex(left_id)}) "
        f"id(right)={right_id} ({hex(right_id)}) same={same}"
    )


def make_257_by_calc():
    return 255 + 2


def make_257_by_int():
    return int("257")


def make_257_by_sum():
    x = 200
    y = 57
    return x + y


def main():
    a = 256
    b = 256
    show_ids("literal 256", a, b)

    c = 257
    d = 257
    show_ids("literal 257", c, d)

    e = make_257_by_calc()
    f = make_257_by_calc()
    show_ids("calc 257", e, f)

    g = make_257_by_int()
    h = make_257_by_int()
    show_ids("int('257')", g, h)

    i = make_257_by_sum()
    j = make_257_by_sum()
    show_ids("sum 200+57", i, j)

    x = 1000
    y = 1000
    show_ids("literal 1000", x, y)


if __name__ == "__main__":
    main()
