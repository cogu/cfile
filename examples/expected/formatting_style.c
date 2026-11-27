int check(int x, int *ptr)
{
  if (ptr == NULL) {
    return -1;
  } else {
    return *ptr + x;
  }
}
