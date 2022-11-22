def find_missing(arr, n=1000):
    expected_sum = (n + 1) * n // 2
    actual_sum = 0
    for i in arr:
        actual_sum += i
    return expected_sum - actual_sum


def main():
    arr = []
    for i in range(1, 1000):
        arr.append(i)

    print(find_missing(arr))


if __name__ == "__main__":
    main()
