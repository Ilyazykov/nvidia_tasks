def findMissing(arr):
    n = 1000
    expected_sum = (n + 1) * n / 2
    sum = 0
    for i in arr:
        sum += i
    return expected_sum - sum
