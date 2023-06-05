#include <iostream>
#include <map>

long long n, p, q;
std::map<long long, long long> arr;

long long dp(long long i)
{
    if (arr.count(i))
    {
        return arr[i];
    }

    return arr[i] = dp(i / p) + dp(i / q);
}

int main()
{
    scanf("%lld %lld %lld", &n, &p, &q);

    arr[0] = 1;

    printf("%lld\n", dp(n));

    return 0;
}